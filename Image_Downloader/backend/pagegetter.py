'''
This module handles scrapping of image links from product pages. It exposes an interface for the
unique supplier scripts to handle html parsing.
'''

import os
import pathlib
import sys
import pickle
from urllib.parse import urlparse
from abc import abstractmethod

import pandas as pd
import requests

class ProductPageGetter:
    '''
    Purpose:
    Provide a pandas.DataFrame object and provide the column names for the 
    Product Title, Product Code (sku) and Product Page URL.

    Alternatively you can use the WorksheetImporter which handles Input for you.
    It supports 
    1. CLI arguments, like python downloader.py myworksheet.xlsx
    2. Drag & Drop, Drop the worksheet file on the executable.
    3. If argument input is given, it searches the data directory 
       and either loads a the worksheet or asks you to choose if it finds more than one.

    This program does not download images. It will only output a file with filename|url pairs
    to feed into another program. 


    Usage: 
    Create a class that inherits from ProductPageGetter and call the run() function. 
    The object will download all product pages and save them to .cache directory.
    The cache is eternal, so if you think that the data in pages have changed, 
    delete the contents of the .cache dir.
    Products with invalid URLs are logged in logs.txt

    
    You can define the following functions:
    
    def parse_html(self, html: str) -> list[str]

    Use this function to define how the program will find the image URLs from the HTML markup.
    The program will log the results in a PIPE seperated format {sku}_{i}.{ext}|{image_url}
    bs4.BeautifulSoup is recommended but not enforced.
    Return a list of the image urls as a list of strings.


    def search(self, url, *args) -> str | None

    Use this function to define how the program will find the Product Page URL if you 
    don\'t know it or the one you have is invalid. If you are using a file, make sure 
    to instantiate it as a class property,
    because the function is called for every product.

    To handle unfound/invalid links, return None


    def fix_title(self, title: str) -> str

    The program uses the title as a name for the cached results. If your title contains characters
    that can be used as filenames by the OS, you can use this to replace the invalid characters
    
    By default it only changes the '/' character to '---'.
    '''

    def __init__(self, worksheet: pd.DataFrame,
                 supplier_path: pathlib.Path,
                 *tablenames: str,
                 failed_only: bool = False):


        title_column, sku_column, url_column = tablenames

        self.app_path = supplier_path
        self.cache_path: pathlib.Path = self.app_path / '.cache'
        if not self.cache_path.exists():
            self.cache_path.mkdir()
        self.cached_files: list[str] = [
            str(x).rsplit(os.sep, maxsplit=1)[-1] for
            x in  self.cache_path.iterdir()
        ]
        self.no_of_parallel_connections: int = 4
        self.not_found = []


        self.df: pd.DataFrame = worksheet
        self.url_table: pd.DataFrame = worksheet[[title_column, sku_column, url_column]]
        self.failed_only = failed_only

        log_file = self.app_path / 'logs.txt'
        skus_in_log = []
        if failed_only and log_file.exists():
            with log_file.open() as f:
                for line in f:
                    _, _, sku, *_ = line.strip().split(' - ')
                    skus_in_log.append(sku.strip())

            if skus_in_log:
                self.url_table.index = pd.Index(self.url_table[sku_column])
                self.url_table = self.url_table.loc[skus_in_log]


    def run(self):
        '''
        The high level API to be used in supplied scripts.
        '''
        self.url_table.fillna('', inplace=True)
        print(f'Found {len(self.url_table)} products.\nDownloading...')

        with (
            (self.app_path / 'logs.txt').open('w') as log_file,
            (self.app_path / 'links.txt').open('a' if self.failed_only else 'w') as links_file
        ):

            for i, row in self.url_table.iterrows():
                title, sku, url = row
                resp = self._request_page(title, sku, url)
                if not resp:
                    log_file.write(f'Failed - No Product Page Found - \
                                    {sku} - {title} - URL:{url}\n')
                else:
                    image_links: list[str] = self.parse_html(resp.text)
                    if len(image_links) == 0:
                        log_file.write(f'Failed - No Images Found - \
                                        {sku} - {title} - URL:{resp.url}\n')
                    for i, link in enumerate(image_links):
                        if '.' in link:
                            *_, ext = link.split('.')
                        else:
                            ext = 'jpg'
                        entry = f'{sku}_{i}.{ext}|{link}'
                        print(entry)
                        links_file.write(entry+'\n')


    def _is_cached(self, title: str) -> bool:
        return title in self.cached_files

    def _add_to_cache(self, title: str, obj: requests.Response):
        with (self.cache_path / title).open('wb') as f:
            pickle.dump(obj, f)

    def _retrieve_from_cache(self, title, sku):
        print(f'Retrieving {sku} - {title} page from Cache')
        with (self.cache_path / title).open('rb') as f:
            return pickle.load(f)

    def _is_valid_url(self, url: str):
        parse_result = urlparse(url)
        if parse_result.scheme not in ['http', 'https']:
            return False
        if not parse_result.netloc:
            return False
        return True


    def fix_title(self, title: str) -> str:
        '''
        Interface method to be used in supplier's __main__. 
        Removes invalid characters from future filenames.
        '''
        if '/' in title:
            title = title.replace('/', '---')
        return title

    def _request_page(self, title: str, sku: str, product_url: str) -> requests.Response | None:
        title = self.fix_title(title)


        is_cached = self._is_cached(title)
        resp: requests.Response
        interrupt = False


        if not is_cached and not self._is_valid_url(product_url):
            url: str | None = self.search(sku)
            if url is None:
                self.not_found.append(f'Not Found: {sku} - {title}')
                return None
            if url:
                if self._is_valid_url(url):
                    product_url = url

        try:
            if is_cached:
                resp = self._retrieve_from_cache(title, sku)
            else:
                print(f'Requesting page {product_url}')
                resp = requests.get(product_url, timeout=10)
                resp.raise_for_status()
                message = f'Request for page {sku} - {title} successful'
                print(message)

        except requests.HTTPError as e:
            message = f'{e} Failed to get page for {title} - {sku}. \
                        GET Request return status {resp.status_code}'
            print(message)

        except requests.Timeout as e:
            message = f'{e} Failed to get page for {title} - {sku}. \
                        Connection timed out'
            print(message)

        finally:
            if resp and resp.status_code == 200 and not is_cached:
                self._add_to_cache(title, resp)
                print(f'Added {sku} - {title} to cache')
            if interrupt:
                sys.exit(2)

        return resp

    @abstractmethod
    def parse_html(self, html_page, *args) -> list[str]:
        '''
        Abstract method to be used in supplier's __main__
        '''

    @abstractmethod
    def search(self, sku, *args) -> str | None:
        '''
        Abstract method to be used in supplier's __main__
        '''
