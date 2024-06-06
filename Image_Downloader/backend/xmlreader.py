'''
Searches image links in Product pages.
'''

import sys
from io import TextIOWrapper
from pathlib import Path
from abc import abstractmethod

import pandas as pd

class XmlReader:
    '''
    Handles XML files and either turns them in 
    dataframes, or just dumps the links in links.txt
    '''

    def __init__(self, supplier_path: str | Path,
                 product_node: str,
                 filename: TextIOWrapper | str | None):

        # Initialize supplier_path
        self.supplier_path = supplier_path
        self.filename = filename

        if len(sys.argv) == 3:
            with open(sys.argv[2], encoding='utf8') as f:
                self.file_contents = f.read()
        self.product_node = product_node
        self.worksheet: pd.DataFrame | None = None
        self.create_worksheet(self.file_contents, self.product_node)
        self.create_links_txt(self.file_contents, self.product_node)

    @abstractmethod
    def create_worksheet(self, file_contents, product_node) -> None:
        '''
        Abstract method that defines how the worksheet is created
        from an XML file. Only one of those needs to be defined.
        '''

    @abstractmethod
    def create_links_txt(self, file_contents, product_node) -> None:
        '''
        Abstract method that defines how the links.txt is created
        from an XML file. Only one of those needs to be defined.
        '''



if __name__ == '__main__':
    reader = XmlReader('asdf', 'Product', 'Image_Downloader/artelibre/data')
