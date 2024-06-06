'''
Downloads images the images as marked on a links.txt
'''

import pathlib
import threading
import pprint
from abc import abstractmethod
from typing import TextIO

import requests

class ImageDownloader:

    '''
    Class to be used on supplier scripts. Downloads the images
    and allows the caller to define a method that applies a
    transformation to the image before saving.
    '''

    def __init__(self, supplier_path: pathlib.Path) -> None:
        self.app_path = supplier_path
        self.links_file = self.app_path / 'links.txt'
        self.out_dir = self.app_path / 'images'
        if not self.out_dir.exists():
            self.out_dir.mkdir()
        self.existing_images: set[str] = {file.name for file in self.out_dir.iterdir()}
        self.links_io: TextIO

    def run(self) -> None:
        '''
        The class' high level API
        '''
        self.links_io = self.links_file.open()
        queue: list[tuple[str, str]] = []
        current_sku = ''
        for line in self.links_io:
            line = line.strip()
            if not line:
                continue

            filename, url = line.split('|')
            sku, _ = filename.split('_')

            if sku != current_sku:
                self._download(queue)
                current_sku = sku
                queue.clear()

            queue.append((filename, url))


    def _download(self, chunk: list[tuple[str, str]]) -> None:
        if not chunk:
            return
        threads = [threading.Thread(target=self._download_item, args=(item,)) for item in chunk]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def _download_item(self, item: tuple[str, str]):
        filename, url = item
        if filename in self.existing_images:
            print(f'Image {filename} already exists')
            return

        log = {}
        log['success'] = False
        log['filename'] = filename
        log['url'] = url
        log['status_code'] = None
        log['timeout'] = False
        log['reason'] = 'Ok'
        try:
            resp = requests.get(url, timeout=10)
            log['status_code'] = resp.status_code
            log['reason'] = resp.reason
            resp.raise_for_status()
            log['success'] = True
        except requests.Timeout as e:
            e.add_note('time out')
            log['timeout'] = True
        except requests.HTTPError as e:
            e.add_note('http error')
        finally:
            if log['success']:
                out_path = self.out_dir / filename
                with out_path.open('wb') as f:
                    f.write(self.transform_image(resp.content, filename))
                print(log)
            else:
                failed_image = self.out_dir / f"{'Failed_log'}-{filename}.txt"
                with failed_image.open('w') as log_file:
                    log_file.write(pprint.pformat(log))
                print(f"Failed to download image {url}. Check {str(failed_image)} for info")

    @abstractmethod
    def transform_image(self, image: bytes, filename: str) -> bytes:
        '''
        Interface method to be defined in the supplier __main__
        '''
        return image
