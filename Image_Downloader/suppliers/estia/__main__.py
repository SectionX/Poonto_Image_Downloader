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

import requests
from bs4 import BeautifulSoup


class SupplierPageGetter(ProductPageGetter):

    api = 'https://estiahomeart.gr/instantSearchFor?q={}'

    def search(self, sku, *args) -> str | None:
        print(f'Attempting to call the search API for product {sku}')
        resp = requests.get(self.api.format(sku))
        data = resp.json()

        total = data['TotalProducts']
        if total < 1:
            return None
        if total == 1:
            product = data['Products'][0]
            url = 'https://estiahomeart.gr' + product['CustomProperties']['Url']
            return url
        if total > 1:
            for product in data['Products']:
                if sku in repr(product):
                    return 'https://estiahomeart.gr' + product['CustomProperties']['Url']
                
                
    def parse_html(self, html_page, *args) -> list[str]:
        soup = BeautifulSoup(html_page, features='html.parser')
        elements = soup.select('.picture-thumbs a.thumb-item')
        links = [a.get('data-full-image-url') for a in elements]

        #handling odd pages case 1
        if len(links) == 0:
            elements = soup.select('div.picture a.picture-link')
            links = [a.get('data-full-image-url') for a in elements]

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
    Archiver(supplier_path, 'Estia', ic).run()

if __name__ == '__main__':
    main()