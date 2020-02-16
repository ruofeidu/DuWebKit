"""Arts defines a single art.

This class allows the user to export an art in JSON, Javascript, etc.
"""
import os
import re
import json
import htmlmin
from markdown import markdown
from scripts.art import Art
from scripts.utils.utils import Utils
from scripts.utils.dumark import DuMark
from scripts.utils.constants import DEBUG_HTML_SCRIPT
from scripts.utils.regex import Regex
from scripts.utils.dir import Dir


class Arts:
  __slots__ = ('_data', '_keys')
  _count = 0

  def __init__(self, rows):
    """ Data is a dict, key is a list. """
    Art.set_header(rows[0])
    Arts._count = len(rows)
    self._data = {}
    self._keys = []
    for i in range(1, len(rows)):
      key = rows[i][0]
      self._keys.append(key)
      self._data[key] = Art(rows[i])

  def fill_templates(self, conditions, lines):
    """ Fills predefined templates in lines by conditions. """
    html = ''
    total = 0
    for k in self._keys:
      art = self._data[k]
      d = art._data
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
        html += art.fill_template(lines, total)
        total += 1
    return html
