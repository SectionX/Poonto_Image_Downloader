#!/usr/bin/python
import sys
from pathlib import Path
    
supplier_path = Path(__file__).parent
app_path = supplier_path.parent.parent.parent
sys.path.append(str(app_path))

from ...backend.pagegetter import ProductPageGetter
from ...backend.worksheet import WorksheetImporter
from ...backend.downloader import ImageDownloader
from ...backend.utils import IntegrityChecker, Archiver
from ...backend.poonto.imagecropper import resize_image

from bs4 import BeautifulSoup
from pathlib import Path


class SupplierPageGetter(ProductPageGetter):

    APP_PATH = Path(__file__).parent

    def search(self, sku, *args) -> str | None:
        pass
                
    def parse_html(self, html_page, *args) -> list[str]:
        soup = BeautifulSoup(html_page, features='html.parser')
        elements = soup.select('.banner-slider a')
        links = [a.get('href') for a in elements]
        return links
        
class SupplierImageDownloader(ImageDownloader):

    def transform_image(self, imagebytes: bytes, filename: str) -> bytes:
        if filename.find('.') == -1:
            return imagebytes
        else:
            ext = filename.rstrip().split('.')[-1]
        return resize_image(imagebytes, (740, 740), ext)
                

def main():
    ws = WorksheetImporter(supplier_path=supplier_path).worksheet
    SupplierPageGetter(ws, 'Title', 'ProductCode', 'ProductURL', supplier_path=supplier_path).run()
    ImageDownloader(supplier_path=supplier_path).run()
    ic = IntegrityChecker(log=True, supplier_path=supplier_path)
    Archiver(supplier_path, 'Vamvax', ic).run()

if __name__ == '__main__':
    main()
