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
        if isinstance(supplier_path, str):
            self.supplier_path = Path(supplier_path)
        elif isinstance(supplier_path, Path):
            self.supplier_path = supplier_path
        else:
            error = TypeError()
            error.add_note('supplier_path must be Path or str')
            raise error

        # Initialize the product file
        self.data_path: Path = self.supplier_path / 'data'
        if filename:
            if isinstance(filename, TextIOWrapper):
                self.file_contents = filename.read()
                filename.close()
            elif isinstance(filename, str):
                with open(filename, encoding='utf8') as f:
                    self.file_contents = f.read()
            else:
                error = TypeError()
                error.add_note('filename must be TextIOWrapper or str')
                raise error            
        else:
            if len(sys.argv) >= 2:
                with open(sys.argv[1], encoding='utf8') as f:
                    self.file_contents = f.read()
            else:
                files = [*self.data_path.iterdir()]
                if len(files) == 1:
                    with open(files[0], 'rb') as f:
                        self.file_contents = f.read()
                else:
                    error = ValueError()
                    error.add_note('Filename can only be None if there exists an \
                                   argument vector or there is a single file in data directory')
                    raise error

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
