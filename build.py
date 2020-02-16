"""DuWebsite builds personal websites by parsing metadata from Google Sheets, Markdown, and JSON.

DuWebsite offers an universial solution to parse papers, people, and addresses, thereafter builds a personal website in HTML.
"""
import os
import re
import json
import markdown
import time
from datetime import datetime
from scripts.papers import Papers
from scripts.people import People
from scripts.data import Data
from scripts.templates import Templates
from scripts.app import App
from scripts.sync import Sync
from scripts.compiler import Compiler
from scripts.utils.dir import Dir

if __name__ == "__main__":
  _build_time = time.time()
  print('Initializing DuWebsite...', flush=True)
  compiler = Compiler()
  sync = Sync()
  print('Initialization completed. Time used %.2f.' %
        (time.time() - _build_time))

  # Synchronizes the data.
  if App.sync_gsheets:
    run_time = time.time()
    print('Synchronizing with gSheets...', flush=True)
    sync.run()
    print('Synchronizing completed. Time used %.2f.' % (time.time() - run_time))

  # Downloads the scholar photos.
  if App.download_photos:
    run_time = time.time()
    print('Downloading scholar photos...', flush=True)
    Data.people.download_photos()
    print('Downloading completed. Time used %.2f.' % (time.time() - run_time))

  # Builds the website.
  run_time = time.time()
  cite_template_filename = os.path.join(Dir.templates, Dir.cites, 'cite.html')
  Data.papers.export_cites_html(cite_template_filename)
  compiler.compile('index.html', True)
  compiler.compile('papers/index.html', True)
  compiler.compile('arts/index.html', True)
  print('Compile completed. Time used %.2f.' % (time.time() - run_time))

  # Backs up the data.
  if App.backup_data:
    run_time = time.time()
    print('Backup...', flush=True)
    Data.papers.backup()
    Data.people.backup()
    print('Backup completed. Time used %.2f.' % (time.time() - run_time))

  print("Done! %d papers rendered. Time used %.2fs at %s. Have a great day!" %
        (Data.papers.count(), time.time() - _build_time,
         datetime.now().strftime('%H:%M')))
