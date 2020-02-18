""" Parser parses templates and output html files.

"""
import re


class Regex:
  """Regular expression patterns for parsing the templates."""

  # Matches: <!-- include: header.html -->
  INCLUDE = re.compile('\<\!\-\-\s*include:\s?([\w\.-\/]+\.\w+)\s*\-\-\>')

  # Matches: <!-- css: main.css -->
  CSS = re.compile('\<\!\-\-\s*css:\s?([\w\.-\/]+\.\w+)\s*\-\-\>')

  # Matches: <!-- js: jquery.poptrox.min.js -->
  JS = re.compile('\<\!\-\-\s*js:\s?([\w\.-\/]+\.\w+)\s*\-\-\>')

  # Matches: <!-- markdown: blog.md -->
  MARKDOWN = re.compile('\<\!\-\-\s*markdown:\s?([\w\.-\/]+\.\w+)\s*\-\-\>')

  # Matches: <!-- image: RuofeiDu.jpg | {{avatar}} -->
  IMAGE = re.compile(
      '\<\!\-\-\s*image\:\s?(\w+\.\w+)\s*\|\s*([\w\{\}]+)\s*\-\-\>')

  # Matches: <!-- assign: variable_abc as variable_abc -->
  ASSIGN = re.compile('\<\!\-\-\s*assign\:\s?(\w+)\s*as\s*(\w+)\s*\-\-\>')

  # Matches: <!-- publication: publication_featured.html -->
  PUBLICATION = re.compile(
      '\<\!\-\-\s*publication:\s?([\w\.-\/]+\.\w+)\s*\-\-\>')

  # Matches: <!-- art: data_art_featured.html -->
  ART = re.compile('\<\!\-\-\s*art:\s?([\w\.-\/]+\.\w+)\s*\-\-\>')

  # Matches: {{avatar}}
  VARIABLE = re.compile('\{\{\s*(\w+)\s*\}\}')

  # Matches: {{$avatar}}
  KEY = re.compile('\{\{\s*\$(\w+)\s*\}\}')

  # Matches: score>89
  CONDITION = re.compile('(\w+)([><=]+)(\d+)')

  # Backburners
  COMMENTS = re.compile("(<!--[^\\[<>].*?(?<!!)-->)", flags=re.DOTALL)
  RAW_COMMENTS = re.compile("(<!--.*?-->)", flags=re.DOTALL)
  BLANK_LINES = re.compile("\n\s*\n", flags=re.DOTALL)
