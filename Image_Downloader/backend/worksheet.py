#!/usr/bin/python

'''
Handles file IO for the downloader.
'''

import pathlib
import sys
from tkinter.filedialog import askopenfilename
import pandas as pd

class WorksheetImporter:
    '''
    Handles IO for excel files.
    '''


    def __init__(self, supplier_path: pathlib.Path):
        self.worksheet: pd.DataFrame
        self.basedir = supplier_path
        self.read_excel = lambda x: pd.read_excel(x, dtype=object)
        # Try to get file from argv
        if len(sys.argv) == 3:
            try:
                self.worksheet = self.read_excel(sys.argv[2])
            except IOError as e:
                print(e)
                sys.exit(1)
        # Try to get file from data dir
        else:
            data_path = pathlib.Path(self.basedir / 'data').absolute()
            files = [*data_path.iterdir()]

            if len(files) == 0:
                print("No worksheets found in data directory")
                sys.exit(1)
            elif len(files) == 1:
                self.worksheet = self.read_excel(files[0].absolute().__str__())
            else:
                print("Please select a file")
                self.worksheet = self.read_excel(askopenfilename(title="Please select a file", initialdir=str(data_path)))
