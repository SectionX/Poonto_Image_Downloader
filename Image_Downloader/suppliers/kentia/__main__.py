#!/usr/bin/python

'''
A script meant to spawned as a process from the controller.py script.
'''

import sys
import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from ...backend.pagegetter import ProductPageGetter
from ...backend.worksheet import WorksheetImporter
from ...backend.downloader import ImageDownloader
from ...backend.utils import IntegrityChecker, Archiver
from ...backend.poonto.imagecropper import resize_image

supplier_path = Path(__file__).parent
app_path = supplier_path.parent.parent.parent
sys.path.append(str(app_path))


class SupplierPageGetter(ProductPageGetter):

    '''
    Class that handles finding product webpages
    and scraping the content. Define bellow how
    this happens.
    '''

    search_api = 'https://www.kentia.gr/index.php?route=extension/module/live_search&filter_name={}'

    def search(self, sku: str, *args) -> str | None:

        try:

            resp = requests.get(self.search_api.format(sku), timeout=20)
            resp.raise_for_status()
            data = resp.json()
            results = data['products'][0]
            url = results['url']
            return url

        except (requests.HTTPError, TypeError) as e:

            e.add_note('Product page not found')
            return None


    def parse_html(self, html_page: str, *args) -> list[str]:
        soup = BeautifulSoup(html_page, features='html.parser')
        elements = soup.select('li a.thumbnail')
        links: list[str] = []
        links = [str(tag.get('href')) for tag in elements]
        return links


class SupplierImageDownloader(ImageDownloader):

    '''
    Standard Poonto image transformation.
    '''

    def transform_image(self, image: bytes, filename: str) -> bytes:
        ext = filename.rsplit('.', maxsplit=1)[-1]
        return resize_image(image, (740, 740), ext)


def main():
    '''
    The function to be called by controller.py.
    Don't attempt to run as top level.
    '''

    ws = WorksheetImporter(supplier_path=supplier_path).worksheet
    SupplierPageGetter(ws, supplier_path,
                       'Title', 'ProductCode', 'ProductURL',
                       failed_only=False).run()
    SupplierImageDownloader(supplier_path=supplier_path).run()
    ic = IntegrityChecker(log=True, supplier_path=supplier_path)
    Archiver(supplier_path, 'Kentia', ic).run()


if __name__ == '__main__':
    main()
