#!/usr/bin/env python3
"""
IPTV Playlist API - Production Version for Railway
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import re
import os
from typing import List, Dict
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlaylistAPI:
    def __init__(self, playlist_file: str = None):
        self.playlist_file = playlist_file or os.getenv('PLAYLIST_FILE', 'converted_playlist.m3u')
        self.channels = []
        self.categories = set()
        self.load_playlist()
    
    def load_playlist(self):
        try:
            if not os.path.exists(self.playlist_file):
                logger.error(f"Playlist file not found: {self.playlist_file}")
                return
            
            logger.info(f"Loading playlist from: {self.playlist_file}")
            
            with open(self.playlist_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.channels = self.parse_playlist(content)
            self.categories = self.extract_categories()
            
            logger.info(f"Loaded {len(self.channels)} channels with {len(self.categories)} categories")
            
        except Exception as e:
            logger.error(f"Error loading playlist: {e}")
    
    def parse_playlist(self, content: str) -> List[Dict]:
        channels = []
        lines = content.split('\n')
        current_channel = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF:'):
                current_channel = self.parse_extinf_line(line)
            elif line.startswith('http') and current_channel:
                current_channel['stream_url'] = line
                channels.append(current_channel.copy())
                current_channel = {}
        
        return channels
    
    def parse_extinf_line(self, line: str) -> Dict:
        channel = {}
        
        tvg_id_match = re.search(r'tvg-id="([^"]*)"', line)
        if tvg_id_match:
            channel['tvg_id'] = tvg_id_match.group(1)
        
        tvg_logo_match = re.search(r'tvg-logo="([^"]*)"', line)
        if tvg_logo_match:
            channel['tvg_logo'] = tvg_logo_match.group(1)
        
        group_title_match = re.search(r'group-title="([^"]*)"', line)
        if group_title_match:
            channel['group_title'] = group_title_match.group(1)
        
        parts = line.split(',')
        if len(parts) > 1:
            channel['name'] = parts[-1].strip()
        
        return channel
    
    def extract_categories(self) -> set:
        categories = set()
        for channel in self.channels:
            if channel.get('group_title'):
                categories.add(channel['group_title'])
        return sorted(list(categories))
    
    def search_channels(self, query: str, limit: int = 50) -> List[Dict]:
        query = query.lower()
        results = []
        
        for channel in self.channels:
            if query in channel.get('name', '').lower():
                results.append(channel)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_channels_by_category(self, category: str, limit: int = 100) -> List[Dict]:
        results = []
        
        for channel in self.channels:
            if channel.get('group_title') == category:
                results.append(channel)
                if len(results) >= limit:
                    break
        
        return results

playlist_api = PlaylistAPI()

@app.route('/')
def home():
    return jsonify({
        "message": "IPTV Playlist API - Railway Hosted",
        "version": "1.0.0",
        "hosting": "Railway",
        "endpoints": {
            "/api/stats": "Get playlist statistics",
            "/api/channels": "Get all channels (paginated)",
            "/api/channels/<tvg_id>": "Get specific channel by tvg-id",
            "/api/search": "Search channels by name",
            "/api/categories": "Get all categories",
            "/api/categories/<category>": "Get channels by category",
            "/api/playlist": "Get full playlist file",
            "/api/random": "Get random channels"
        },
        "total_channels": len(playlist_api.channels),
        "total_categories": len(playlist_api.categories)
    })

@app.route('/api/stats')
def get_stats():
    category_counts = {}
    for channel in playlist_api.channels:
        category = channel.get('group_title', 'Unknown')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    return jsonify({
        "total_channels": len(playlist_api.channels),
        "total_categories": len(playlist_api.categories),
        "categories": list(playlist_api.categories),
        "category_counts": category_counts,
        "last_updated": datetime.now().isoformat(),
        "hosting": "Railway"
    })

@app.route('/api/channels')
def get_channels():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    channels = playlist_api.channels[start_idx:end_idx]
    
    return jsonify({
        "channels": channels,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(playlist_api.channels),
            "pages": (len(playlist_api.channels) + per_page - 1) // per_page
        }
    })

@app.route('/api/channels/<tvg_id>')
def get_channel(tvg_id):
    for channel in playlist_api.channels:
        if channel.get('tvg_id') == tvg_id:
            return jsonify(channel)
    
    return jsonify({"error": "Channel not found"}), 404

@app.route('/api/search')
def search_channels():
    query = request.args.get('q', '')
    limit = min(request.args.get('limit', 50, type=int), 100)
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    results = playlist_api.search_channels(query, limit)
    
    return jsonify({
        "query": query,
        "results": results,
        "total_found": len(results)
    })

@app.route('/api/categories')
def get_categories():
    return jsonify({
        "categories": list(playlist_api.categories),
        "total": len(playlist_api.categories)
    })

@app.route('/api/categories/<category>')
def get_channels_by_category(category):
    limit = min(request.args.get('limit', 100, type=int), 200)
    
    results = playlist_api.get_channels_by_category(category, limit)
    
    return jsonify({
        "category": category,
        "channels": results,
        "total": len(results)
    })

@app.route('/api/playlist')
def get_playlist():
    if os.path.exists(playlist_api.playlist_file):
        return send_file(
            playlist_api.playlist_file,
            mimetype='application/vnd.apple.mpegurl',
            as_attachment=True,
            download_name='playlist.m3u'
        )
    else:
        return jsonify({"error": "Playlist file not found"}), 404

@app.route('/api/random')
def get_random_channels():
    import random
    
    count = min(request.args.get('count', 10, type=int), 50)
    random_channels = random.sample(playlist_api.channels, min(count, len(playlist_api.channels)))
    
    return jsonify({
        "channels": random_channels,
        "count": len(random_channels)
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "channels_loaded": len(playlist_api.channels) > 0,
        "timestamp": datetime.now().isoformat(),
        "hosting": "Railway",
        "total_channels": len(playlist_api.channels),
        "total_categories": len(playlist_api.categories)
    })

@app.route('/web_interface.html')
def web_interface():
    return send_file('web_interface.html', mimetype='text/html')

@app.route('/web')
def web_interface_redirect():
    return send_file('web_interface.html', mimetype='text/html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"IPTV Playlist API Starting on Railway...")
    print(f"Loaded {len(playlist_api.channels)} channels")
    print(f"Available categories: {len(playlist_api.categories)}")
    print(f"API will be available on port: {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
