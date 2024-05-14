#!/usr/bin/python

'''
A script meant to spawned as a process from the controller.py script.
'''

import sys
import os
from pathlib import Path

import xmltodict

from ...backend.xmlreader import XmlReader
from ...backend.downloader import ImageDownloader
from ...backend.utils import IntegrityChecker, Archiver
from ...backend.poonto.imagecropper import resize_image

supplier_path = Path(__file__).parent
app_path = supplier_path.parent.parent.parent
sys.path.append(str(app_path))
sys.path.extend([str(path) for path in supplier_path.parents])

class SupplierImageDownloader(ImageDownloader):

    '''
    Standard Poonto image transformation.
    '''

    def transform_image(self, image: bytes, filename: str) -> bytes:
        ext = filename.rsplit(os.sep, maxsplit=1)[-1]
        return resize_image(image, (740, 740), ext)

class SupplierXMLreader(XmlReader):

    '''
    Definition for Artelibre feed.
    '''

    def create_worksheet(self, file_contents, product_node) -> None:
        raise NotImplementedError()

    def _traverse_dict(self, _dict, product_node) -> list[dict]:
        stack = [_dict]
        while stack:
            _dict = stack.pop()
            if product_node in _dict:
                data = _dict[product_node]
            else:
                for key in _dict.keys():
                    stack.append(_dict[key])

        if data is None:
            raise KeyError()
        if not isinstance(data, list):
            raise ValueError()
        return data

    def create_links_txt(self, file_contents: str, product_node: str):
        _dict = xmltodict.parse(file_contents)
        data = self._traverse_dict(_dict, product_node)
        entries = []
        for item in data:
            sku = item.get('sku')
            images = item.get('images')
            entries.append((sku, images))

        stringbuffer = ''
        for sku, image_dict in entries:
            if not (sku or images):
                continue
            images = image_dict['image']
            if isinstance(images, str):
                stringbuffer += f'{sku}_0|{images}\n'
            elif isinstance(images, list):
                for i, image in enumerate(images):
                    stringbuffer += f"{sku}_{i}|{image}\n"

        with (supplier_path / 'links.txt').open('w') as f:
            f.write(stringbuffer)


def main():

    '''
    Is called by the controller.py script. Don't attempt to run as top level.
    '''

    _ = SupplierXMLreader(supplier_path, 'Product', None)
    ImageDownloader(supplier_path=supplier_path).run()
    ic = IntegrityChecker(log=True, supplier_path=supplier_path)
    Archiver(supplier_path, 'Artelibre', ic).run()


if __name__ == '__main__':
    main()
