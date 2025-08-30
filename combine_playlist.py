#!/usr/bin/env python3
"""
Playlist Chunk Loader
Combines split playlist chunks back into one file
"""

import os
import glob

def combine_playlist_chunks():
    """Combine all playlist chunks into one file"""
    
    # Find all chunk files
    chunk_files = sorted(glob.glob("playlist_part_*.m3u"))
    
    if not chunk_files:
        print("❌ No chunk files found")
        return
    
    print(f"🔗 Combining {len(chunk_files)} chunks...")
    
    # Combine chunks
    with open("converted_playlist.m3u", 'w', encoding='utf-8') as output:
        for i, chunk_file in enumerate(chunk_files):
            print(f"📁 Processing {chunk_file}...")
            
            with open(chunk_file, 'r', encoding='utf-8') as input_file:
                content = input_file.read()
                
                # Remove header from all chunks except first
                if i > 0:
                    lines = content.split('\n')
                    if lines and lines[0].startswith('#EXTM3U'):
                        content = '\n'.join(lines[1:])
                
                output.write(content)
                if not content.endswith('\n'):
                    output.write('\n')
    
    # Get final file size
    final_size = os.path.getsize("converted_playlist.m3u")
    final_size_mb = final_size / (1024 * 1024)
    
    print(f"✅ Combined into converted_playlist.m3u ({final_size_mb:.1f}MB)")
    print("🎯 Ready to use with your API!")

if __name__ == "__main__":
    combine_playlist_chunks()
