# IPTV Playlist API 
 
A powerful IPTV playlist API with 325,842 channels across 355 categories. 
 
## Features 
 
- **325,842 channels** available 
- **355 categories** to browse 
- **Real-time search** functionality 
- **Category filtering** 
- **Pagination support** 
- **CORS enabled** for web applications 
 
## API Endpoints 
 
- `GET /api/stats` - Get playlist statistics 
- `GET /api/channels` - Get all channels (paginated) 
- `GET /api/search?q=query` - Search channels by name 
- `GET /api/categories` - Get all categories 
- `GET /api/categories/{category}` - Get channels by category 
- `GET /api/playlist` - Download full playlist 
- `GET /web_interface.html` - Web interface 
 
## Deployment 
 
This API is automatically deployed to Railway via GitHub Actions. 
 
## Live Demo 
 
Visit: https://your-project.railway.app 
 
--- 
Built with Flask and deployed on Railway 
