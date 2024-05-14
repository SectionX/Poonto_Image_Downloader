from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, JSONResponse, FileResponse

from .manage import create_process
from .manage import upload_excel
from .manage import check_progress
from .manage import request

app = FastAPI()

@app.post('/images/{supplier_name}/upload')
def upload_products_worksheet(supplier_name: str) -> JSONResponse:
    ...

@app.get('/images/{supplier_name}/run')
def start_downloader_process(supplier_name: str) -> JSONResponse:
    ...

@app.get('/images/{supplier_name}/check') 
def check_downloader_progress(supplier_name: str) -> JSONResponse:
    ...

@app.get('/images/{supplier_name}/request') 
def serve_image_archive(supplier_name: str) -> FileResponse: 
    ...