"""Paper defines a single paper.

This class allows the user to export a paper in JSON, Javascript, etc.
"""
import os
import re
import json
import htmlmin
from markdown import markdown
from scripts.paper import Paper
from scripts.utils.utils import Utils
from scripts.utils.dumark import DuMark
from scripts.utils.constants import DEBUG_HTML_SCRIPT
from scripts.utils.regex import Regex
from scripts.utils.dir import Dir


class Papers:
  __slots__ = ('_data', '_keys')
  _count = 0

  def __init__(self, rows):
    """ Data is a dict, key is a list. """
    Paper.set_header(rows[0])
    Papers._count = len(rows)
    self._data = {}
    self._keys = []
    for i in range(1, len(rows)):
      key = rows[i][0]
      self._keys.append(key)
      self._data[key] = Paper(rows[i])

  # Backs up the data.
  def backup(self):
    self.export_bib('bib/papers.bib')
    self.export_bib_ids('debug/bib_ids.txt')
    self.export_resume('debug/papers.tex')
    self.export_file_names('debug/paper_filesnames.txt')
    self.export_html('debug/index.html')
    # JSON has to be backed up lastly.
    self.export_json('json/papers.json')

  # Returns the JSON format data of the full class.
  def to_json(self):
    print('! Papers To JSON must be called in the end: it destroys authors.')
    _dict = {}
    for pid in self._keys:
      _dict[pid] = self._data[pid].to_dict()
      _dict[pid]['authors'] = str(_dict[pid]['authors'])

    return json.dumps({'_data': _dict, '_keys': self._keys}, indent=2)

  # Writes to JSON file.
  def export_json(self, filename):
    with open(filename, 'w', encoding='utf8') as f:
      f.write(self.to_json())

  # Writes to BIB file.
  def export_bib(self, filename):
    Utils.set_to_print_file()
    s = ''
    for k in self._keys:
      s += self._data[k].get_bibtex()
      s += Utils.get_line_break()
    with open(filename, 'w', encoding='utf8') as f:
      f.write(s)

  def export_resume(self, filename):
    Utils.set_to_print_file()
    s = ''
    for k in self._keys:
      s += self._data[k].get_resume()
      s += Utils.get_line_break()
    with open(filename, 'w', encoding='utf8') as f:
      f.write(s)

  # Debug: Writes bib ids to a file.
  def export_bib_ids(self, filename):
    Utils.set_to_print_file()
    s = ''
    for k in self._keys:
      s += self._data[k].get_bib_id()
      s += Utils.get_line_break()
    with open(filename, 'w', encoding='utf8') as f:
      f.write(s)

  # Debug: Writes paper files names to a file.
  def export_file_names(self, filename):
    s = ''
    for k in self._keys:
      s += self._data[k].get_filename()
      s += Utils.get_line_break()
    with open(filename, 'w', encoding='utf8') as f:
      f.write(s)

  @staticmethod
  def count():
    return Papers._count

  def export_html(self, filename):
    """ Exports HTML for debugging only. """
    Utils.set_to_print_web()
    s = DuMark.get_h1('List of publications (temporary)')
    i = 0
    for k in self._keys:
      d = self._data[k]
      if not d.is_visible():
        continue
      d.debug_pdf()
      i += 1
      s += '[%d] ' % i
      s += d.get_authors().get_markdown()
      s += '. '
      s += d.get_title_markdown()
      s += ' '
      s += d.get_lowres_markdown()
      s += ' '
      s += d.get_book()
      s += '. '
      s += d.get_year()
      s += '.'
      s += Utils.get_separator()
    s += DEBUG_HTML_SCRIPT
    s = htmlmin.minify(markdown(s))
    with open(filename, 'w', encoding='utf8') as f:
      f.write(s)

  def fill_templates(self, conditions, lines):
    """ Fills predefined templates in lines by conditions. """
    html = ''
    total = 0
    for k in self._keys:
      paper = self._data[k]
      d = paper._data
      d['count'] = total + 1
      condition_met = True
      for condition in conditions:
        matched = Regex.CONDITION.search(condition)
        if matched:
          lhs = matched.group(1)
          compare = matched.group(2)
          rhs = matched.group(3)
          if rhs.isdigit():
            rhs = int(rhs)
          if (compare == '>' and
              d[lhs] <= rhs) or (compare == '>=' and d[lhs] <= rhs) or (
                  compare == '<' and
                  d[lhs] >= rhs) or (compare == '<=' and d[lhs] > rhs) or (
                      (compare == '=' or compare == '==') and d[lhs] != rhs):
            condition_met = False
        else:
          print('Error in parsing condition ' + condition)
      # Appends the filled templates if all conditions are met.
      if condition_met:
        html += paper.fill_template(lines, total)
        total += 1
    return html

  def export_cites_html(self, filename):
    Utils.set_to_print_web()
    with open(filename, 'r', encoding='utf8') as f:
      lines = f.readlines()
      for k in self._keys:
        paper = self._data[k]
        d = paper._data
        html = ''
        html += paper.fill_template(lines)
        Dir.ensure_dir(os.path.join(Dir.builds, Dir.cites))
        output_filename = os.path.join(Dir.builds, Dir.cites,
                                       '%s.html' % d['bib'])
        with open(output_filename, 'w', encoding='utf8') as f:
          f.write(html)
