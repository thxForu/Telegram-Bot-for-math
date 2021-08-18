import time
from bot import clean_collections

while True:
    clean_collections()
    time.sleep(86400)