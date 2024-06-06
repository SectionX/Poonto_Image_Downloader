
"""
Provides high level functions to resolve API calls
"""

import subprocess as sp
import pathlib
import sys
from typing import Any
from threading import Thread

import dotenv

from .backend.utils import archive_data
from .backend.utils import show_logs
from .backend.utils import show_image_links
from .backend.utils import check_process
from .backend.exports import export_images


with open(dotenv.find_dotenv(), encoding='utf8') as configfile:
    env = dotenv.dotenv_values(stream=configfile)



def find_path(supplier) -> pathlib.Path:

    """
    Resolves the path of the Supplier's script
    """

    supplier_dir = env.get('suppliers_dir')
    if supplier_dir is None:
        print('config.json must define supplier_dir')
        sys.exit(1)
    else:
        path = pathlib.Path.cwd() / 'Image_Downloader' / supplier_dir / supplier

    supplier_path = path
    return supplier_path


def show_actions(message: str = '') -> dict[str, str]:
    """
    Returns a help message
    """

    return {
        'message': f'Help Message. {message}',
        'main': 'GET | Run the ImageDownloader',
        'main_no_dl': 'GET | Run the ImageDownloader but only find the image links',
        'import_data_file': 'POST | Send and Excel, CSV, or XML file to \
                            the application holding information about products',
        'export_images': 'GET | Download a zip file with the images',
        'check_logs': 'GET | See the logs for the last run',
        'get_image_links': 'GET | Get a file with sku-link pairs',
        'check_process': 'GET | Check the status of the current ImageDownloader process',
    }

def create_process(path, *args) -> sp.Popen:
    """
    Spawns the process requested by the API
    """
    with sp.Popen(['python', str(path), *args], stdout=sys.stdout) as process:
        return process


def controller(supplier: str, action: str, user: str | None) -> Any:

    """
    Parses the request and returns the appropriate response
    """
    path = find_path(supplier)
    response: Any = None
    try:
        match action:
            case 'main'             : response = create_process(path)
            case 'main_no_dl'       : response = create_process(path, '--links-only')
            case 'import_data_file' : archive_data(path)
            case 'export_images'    : export_images() #parameters -> path
            case 'check_logs'       : response = show_logs(path)
            case 'get_image_links'  : response = show_image_links(path)
            case 'check_process'    : response = check_process() #parameters -> path
            case 'help'             : response = show_actions()
            case _                  : response = show_actions('Bad Action')
        return response
    finally:
        with open('logs.txt', 'a', encoding='utf8') as f:
            f.write(f"{action = }, {supplier = }, {user = }\n")


def parse():
    '''
    Parses the request and returns a dict for the controller to read.
    Accepts Request and returns dict[str, Any]
    '''
