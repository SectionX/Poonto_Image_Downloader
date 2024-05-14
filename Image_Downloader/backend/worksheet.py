#!/usr/bin/python

'''
Handles file IO for the downloader.
'''

import os
import pathlib
import sys
import tkinter as tk

import pandas as pd

class Msgbox(tk.Tk):
    '''
    Provides a simple GUI interface for file IO.
    '''

    selection: str

    def __init__(self):
        super().__init__()
        self.geometry('400x100')
        self.title = 'Msgbox'

    def alert(self, message):
        '''Throws a message box explaining the issue'''
        label = tk.Label(self, text=message)
        label.pack()
        self.mainloop()
        label.destroy()

    def _get_selection(self, selection):
        self.selection = selection
        self.quit()

    def select(self, *items):
        '''Provides a GUI interface to choose a file from a list'''
        frame = tk.Frame(self)
        copied_items = []
        for item in items:
            copied_items.append(item)
            button = tk.Button(frame, text=item.split(os.sep)[-1],
                               command=lambda: self._get_selection(copied_items[-1]))
            button.pack()
        frame.pack()
        self.mainloop()
        frame.destroy()
        return self.selection


class WorksheetImporter:
    '''
    Handles IO for excel files.
    '''


    def __init__(self, supplier_path: pathlib.Path):
        self.worksheet: pd.DataFrame
        self.msgbox = Msgbox()
        self.basedir = supplier_path
        self.read_excel = lambda x: pd.read_excel(x, dtype=object)
        # Try to get file from argv
        if len(sys.argv) == 2:
            try:
                self.worksheet = self.read_excel(sys.argv[1])
            except IOError as e:
                print(e)
                self.msgbox.alert("File isn't recognized as valid worksheet\n" + sys.argv[1])
                sys.exit(1)
        # Try to get file from data dir
        else:
            data_path = pathlib.Path(self.basedir / 'data').absolute()
            files = [*data_path.iterdir()]

            if len(files) == 0:
                print("No worksheets found in data directory")
                self.msgbox.alert("No worksheets found in data directory")
                sys.exit(1)
            elif len(files) == 1:
                self.worksheet = self.read_excel(files[0].absolute().__str__())
            else:
                print("Please select a file")
                self.worksheet = self.read_excel(self.msgbox.select(*[str(file) for file in files]))
