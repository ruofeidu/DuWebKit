"""DuWebsite builds personal websites by parsing metadata from Google Sheets, Markdown, and JSON.

DuWebsite offers an universial solution to parse papers, people, and addresses, thereafter builds a personal website in HTML.
"""
import os
import re
import json
import markdown
import time
import logging
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
  logging.basicConfig(filename='duweb.log', level=logging.WARNING)

  logging.info('Initializing DuWebsite...', flush=True)
  compiler = Compiler()
  sync = Sync()
  logging.info('Initialization completed. Time used %.2f.' %
               (time.time() - _build_time))

  # Synchronizes the data.
  if App.sync_gsheets:
    run_time = time.time()
    print('Synchronizing with gSheets...', flush=True, end="\r")
    sync.run()
    print('Synchronizing completed. Time used %.2f.' % (time.time() - run_time))

  # Builds the website.
  print('Compiling...', flush=True, end="\r")
  run_time = time.time()
  cite_template_filename = os.path.join(Dir.templates, Dir.cites, 'cite.html')
  Data.papers.export_cites_html(cite_template_filename)
  for build_file in Data.build_files:
    compiler.compile(build_file, write_to_file=True)
  print('Compile completed. Time used %.2f.' % (time.time() - run_time))
  Data.ready_to_destroy = True

  # Backs up the data.
  if App.backup_data:
    run_time = time.time()
    print('Backing up...', flush=True, end="\r")
    Data.papers.backup()
    Data.people.backup()
    print('Backup completed. Time used %.2f.' % (time.time() - run_time))

  print("Done! %d papers rendered. Time used %.2fs at %s. Have a great day!" %
        (Data.papers.count(), time.time() - _build_time,
         datetime.now().strftime('%H:%M')))
