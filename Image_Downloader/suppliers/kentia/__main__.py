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

# Useful libraries for this program
import requests
from bs4 import BeautifulSoup
from PIL import Image


class SupplierPageGetter(ProductPageGetter):

    search_api = 'https://www.kentia.gr/index.php?route=extension/module/live_search&filter_name={}'

    def search(self, sku: str, *args) -> str | None:
        try:
            resp = requests.get(self.search_api.format(sku))
            resp.raise_for_status()
            data = resp.json()
            results = data['products'][0]
            url = results['url']
            return url
        except Exception as e:
            return None
        

    def parse_html(self, html_page: str, *args) -> list[str]:
        soup = BeautifulSoup(html_page, features='html.parser')
        elements = soup.select('li a.thumbnail')
        links: list[str] = []
        links = [str(tag.get('href')) for tag in elements]
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
    Archiver(supplier_path, 'Kentia', ic).run()


if __name__ == '__main__':
    main()
