import pathlib
import threading
import requests
import pprint
from typing import TextIO

class ImageDownloader:

    def __init__(self, supplier_path: pathlib.Path) -> None:
        self.APP_PATH = supplier_path
        self.links_file = (self.APP_PATH / 'links.txt')
        self.out_dir = self.APP_PATH / 'images'
        self.existing_images: set[str] = {file.name for file in self.out_dir.iterdir()}
        self.links_IO: TextIO

    def run(self) -> None:
        self.links_IO = self.links_file.open()
        queue: list[tuple[str, str]] = []
        current_sku = ''
        for line in self.links_IO:
            line = line.strip()
            if not line: continue

            filename, url = line.split('|')
            sku, _ = filename.split('_')

            if sku != current_sku:
                self.download(queue)
                current_sku = sku
                queue.clear()

            queue.append((filename, url))


    def download(self, chunk: list[tuple[str, str]]) -> None:
        if not chunk: return
        threads = [threading.Thread(target=self.download_item, args=(item,)) for item in chunk]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def download_item(self, item: tuple[str, str]):
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
            log['timeout'] = True
        except requests.HTTPError as e:
            pass
        except Exception as e:
            log['reason'] = repr(e)
        finally:
            if log['success']:
                out_path = self.out_dir / filename
                with out_path.open('wb') as f: f.write(self.transform_image(resp.content, filename))
                print(log)
            else:
                failed_image = self.out_dir / f"{'Failed_log'}-{filename}.txt"
                with failed_image.open('w') as log_file:
                    log_file.write(pprint.pformat(log))
                print(f"Failed to download image {url}. Check {str(failed_image)} for info")


    def transform_image(self, image: bytes, filename: str) -> bytes:
        return image
