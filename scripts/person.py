"""Person defines a person with his cooresponding properties.

This class allows a person to get names.
"""
import re
import os
import json
from scripts.utils.dumark import DuMark
from scripts.data import Data
from scripts.utils.ducrawler import DuCrawler
from scripts.utils.constants import SCHOLAR_PHOTO_LOCAL, SCHOLAR_PHOTO_URL, WEBSITE_PHOTO_LOCAL
from datetime import datetime
import datetime

re_birthday = re.compile('(\d+)\/(\d+)\/\d+')


class Person:
  __slots__ = ('_data')

  def __init__(self, row):
    # type: (self, list(str)) -> None
    self._data = {}
    b = self._data
    for i, label in enumerate(Person.get_header()):
      b[label] = row[i] if i < len(row) else ''

    if not ('pid' in b and b['pid'] and not Data.has_pid(b['pid'])):
      i, suffix = 1, ''
      while True:
        pid = row[2].lower() + row[1].lower() + suffix
        if not Data.has_pid(pid):
          b['pid'] = pid
          break
        i += 1
        suffix = str(i)

  def __str__(self):
    return '%s %s' % (self._data['first'], self._data['last'])

  def get_name_markdown(self):
    if 'web' in self._data and self._data['web'] and not self.is_me():
      return DuMark.get_website(self._data['web'], str(self))
    else:
      return str(self)

  def to_json(self):
    return json.dumps({'_data': self._data})

  def to_dict(self):
    return self._data

  def get_bib(self):
    return '%s, %s' % (self._data['last'], self._data['first'])

  def set_name(self, first, last):
    self._data = {'first': first, 'last': last}

  def get_last(self):
    return self._data['last']

  def get_first(self):
    return self._data['first']

  def get_middle(self):
    return self._data['middle']

  def get_pid(self):
    return self._data['pid']

  def get_first_name(self):
    return self.get_first()

  def get_last_name(self):
    return self.get_last()

  def get_middle_name(self):
    return self.get_middle()

  def get_initials(self):
    initials = self.get_first()[0] + '.'
    if self.get_middle() and not self.get_middle()[0].isdigit():
      initials += '.' + self.get_middle() + '.'
    return initials

  def get_apa(self):
    return self.get_last() + ', ' + self.get_initials()

  def get_mla(self):
    return self.get_last() + ', ' + self.get_first()

  # Returns the full name, separated by spaces without numerical marks.
  # Filters empty middle names.
  def get_name(self):
    return ' '.join(
        list(
            filter(None, [
                self.get_first_name(),
                re.sub(r'\d+', '', self.get_middle_name()),
                self.get_last_name()
            ])))

  def is_me(self):
    return self._data['web'] == 'duruofei.com'

  def get_original_name(self):
    return self._data['original']

  def get_full_name_with_marks(self):
    return ' '.join(
        list(
            filter(None, [
                self.get_first_name(),
                self.get_middle_name(),
                self.get_last_name()
            ])))

  # Returns a unique file name with First_Middle_Last.
  def _get_filename(self):
    return '_'.join(
        list(
            filter(None, [
                self.get_first_name(),
                self.get_middle_name(),
                self.get_last_name()
            ])))

  def get_birthday_to_today(self):
    date = self._data['birthday']
    if date.find('/') >= 0:
      date_match = re_birthday.match(date)
      if date_match is None:
        print('* ' + date)
      today = datetime.date.today()
      year = today.year
      month = int(date_match.group(1))
      day = int(date_match.group(2))
      if today.month == 12 and month == 1:
        year = year + 1
      birthday = datetime.date(year, month, day)
      return (birthday - today).days
    else:
      INVALID_BIRTHDAY_DIFF = -365
      return INVALID_BIRTHDAY_DIFF

  def get_birthday_str(self):
    return self._data['birthday']

  def get_name_google_markdown(self):
    return DuMark.get_google(self.get_name())

  def get_best_face_markdown(self):
    if self.check_scholar_photo_valid():
      return DuMark.get_image('../' + self._get_local_scholar_photo_url,
                              self.get_name())

    if 'face' in self._data:
      return DuMark.get_image(self._data['face'], self.get_name())
    else:
      return ''

  def get_face_raw_markdown(self):
    if 'face' in self._data:
      return DuMark.get_image(self._data['face'], self.get_name())
    else:
      return ''

  def get_website_markdown(self):
    return DuMark.get_website(self._data['web'])

  def get_email_markdown(self):
    return DuMark.get_email(self._data['email'])

  def get_facebook_markdown(self):
    return DuMark.get_facebook(self._data['FB'])

  def get_twitter_markdown(self):
    return DuMark.get_twitter(self._data['twitter'])

  def get_scholar_markdown(self):
    return DuMark.get_scholar(self._data['scholar'])

  def get_linkedin_markdown(self):
    return DuMark.get_linkedin(self._data['linkedin'])

  def get_instagram_markdown(self):
    return DuMark.get_instagram(self._data['instagram'])

  def get_github_markdown(self):
    return DuMark.get_github(self._data['github'])

  def get_vimeo_markdown(self):
    return DuMark.get_vimeo(self._data['vimeo'])

  def get_youtube_markdown(self):
    return DuMark.get_youtube(self._data['youtube'])

  def get_researchgate_markdown(self):
    return DuMark.get_researchgate(self._data['gate'])

  def _get_local_scholar_photo_url(self):
    return SCHOLAR_PHOTO_LOCAL % self._get_filename()

  def check_scholar_photo_existed(self):
    url = self._get_local_scholar_photo_url()
    return os.path.isfile(url)

  def check_scholar_photo_valid(self):
    url = self._get_local_scholar_photo_url()
    return os.path.isfile(url) and os.path.getsize(url) > 2864128

  def download_scholar_photo(self):
    if self._data['scholar']:
      filename = self._get_local_scholar_photo_url()
      DuCrawler.download_file(SCHOLAR_PHOTO_URL % self._data['scholar'],
                              filename)

  def _get_local_linkedin_photo_url(self):
    return LINKEDIN_PHOTO_LOCAL % self._get_filename()

  def download_linkedin_photo(self):
    if self._data['linkedin']:
      filename = self._get_local_scholar_photo_url()
      DuCrawler.download_image(LINKEDIN % self._data['linkedin'], filename,
                               {'class': 'pv-top-card-section__photo'})

  def check_linkedin_photo_existed(self):
    url = self._get_local_linkedin_photo_url()
    return os.path.isfile(url)

  def _get_local_website_photo_url(self):
    return WEBSITE_PHOTO_LOCAL % self._get_filename()

  def check_website_photo_existed(self):
    url = self._get_local_website_photo_url()
    return os.path.isfile(url)

  def download_website_photo(self):
    if self._data['face']:
      filename = self._get_local_website_photo_url()
      DuCrawler.download_file(self._data['face'], filename)

  # Sets the header of the properties of the Person class from gSheet.
  @staticmethod
  def set_header(header):
    Person._header = header

  # Gets the header of the properties of the Person class from gSheet.
  @staticmethod
  def get_header():
    return Person._header
