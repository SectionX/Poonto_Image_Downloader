"""
Utility functions
"""


import pathlib
from enum import Enum
from zipfile import ZipFile
from datetime import datetime

from PIL import Image

class Integrity(Enum):
    """
    Enumerator to be used with IntegrityChecker
    """
    BOTH = 1
    DOWNLOAD = 2
    IMAGE = 3

class IntegrityChecker():
    """
    Checks downloaded images for integrity, failed requests and other issues.
    """

    def __init__(self, supplier_path: pathlib.Path,
                 mode: Integrity = Integrity.BOTH,
                 log = False):

        self.app_path = supplier_path
        self.image_path = self.app_path / 'images'
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
            except OSError as e:
                self.integrity_check_passed = False
                self.failed_files.append(
                    {'name': file.name, 'reason': f'Integrity Check Failed, {e}'}
                )


        match mode:
            case Integrity.BOTH: self.result = self.integrity_check_passed and \
                                               self.download_check_passed
            case Integrity.DOWNLOAD: self.result = self.download_check_passed
            case Integrity.IMAGE: self.result = self.integrity_check_passed
        if log:
            self.write_to_log()

    def write_to_log(self):
        """
        Logs the result to notify the client.
        """

        with (self.app_path / 'integrity_log.txt').open('w') as f:
            f.writelines(str(item)+'\n' for item in self.failed_files)

    def __bool__(self):
        return self.result

    def __repr__(self):
        return f'IntegrityChecker({self.result})'


class Archiver:
    '''
    Handles archiving for downloaded images and logs.
    '''

    def __init__(self,
                 supplier_path: pathlib.Path,
                 name: str = ..., # type: ignore
                 integrity: bool | IntegrityChecker = ... # type: ignore
                ):

        self.app_path = supplier_path
        self.image_path = self.app_path / 'images'
        self.time: str = datetime.now().strftime('%Y%m%d')
        self.files = self.image_path.iterdir()
        self.log_files = ['integrity_log.txt', 'logs.txt', 'links.txt']
        self.name = 'ImageArchive' if name is Ellipsis else name
        self.integrity = bool(integrity)
        self.zip_name = str(self.app_path / f'{self.name}-{self.time}.zip')


    def run(self):
        """
        The API of the class
        """

        if not self.integrity:
            print('The integrity check failed. \
                  Check the integrity_log.txt for issues or override the integrity check')
            return
        self.make_archive()


    def make_archive(self):
        """
        Turns the images to a .zip file for easier transmission.
        """

        with ZipFile(self.zip_name, 'w') as zipfile:

            for file in self.files:
                zipfile.write(str(file), file.name)

            for filename in self.log_files:
                file = self.app_path / filename
                zipfile.write(str(file), file.name)


def archive_data(supplier_path: pathlib.Path) -> None:
    '''
    Archives the old worksheets. Doesn't hold long records. Calling it twice deletes everything.
    '''
    data_path = supplier_path / 'data'
    archive_path = supplier_path / 'data.old'

    data_path.replace(archive_path)
    data_path.mkdir()
    return None


def show_logs(supplier_path: pathlib.Path) -> str:
    '''
    Returns the contents of the logs.txt file to the client.
    '''
    log_path = supplier_path / 'logs.txt'
    try:
        with log_path.open() as f:
            return f.read()
    except IOError as e:
        return f'{e}, Logs not found for supplier {supplier_path.name}'


def show_image_links(supplier_path: pathlib.Path) -> str:
    '''
    Returns text with filename|image_url pairs to the client if links.txt exists.
    Otherwise notifies the client.
    '''
    link_path = supplier_path / 'links.txt'
    try:
        with link_path.open() as f:
            return f.read()
    except IOError as e:
        return f'Links file not found for supplier {supplier_path.name}, {e}'


def check_process() -> str:
    """
    Arguments 'supplier_path: pathlib.Path'
    Checks if the Downloader process and returns the appropriate message.
    """
    return 'Not Implemented Yet'
    