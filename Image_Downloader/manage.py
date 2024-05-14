import subprocess as sp
import dotenv
import pathlib
import threading
import time
import sys
from hashlib import sha256
from base64 import b64encode
print(b64encode(sha256('1amalakagt'.encode()).digest()).decode())

with open(dotenv.find_dotenv()) as f:
    env = dotenv.dotenv_values(stream=f)


print(env)  

def create_process(supplier: str):
    path = pathlib.Path.cwd() / 'Image_Downloader' / env['suppliers_dir'] / supplier
    print(path)
    process = sp.Popen(['python', str(path)], stdout=sys.stdout)
    return process


process = create_process('estia')
print('Hello')
time.sleep(10)
process.kill()
print(process.returncode)
