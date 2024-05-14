#!/usr/bin/python

'''
A script meant to spawned as a process from the controller.py script.
'''

import sys
import os
from pathlib import Path

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

    def search(self, sku, *args) -> str | None:
        pass

    def parse_html(self, html_page, *args) -> list[str]:
        soup = BeautifulSoup(html_page, features='html.parser')
        elements = soup.select('.banner-slider a')
        links = [a.get('href') for a in elements]
        if links is None:
            return []
        return links #type: ignore

class SupplierImageDownloader(ImageDownloader):

    '''
    Standard Poonto image transformation.
    '''

    def transform_image(self, image: bytes, filename: str) -> bytes:
        ext = filename.rsplit(os.sep, maxsplit=1)[-1]
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
    ImageDownloader(supplier_path=supplier_path).run()
    ic = IntegrityChecker(log=True, supplier_path=supplier_path)
    Archiver(supplier_path, 'Vamvax', ic).run()

if __name__ == '__main__':
    main()
