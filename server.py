"""
Starts the test server
"""


import uvicorn

if __name__ == '__main__':
    uvicorn.run('Image_Downloader.app:app', port=8080, reload=True)
