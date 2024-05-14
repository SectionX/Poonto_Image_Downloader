"""
Starts the test server with the reload parameter.
It's hardcoded to listen on port 8080.
"""

import uvicorn

if __name__ == '__main__':
    uvicorn.run('Image_Downloader.app:app', port=8080, reload=True)
