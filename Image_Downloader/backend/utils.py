import pathlib
from PIL import Image
from typing import Literal
from enum import Enum
from zipfile import ZipFile
from datetime import datetime


class integrity(Enum):
    BOTH = 1
    DOWNLOAD = 2
    IMAGE = 3

class IntegrityChecker():
    
    
    def __init__(self, supplier_path: pathlib.Path, mode: Literal[integrity.BOTH, integrity.DOWNLOAD, integrity.IMAGE] = integrity.BOTH, log = False):

        self.APP_PATH = supplier_path
        self.image_path = self.APP_PATH / 'images'
        self.files = self.image_path.iterdir()
        self.failed_files = []
        self.integrity_check_passed = True
        self.download_check_passed = True

        for file in self.files:

            #check if downloaded
            if file.name.startswith('Failed'):
                self.download_check_passed = False
                with file.open() as f:
                    self.failed_files.append({'name': file.name, 'reason': f.read()})
                

            #check integrity
            try:
                image = Image.open(file)
                image.verify()
            except:
                self.integrity_check_passed = False
                self.failed_files.append({'name': file.name, 'reason': 'Integrity Check Failed'})


        match mode:
            case integrity.BOTH: self.result = self.integrity_check_passed and self.download_check_passed
            case integrity.DOWNLOAD: self.result = self.download_check_passed
            case integrity.IMAGE: self.result = self.integrity_check_passed
        if log:
            self.write_to_log()

    def write_to_log(self):
        with (self.APP_PATH / 'integrity_log.txt').open('w') as f:
            f.writelines(str(item)+'\n' for item in self.failed_files)

    def __bool__(self):
        return self.result

    def __repr__(self):
        return f'IntegrityChecker({self.result})'
    

class Archiver:

    def __init__(self, supplier_path: pathlib.Path, name: str = ..., integrity: bool | IntegrityChecker = ...):
        self.APP_PATH = supplier_path
        self.image_path = self.APP_PATH / 'images'
        self.time: str = datetime.now().strftime('%Y%m%d')
        self.files = self.image_path.iterdir()
        self.log_files = ['integrity_log.txt', 'logs.txt', 'links.txt']
        self.name = 'ImageArchive' if name is Ellipsis else name
        self.integrity = bool(integrity)
        self.zip_name = str(self.APP_PATH / f'{self.name}-{self.time}.zip')

    def run(self):
        if not self.integrity:
            print('The integrity check failed. Check the integrity_log.txt for issues or override the integrity check')
            return
        self.make_archive()

    def make_archive(self):
        zip = ZipFile(self.zip_name, 'w')

        for file in self.files: 
            zip.write(str(file), file.name)

        for filename in self.log_files:
            file = self.APP_PATH / filename
            zip.write(str(file), file.name)
        zip.close()