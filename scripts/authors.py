"""Authors define an author list.

This class allows the user process authors in batch.
"""
from markdown import markdown

from scripts.person import Person
from scripts.data import Data
from scripts.app import App
import warnings


class Authors:
  __slots__ = ('_data', '_keys')
  _count = 0

  # Initializes the author with list of names
  # The names can use commas to separate first and last names.
  def __init__(self, names):
    self._data = []
    # Separates a list of authors.
    for name in names:
      s = name.strip()
      # Finds the separater.
      p = s.find(',')
      # case 1: Du, Ruofei
      if p >= 0:
        last, first = s[:p].strip(), s[p + 1:].strip()
      # case 2: Ruofei Du
      else:
        p = s.rfind(' ')
        first, last = s[:p].strip(), s[p + 1:].strip()
      res = Data.people.query_first_last(first, last)
      if not res:
        res = Data.people.add_person(first, last)
      self._data.append(res)

  def __str__(self):
    """Converts an author list to a readable string."""
    s, n = '', len(self._data)
    for i, author in enumerate(self._data):
      s += str(author)
      if n == 2 and i == 0:
        s += ' and '
      elif n > 2:
        if i < n - 2:
          s += ', '
        elif i == n - 2:
          s += ', and '
    return s

  def get_apa(self):
    """Converts the author list to a string of APA style."""
    s, n = '', len(self._data)
    for i, author in enumerate(self._data):
      s += author.get_apa()
      if n == 2 and i == 0:
        s += ', & '
      elif n > 2:
        if i < n - 2:
          s += ', '
        elif i == n - 2:
          s += ', & '
    return s

  def get_mla(self):
    """Converts the author list to a string of MLA style."""
    s, n = '', len(self._data)
    for i, author in enumerate(self._data):
      s += author.get_mla()
      if n == 2 and i == 0:
        s += ' and '
      elif n > 2:
        if i < n - 2:
          s += ', '
        elif i == n - 2:
          s += ', and '
    return s

  def get_markdown(self):
    s, n = '', len(self._data)
    for i, author in enumerate(self._data):
      s += author.get_name_markdown()
      if n == 2 and i == 0:
        s += ' and '
      elif n > 2:
        if i < n - 2:
          s += ', '
        elif i == n - 2:
          s += ', and '
    return s

  def get_html(self):
    return markdown(self.get_markdown())

  def first(self):
    return self._data[0] if self._data else None

  # Gets the list of authors in bibtex format.
  def get_bib(self):

    # Gets a single author's bibtex.
    def _get_single_bib(author):
      return author.get_bib()

    # Returns the list of authors' bibtex connected by 'and'.
    return ' and '.join(list(map(_get_single_bib, self._data)))

  # Gets my resume.
  def get_resume(self):
    return str(self).replace(App.my_name, '\\textbf{' + App.my_name + '}')

  @staticmethod
  def count():
    return Authors._count
