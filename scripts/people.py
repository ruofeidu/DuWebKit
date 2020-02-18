"""Paper defines a paper manager.

This class allows the user process papers in batch.
"""
import re
import json
import htmlmin
import logging
from markdown import markdown
from scripts.data import Data
from scripts.person import Person
from scripts.utils.utils import Utils
from scripts.utils.constants import DEBUG_HTML_SCRIPT
import logging
from datetime import datetime
import operator


class People:
  __slots__ = ('_data', '_keys', '_last_dict')
  _count = 0

  def __init__(self, rows):
    # pid -> Person.
    self._data = {}

    # pid list.
    self._keys = []

    # A dict of dict of list, indexed by last names, followed by first names.
    self._last_dict = {}

    if not rows:
      logging.error('No people sheet in gSheet was found.')
      return
    else:
      logging.info(rows[0])

    Person.set_header(rows[0])
    People._count = len(rows)
    for i in range(1, len(rows)):
      p = Person(rows[i])
      self._add_person(p)
    pass

  # Makes a backup for the input data.
  def backup(self):
    self._export_json('json/people.json')
    self._export_people_names('debug/names.txt')
    self.export_html('debug/people.html')
    # Verifies if duplicates exist.
    duplicates = set()
    for k in self._keys:
      d = self._data[k]
      name = d.get_full_name_with_marks()
      if name in duplicates:
        logging.warn('Duplicated: ', name)
      duplicates.add(name)
    # Examines birthdays.
    birthday_list = []
    for k in self._keys:
      person = self._data[k]
      diff = person.get_birthday_to_today()
      if -7 <= diff <= 15:
        birthday_list.append(
            (person.get_name(), person.get_birthday_str(), diff))
    birthday_list.sort(key=operator.itemgetter(2))
    print('========= Happy Birthday =========')
    for item in birthday_list:
      print(item[0], item[1], item[2])
    print('========= Awesome Birthday =========')

  # Returns the person with first name (may contains middle name) and
  # the last name.
  def query_first_last(self, first, last, allow_middle=True):
    if last in self._last_dict:
      if first in self._last_dict[last]:
        return self._last_dict[last][first][0]
      p = first.find(' ')
      if allow_middle and p > 0:
        first = first[:p]
        if first in self._last_dict[last]:
          return self._last_dict[last][first][0]
    return None

  def _add_to_last_dict(self, p):
    """Adds a Person to the last dict."""
    first, last = p.get_first(), p.get_last()
    if last not in self._last_dict:
      self._last_dict[last] = {}
    if first not in self._last_dict[last]:
      self._last_dict[last][first] = [p]
    else:
      self._last_dict[last][first].append(p)

  def _add_person(self, p):
    """Adds a Person to self."""
    self._add_to_last_dict(p)
    pid = p.get_pid()
    self._data[pid] = p
    self._keys.append(pid)
    Data.pids.add(pid)

  def add_person(self, first, last):
    """Adds a Person with first and last names."""
    p = Person(['', first, last])
    self._add_person(p)
    return p

  def to_json(self):
    """Converts to JSON."""
    _dict = {}
    for pid in self._keys:
      _dict[pid] = self._data[pid].to_dict()

    return json.dumps({'_data': _dict, '_keys': self._keys}, indent=2)

  def _export_json(self, filename):
    Utils.write_file(filename, self.to_json())

  def _export_people_names(self, filename):
    Utils.set_to_print_file()
    s = ''
    for k in self._keys:
      s += self._data[k].get_name()
      s += Utils.get_line_break()
    Utils.write_file(filename, s)

  # Exports an HTML file in the debug/ folder.
  def export_html(self, filename):
    Utils.set_to_print_web()
    s = ''
    for k in self._keys:
      d = self._data[k]
      s += d.get_name_google_markdown()
      if d.get_original_name():
        s += ' (%s)' % d.get_original_name()
      s += ': '
      s += Utils.get_line_break()
      s += d.get_best_face_markdown()
      s += Utils.get_line_break()
      s += ' '.join([
          d.get_website_markdown(),
          d.get_facebook_markdown(),
          d.get_twitter_markdown(),
          d.get_vimeo_markdown(),
          d.get_linkedin_markdown(),
          d.get_instagram_markdown(),
          d.get_youtube_markdown(),
          d.get_github_markdown(),
          d.get_researchgate_markdown(),
          d.get_scholar_markdown()
      ])
      s += Utils.get_separator()
    s += DEBUG_HTML_SCRIPT
    s = htmlmin.minify(markdown(s))
    Utils.write_file(filename, s)

  def download_photos(self, check_existing=True):
    self._download_scholar_photos()
    self._download_website_photos()

  def _download_website_photos(self, check_existing=True):
    for k in self._keys:
      d = self._data[k]
      if check_existing and d.check_website_photo_existed():
        continue
      d.download_website_photo()

  def _download_scholar_photos(self, check_existing=True):
    for k in self._keys:
      d = self._data[k]
      if check_existing and d.check_scholar_photo_existed():
        continue
      d.download_scholar_photo()

  def _download_linkedin_photos(self, check_existing=True):
    for k in self._keys:
      d = self._data[k]
      if check_existing and d.check_linkedin_photo_existed():
        continue
      d.download_linkedin_photo()

  @staticmethod
  def count():
    return People._count
