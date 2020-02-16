"""Paper defines a single paper.

This class allows the user to format a paper.
"""
import re
import math
import warnings
import os.path
from markdown import markdown

from scripts.app import App
from scripts.authors import Authors
from scripts.utils.constants import PUNCTUATION, FILE_LOWRES_MAXSIZE, LINK_SEPARATOR, LINK_COMMA
from scripts.utils.utils import Utils
from scripts.utils.dumark import DuMark
from scripts.utils.regex import Regex
from scripts.utils.dir import Dir


# Capitalizes a single word w.
def capitalize_single(w):
  return w[0].upper() + w[1:]


# Capitalizes into APA format.
def capitalize_apa(s, spliter=' '):
  LOWER_CASES = {
      'a', 'an', 'the', 'to', 'on', 'in', 'of', 'at', 'by', 'for', 'or', 'and',
      'vs.', 'iOS'
  }

  s = s.strip(',.- ')

  # Reverse wrong order for IEEE proceedings.
  # if comma is found and last word is 'on'
  if s.rfind(',') > 0 and s[-3:].lower() == ' on':
    p = s.rfind(',')
    s = s[p + 2:] + s[:p]

  # Split the words and capitalize with filters
  words = s.split(spliter)
  capitalized_words = []
  start = True
  for word in words:
    if len(word) == 0:
      continue
    if not start and word.lower() in LOWER_CASES:
      capitalized_words.append(word.lower())
    else:
      capitalized_words.append(capitalize_single(word))
    start = word[-1] in '.:'

  s = spliter.join(capitalized_words)

  return s if spliter == '-' else capitalize_apa(s, '-')


# Capitalizes a string.
def capitalize_all(s):
  return ' '.join(list(map(capitalize_single, s.split(' '))))


class Paper:
  __slots__ = ('_data')
  _header = []

  _bib_items = [
      'b_title', 'b_author', 'journal', 'booktitle', 'school', 'institution',
      'note', 'year', 'volume', 'number', 'editor', 'location', 'publisher',
      'b_month', 'day', 'b_pages', 'b_numpages', 'series', 'doi'
  ]

  _book_map = {
      'article': 'journal',
      'inproceedings': 'booktitle',
      'conference': 'booktitle',
      'techreport': 'institution',
      'phdthesis': 'school',
      'masterthesis': 'school',
      'bachelorthesis': 'school',
      'misc': 'howpublished'
  }

  _type_map = {
      'conf': 'inproceedings',
      'poster': 'inproceedings',
      'lbw': 'inproceedings',
      'poster': 'inproceedings',
      'workshop': 'inproceedings',
      'demo': 'inproceedings',
      'journal': 'article',
      'phd': 'phdthesis',
      'ms': 'masterthesis',
      'bs': 'bachelorthesis',
      'patent': 'misc',
      'arxiv': 'misc',
      'report': 'techreport',
  }

  _month_map = [
      '',
      'Jan.',
      'Feb.',
      'Mar.',
      'Apr.',
      'May',
      'Jun.',
      'Jul.',
      'Aug.',
      'Sep.',
      'Oct.',
      'Nov.',
      'Dec.',
  ]

  def __init__(self, row):
    """Iniializes the data and defaul fields."""
    self._data = {}
    b = self._data
    for i, label in enumerate(Paper.get_header()):
      b[label] = row[i] if i < len(row) else ''

    self._create_authors()
    self._create_title()

    self._create_bib_id()
    self._create_bib_date()
    self._create_bib_pages()
    # Reformats proceeding or journal names.
    self._create_bib_type()

    b['score'] = int(b['score'])
    b['published'] = (b['published'] == '1')
    b['visible'] = (b['visible'] == '1')
    b['lowres'] = False
    self.debug_pdf()

    # Assigns video URL. TODO: fill MP4.
    if b['youtube']:
      b['video'] = self.get_youtube_url()
    elif b['vimeo']:
      b['video'] = self.get_vimeo_url()
    else:
      b['video'] = ''

    # Assigns slides URL. TODO: fill pptx and pdf.
    if b['slideshare']:
      b['slides'] = self.get_slideshare_url()
    elif b['gslides']:
      b['slides'] = self.get_gslides_url()
    else:
      b['slides'] = ''

  def get_youtube_url(self):
    return 'https://youtu.be/%s' % self._data['youtube'] if self._data[
        'youtube'] else ''

  def get_vimeo_url(self):
    return 'https://vimeo.com/%s' % self._data['vimeo'] if self._data[
        'vimeo'] else ''

  def get_slideshare_url(self):
    return 'https://www.slideshare.net/duruofei/%s' % (
        self._data['slideshare']) if self._data['slideshare'] else ''

  def get_gslides_url(self):
    gslides = self._data['gslides']
    if gslides:
      if gslides[:4] == 'http':
        return gslides
      else:
        return 'https://docs.google.com/presentation/d/%s'
    else:
      return ''

  def get_doi(self):
    return self._data['doi']

  def get_doi_markdown(self):
    return DuMark.get_url('https://doi.org/%s' % self.get_doi(), 'doi')

  def get_doi_html(self):
    return Utils.remove_p(markdown(self.get_doi_markdown()))

  def get_cite_html(self):
    return '<a class="cite" href="%scites/%s.html">cite</a>' % (
        App.root, self._data['bib'])

  def export_cite_html(self):
    html = ''

    filename = os.path.join(Dir.cites, "%s.html" % self._data['bib'])
    with open(filename, 'w', encoding='utf8') as f:
      f.write(html)

  def get_bibtex(self):
    """ Returns BibTeX of this paper.

    References:
      http://www.bibtex.org/Format
      https://verbosus.com/bibtex-style-examples.html
    """
    b = self._data
    TAB, LB = Utils.get_tab(), Utils.get_line_break()
    s = '@%s{%s,%s' % (b['b_type'], b['bib'], LB)

    for label in Paper.get_bib_items():
      if label in b and b[label]:
        key = label
        if label[:2] == 'b_':
          key = label[2:]
        s += '%s%s = {%s},%s' % (TAB, key, b[label], LB)

    s += '}%s' % LB
    return s

  def get_apa(self):
    """Returns APA style citation.
    Reference:
      TODO: https://owl.purdue.edu/owl/research_and_citation/apa_style/apa_formatting_and_style_guide/reference_list_author_authors.html
    """
    b = self._data
    TAB, LB = Utils.get_tab(), Utils.get_line_break()
    s = self.get_authors().get_apa()
    s += ' (%s).' % b['year']
    s += LB
    s += b['title'] + '.'
    s += LB
    s += 'In %s, ' % self.get_book()
    # Appends volume and number for journal articles.
    if b['volume']:
      s += b['volume']
      if b['number']:
        s += '(%s)' % b['number']
      s += ', '

    # Appends pages.
    if 'b_pages' in b:
      s += b['b_pages'].replace('--', '-')
    elif 'b_numpages' in b:
      s += 'pp. ' + b['b_pages']
    s += '.'
    return s

  def get_mla(self):
    """Returns MLA style citation."""
    b = self._data
    TAB, LB = Utils.get_tab(), Utils.get_line_break()
    s = self.get_authors().get_mla()
    s += LB
    s += '"%s".' % b['title']
    s += LB
    s += self.get_book() + ', '
    if b['volume']:
      s += b['volume']
      if b['number']:
        s += '(%s)' % b['number']
      s += ', '

    if 'b_pages' in b:
      s += b['b_pages'].replace('--', '-')
    elif 'b_numpages' in b:
      s += 'pp. %s' % b['b_pages']
    s += '. %s.' % b['year']
    return s

  def get_chicago(self):
    """Returns MLA style citation."""
    b = self._data
    TAB, LB = Utils.get_tab(), Utils.get_line_break()
    s = self.get_authors().get_mla()
    s += LB
    s += '"%s".' % b['title']
    s += LB
    s += self.get_book() + ', '
    if b['volume']:
      s += b['volume']
      if b['number']:
        s += '(%s)' % b['number']
      s += ', '

    if 'b_pages' in b:
      s += b['b_pages'].replace('--', '-')
    elif 'b_numpages' in b:
      s += 'pp. %s' % b['b_pages']
    s += '. %s.' % b['year']
    return s

  def get_harvard(self):
    """Returns Harvard style citation."""
    b = self._data
    TAB, LB = Utils.get_tab(), Utils.get_line_break()
    s = self.get_authors().get_mla()
    s += LB
    s += '"%s".' % b['title']
    s += LB
    s += self.get_book() + ', '
    if b['volume']:
      s += b['volume']
      if b['number']:
        s += '(%s)' % b['number']
      s += ', '

    if 'b_pages' in b:
      s += b['b_pages'].replace('--', '-')
    elif 'b_numpages' in b:
      s += 'pp. %s' % b['b_pages']
    s += '. %s.' % b['year']
    return s

  def get_vancouver(self):
    """Returns Vancouver style citation."""
    b = self._data
    TAB, LB = Utils.get_tab(), Utils.get_line_break()
    s = self.get_authors().get_mla()
    s += LB
    s += '"%s".' % b['title']
    s += LB
    s += self.get_book() + ', '
    if b['volume']:
      s += b['volume']
      if b['number']:
        s += '(%s)' % b['number']
      s += ', '

    if 'b_pages' in b:
      s += b['b_pages'].replace('--', '-')
    elif 'b_numpages' in b:
      s += 'pp. %s' % b['b_pages']
    s += '. %s.' % b['year']
    return s

  def get_resume(self):
    b = self._data
    s = ''
    s = b['authors'].get_resume()
    s += '. {\\it ' + b['title'] + '}. '
    if 'book' in b and b['book']:
      s += b['book'] + ' '
    else:
      return ''
    s += b['year']
    return s

  def get_bib_id(self):
    return self._data['b_id']

  def get_authors(self):
    """Returns the full Authors class."""
    return self._data['authors']

  def get_filename(self):
    """Returns the PDF file name."""
    b = self._data
    return '%s_%s_%s%s' % (b['authors'].first().get_last_name(),
                           b['title_file'], b['series'].replace(' ',
                                                                ''), b['year'])

  def _create_authors(self):
    """Creates Authors into the `authors` field.

    case 1: Du, Ruofei and Wills, Kent R. and Potasznik, Max and Froehlich, Jon E.
    case 2: Yue Jiang, Ruofei Du, Christof Lutteroth, and Wolfgang Stuerzlinger
    case 3: Ruofei Du and Sujal Bista and Amitabh Varshney

    names = re.split(',|;|and', authors) will not work for all cases
    """
    b = self._data
    authors = b['authors']
    names = authors.split('and')
    spliter_and = True
    for name in names:
      if name.count(',') > 1:
        spliter_and = False
    if not spliter_and:
      names = authors.split(',')

    # Removes ' and ' from names.
    names = [y for x in names for y in x.split('and ')]

    # Removes leading and trailing spaces / and.
    map(str.strip, names)

    # Removes empty name.
    names = list(filter(None, names))
    b['authors'] = Authors(names)
    b['b_author'] = b['authors'].get_bib()

  def _create_bib_id(self):
    """Computes the bib ID using format Lastname2000Title format."""
    b = self._data
    b['b_id'] = b['authors'].first().get_last() + b['year'] + b['title_first']
    if b['b_id'] != b['bib']:
      print('* ', b['b_id'], 'and', b['bib'], ' do not match')

  def _create_title(self):
    """Reformats the title."""
    b = self._data
    b['title'] = capitalize_apa(b['title'])
    b['b_title'] = '{%s}' % b['title'].replace('° ', '\degree~')
    if b['title'].count(' '):
      word = b['title'][:b['title'].find(' ')]
      for p in PUNCTUATION:
        if word.count(p):
          word = word[:word.find(p)]
      b['title_first'] = capitalize_all(word)
    else:
      b['title_first'] = b['title'].strip(PUNCTUATION)

    b['title_file'] = ''.join(
        re.split(' |\.|\,|\!|\?',
                 capitalize_all(b['title']).replace(':', '-').replace('°', '')))

  def _create_bib_type(self):
    """Reformats the bibtype."""
    self._data['b_type'] = self._type_map[self._data['type']]
    self._data[Paper._book_map[self._data['b_type']]] = self._data['book']

  def debug_pdf(self):
    """Outputs whether the corresponding PDF and low-res version exist."""
    if 'debugged_pdf' in self._data:
      return True
    self._data['debugged_pdf'] = True
    rawname = self.get_filename()
    filename = 'builds/papers/%s.pdf' % rawname
    lowres = 'builds/papers/%s_lowres.pdf' % rawname
    supp = 'builds/papers/%s_supp.pdf' % rawname

    if not os.path.isfile(filename):
      print('%s does not exist.' % filename)
      return False
    if os.path.getsize(filename) > FILE_LOWRES_MAXSIZE:
      if not os.path.isfile(lowres):
        print('%s does not have low-res version.' % filename)
        return False
      else:
        self._data['lowres'] = True
    if os.path.isfile(supp):
      self._data['supp'] = '/papers/%s_supp.pdf' % rawname
    return True

  def _create_bib_date(self):
    """Reformat dates."""
    if 'month' in self._data and self._data['month']:
      self._data['month'] = int(self._data['month'])
      self._data['b_month'] = self._month_map[self._data['month']]

  def _create_bib_pages(self):
    """Reformat pages."""
    if self._data['pages'].find('-'):
      self._data['b_pages'] = self._data['pages'].replace('-', '--')
    else:
      del self._data['b_pages']
      self._data['b_numpages'] = self._data['pages']

  def to_dict(self):
    return self._data

  def is_published(self):
    return self._data['published']

  def is_visible(self):
    return self._data['visible']

  @staticmethod
  def get_bib_items():
    return Paper._bib_items

  @staticmethod
  def set_header(header):
    Paper._header = header

  @staticmethod
  def get_header():
    return Paper._header

  def get_title_markdown(self):
    return DuMark.get_paper(self.get_filename(), self._data['title'])

  def get_title_html(self):
    return Utils.remove_p(markdown(self.get_title_markdown()))

  def get_pdf_markdown(self):
    return DuMark.get_paper(self.get_filename(), 'pdf', self._data['title'])

  def get_lowres_markdown(self):
    if self._data['lowres']:
      return DuMark.get_paper(self.get_filename() + '_lowres', 'lowres',
                              self._data['title'] + ' low resolution file')
    else:
      return ''

  def get_book(self):
    """Returns the generic book title."""
    return self._data['book']

  def get_book_and_year(self):
    """Returns book and year."""
    return '%s, %s.' % (self.get_book(), self.get_year())

  def get_book_and_series_and_year(self):
    """Returns book and series and year."""
    if self._data['type'] == 'phd':
      return '%s, %s, %s.' % (self._data['attr'], self.get_book(),
                              self.get_year())
    elif self._data['series']:
      return '%s (%s), %s.' % (self.get_book(), self._data['series'],
                               self.get_year())
    else:
      return self.get_book_and_year()

  def get_year(self):
    """Returns year."""
    return self._data['year']

  def get_teaser_markdown(self):
    """Returns teaser markdown."""
    return DuMark.get_image('/%s/%s.jpg' % (Dir.teasers, self.get_bib_id()),
                            '%s Teaser Image.' % self._data['title'])

  def get_teaser_html(self):
    return Utils.remove_p(markdown(self.get_teaser_markdown()))

  def get_pdf_url(self):
    return '%spapers/%s.pdf' % (App.root, self.get_filename())

  def get_web_url(self):
    if self._data['web']:
      return self._data['web']
    else:
      return self.get_pdf_url()

  def get_web_markdown(self):
    return DuMark.get_url(self.get_web_url(), 'website')

  def get_video_markdown(self):
    if self._data['video']:
      return DuMark.get_url(self._data['video'], 'video')
    else:
      return ''

  def get_slides_markdown(self):
    if self._data['slides']:
      return DuMark.get_url(self._data['slides'], 'slides')
    else:
      return ''

  def get_code_markdown(self):
    if self._data['code']:
      return DuMark.get_url(self._data['code'], 'code')
    else:
      return ''

  def get_data_markdown(self):
    if self._data['data']:
      return DuMark.get_url(self._data['data'], 'data')
    else:
      return ''

  def get_demo_markdown(self):
    if self._data['demo']:
      return DuMark.get_url(self._data['demo'], 'demo')
    else:
      return ''

  def get_supp_markdown(self):
    if 'supp' in self._data:
      return DuMark.get_url(self._data['supp'], 'supp')
    else:
      return ''

  def get_short_links_markdown(self):
    """ pdf, lowres, doi | website, video, slides, code, demo, supp | cite """
    # pdf, lowres, doi.
    md = self.get_pdf_markdown()
    line = self.get_lowres_markdown()
    if line:
      md += LINK_COMMA + line
    if self.get_doi():
      md += LINK_COMMA + self.get_doi_markdown()

    md += LINK_SEPARATOR

    # website, video, slides, code.
    md += self.get_web_markdown()
    line = self.get_video_markdown()
    if line:
      md += LINK_COMMA + line
    line = self.get_slides_markdown()
    if line:
      md += LINK_COMMA + line
    line = self.get_code_markdown()
    if line:
      md += LINK_COMMA + line
    line = self.get_data_markdown()
    if line:
      md += LINK_COMMA + line
    line = self.get_demo_markdown()
    if line:
      md += LINK_COMMA + line
    line = self.get_supp_markdown()
    if line:
      md += LINK_COMMA + line

    md += LINK_SEPARATOR
    # cite
    md += self.get_cite_html()
    return md

  def get_short_links_html(self):
    """Get a list of short links."""
    return Utils.remove_p(markdown(self.get_short_links_markdown()))

  def fill_template(self, lines, total=0):
    """Fills predefined templates in lines by conditions."""
    html = ''
    for line in lines:
      matched = Regex.KEY.search(line)
      while matched:
        key = matched.group(1)
        value = ''
        if key == 'even':
          value = '$' if total % 2 == 1 else ''
        elif key == 'web':
          value = self.get_web_url()
        elif key == 'teaser':
          value = self.get_teaser_html()
        elif key == 'title':
          value = self.get_title_html()
        elif key == 'award':
          if self._data[key]:
            value += '<span class="award">%s</span>' % self._data[key]
        elif key == 'authors':
          value += self.get_authors().get_html()
        elif key == 'book_title':
          value += self.get_book_and_series_and_year()
        elif key == 'short_links':
          value += self.get_short_links_html()
        elif key == 'apa_html':
          value += self.get_apa()
        elif key == 'mla_html':
          value += self.get_mla()
        elif key == 'bibtex_html':
          value += self.get_bibtex()
        line = line.replace(matched.group(0), value)
        matched = Regex.KEY.search(line)
      html += line
    return html
