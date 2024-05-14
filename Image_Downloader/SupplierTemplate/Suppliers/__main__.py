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

# Useful libraries for this script
# import requests
# from bs4 import BeautifulSoup
# from PIL import Image

class SupplierPageGetter(ProductPageGetter):

    APP_PATH = Path(__file__).parent

    def search(self, sku: str, *args) -> str | None:
        
        '''
        You are given the Product Code / sku
        args[0] holds the Product Title

        Define how the program will find the link
        to the Product's page if it's not provided
        For example:

        import requests
        search_api_url = 'https://www.suppliersite.com/search_handler?query={}'
        resp = requests.get(search_api_url.format(sku))
        results = resp.json()['Products']
        if results:
            return results[0]['product_page_url']
        else:
            return None


        return the url string if found
        return None if not found
        '''
        url = ''
        if url:
            return url
        else:
            return None

    def parse_html(self, html_page: str, *args) -> list[str]:
        '''
        The html_page parameter holds the html markup of
        the Product's page as a string.

        Define how the program will find the correct
        image links. An easy way to do it is using 
        BeautifulSoup. Example:

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_page, features='html.parser')
        elements = soup.select(div.slider a)
        links = [element.get('href') for element in elements]
        return links

        return a list of url strings if images exist
        return an empty list if images don't exist
        '''
        links = []
        return links


class SupplierImageDownloader(ImageDownloader):

    def transform_image(self, image: bytes, filename: str) -> bytes:
        '''
        Warning: Currently the program supports only
        concurrency through the threading module as
        it's a good way to improve network IO performance
        but the transformations will be single threaded
        due to the GIL

        The image parameter holds the downloaded image
        as if getting the requests.Response.content
        attribute.
        For example:

        from PIL import Image
        from io import BytesIO
        
        ext = filename.strip().split('.')[-1]
        if ext == 'jpg': ext == 'jpeg'

        im = Image.open(BytesIO(image))
        ...
        ... your transformation code here
        ...
        with io.Bytes() as buffer:
            im.save(buffer)
            buffer.seek(0)
            return buffer.read()


        Apply a transformation to the image and return
        the bytes.
        '''
        return image


def main():
    ws = WorksheetImporter(supplier_path=supplier_path).worksheet
    SupplierPageGetter(ws, 'Title', 'ProductCode', 'ProductURL', supplier_path=supplier_path).run()     # Make sure to define the correct column names.
    ImageDownloader(supplier_path=supplier_path).run()
    ic = IntegrityChecker(log=True, supplier_path=supplier_path)
    Archiver(supplier_path, 'SupplierName', ic).run()                                                   # Change SupplierName to something more appropriate.


if __name__ == '__main__':
    main()
