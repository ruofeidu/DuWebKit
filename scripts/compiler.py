""" Compiler parses templates and output html files.

"""
import os
import datetime
import configparser
import htmlmin
from markdown import markdown
from shutil import copyfile
import csscompressor
from jsmin import jsmin

from scripts.data import Data
from scripts.utils.regex import Regex
from scripts.app import App
from scripts.sync import Sync
from scripts.utils.dumark import DuMark
from scripts.utils.dir import Dir


class Lang:
  current = None
  prev = None
  en = {}
  cn = {}


class Input:
  html = []
  data = []
  md = []
  build = []


class Compiler:
  built_dict = set()
  built_html = {}

  def __init__(self):
    """Parses the configuration file for settings, languages, etc."""
    config = configparser.ConfigParser()
    config.read("config.ini", encoding='utf8')
    Dir.template = config.get('Dir', 'template').strip()
    App.debug = config.getboolean('App', 'debug')
    App.my_name = config.get('App', 'my_name').strip()
    Input.build = config.get('Input', 'build').strip().replace(" ",
                                                               "").split(",")
    # Sets up languages.
    Lang.en = dict(config.items('English'))
    Lang.cn = dict(config.items('Chinese'))
    Lang.en['year'] = datetime.date.today().year
    Lang.current = Lang.en

    # Gets the gSheets id for synchronization.
    Sync.publication = config.get('Sync', 'publication').strip().strip('"')
    Sync.people = config.get('Sync', 'people').strip().strip('"')

  def compile_css(self, css_filename):
    """Generates CSS files."""
    if css_filename in self.built_dict:
      return False
    css_fullpath = os.path.join(Dir.templates, Dir.css, css_filename)
    with open(css_fullpath, 'r', encoding='utf8') as f:
      css_content = ''.join(f.readlines())
      if App.minimize_css and css_filename.find('.min.') == -1:
        css_content = csscompressor.compress(css_content)
      output_filename = os.path.join(Dir.builds, Dir.css, css_filename)
      with open(output_filename, 'w', encoding='utf8') as o:
        o.write(css_content)
    self.built_dict.add(css_filename)
    return True

  def compile_js(self, js_filename):
    """Generates JS files."""
    if js_filename in self.built_dict:
      return False
    js_fullpath = os.path.join(Dir.templates, Dir.js, js_filename)
    with open(js_fullpath, 'r', encoding='utf8') as f:
      js_content = ''.join(f.readlines())
      # Minimizes JS file.
      if App.minimize_js and js_filename.find('.min.') == -1:
        js_content = jsmin(js_content)
      output_filename = os.path.join(Dir.builds, Dir.js, js_filename)
      with open(output_filename, 'w', encoding='utf8') as o:
        o.write(js_content)
    self.built_dict.add(js_filename)
    return True

  def compile_publication(self, pub_filename):
    """Generates publication item."""
    # First, parses the condition.
    if pub_filename in self.built_html:
      return self.built_html[pub_filename]
    with open(pub_filename, 'r', encoding='utf8') as f:
      lines = f.readlines()
    conditions = lines[0][5:-5].split(',')
    for condition in conditions:
      condition = condition.strip()
    return Data.papers.fill_templates(conditions, lines[1:])

  def compile_art(self, art_filename):
    """Generates an art work."""
    # First, parses the condition.
    if art_filename in self.built_html:
      return self.built_html[art_filename]
    with open(art_filename, 'r', encoding='utf8') as f:
      lines = f.readlines()
    conditions = lines[0][5:-5].split(',')
    for condition in conditions:
      condition = condition.strip()
    return Data.arts.fill_templates(conditions, lines[1:])

  def compile(self, filename, write_to_file=False):
    """Generates HTML files with Markdown templates.

    Args:
      filename: input filename with predefined grammar rules.

    Returns:
      HTML contents of this file.
    """
    if filename in self.built_html:
      print("Reusing HTML: %s" % filename)
      return self.built_html[filename]
    html = ''

    # extension = os.path.splitext(filename)[1]
    input_filename = os.path.join(Dir.templates, filename)
    output_filename = os.path.join(Dir.builds, filename)

    # Parses the HTML line by line.
    with open(input_filename, 'r', encoding='utf8') as f:
      lines = f.readlines()

    for line in lines:
      # Early pruning for non-special rules.
      if line.find('<!--') == -1 and line.find('{{') == -1:
        html += line
        continue

      # 1. Recursively parses the included file.
      ans = Regex.INCLUDE.search(line)
      if ans:
        include_filename = ans.group(1)
        print("~ Including HTML: %s" % include_filename)
        include_content = self.compile(include_filename)
        html += include_content
        continue

      # 2. Parses, compresses, and writes the css file.
      ans = Regex.CSS.search(line)
      if ans:
        css_filename = ans.group(1)
        print("~ Minimizing CSS: %s" % css_filename)
        self.compile_css(css_filename)
        css_filename = os.path.join(Dir.css, css_filename)
        css_filename.replace('\\', '/')
        html += '<link rel="stylesheet" href="/%s" />' % css_filename
        continue

      # 3. Parses, compresses, and writes the js file.
      ans = Regex.JS.search(line)
      if ans:
        js_filename = ans.group(1)
        print("~ Minimizing JS: %s" % js_filename)
        self.compile_js(js_filename)
        js_filename = os.path.join(Dir.js, js_filename)
        js_filename.replace('\\', '/')
        html += '<script src="/%s"></script>' % js_filename
        continue

      # 4. Parses image file.
      ans = Regex.IMAGE.search(line)
      if ans:
        image_filename = os.path.join('images', ans.group(1))
        image_description = Compiler.parse_variable(ans.group(2))
        line = DuMark.get_image('/' + image_filename, image_description)
        line = markdown(line)

      # 5. Parses publication file.
      ans = Regex.PUBLICATION.search(line)
      if ans:
        pub_filename = os.path.join('templates', ans.group(1))
        line = self.compile_publication(pub_filename)

      # 6. Parses art file.
      ans = Regex.ART.search(line)
      if ans:
        art_filename = os.path.join('templates', ans.group(1))
        line = self.compile_art(art_filename)

      # Processes variables.
      line = Compiler.parse_variable(line)

      # Appends this line.
      html += line

    # Outputs the HTML file if required.
    if write_to_file:
      # Minimizes the HTML:
      if App.minimize_html:
        if App.debug_html:
          print(html)
        html = htmlmin.minify(
            html, remove_comments=True, remove_all_empty_space=True)
      with open(output_filename, 'w', encoding='utf8') as f:
        f.write(html)

    self.built_html[filename] = html
    return html

  @staticmethod
  def parse_markdown(text):
    """Converts a line of markdown to HTML."""
    # Converts \\ to <br>.
    text = str(text).strip('"').replace('\\\\', '<br />')
    text = markdown(text)
    # Eliminates extra paragraph labels.
    if len(text) > 7 and text[:3] == '<p>' and text[-4:] == '</p>':
      text = text[3:-4]
    return text

  @staticmethod
  def parse_variable(line):
    """Converts a variable to language-dependent text."""
    ans = Regex.VARIABLE.search(line)
    while ans:
      variable = ans.group(1)
      language = Lang.current
      # Forces language if required.
      if variable.find('_cn') != -1:
        language = Lang.cn
        variable = variable[:-3]
      elif variable.find('_en') != -1:
        language = Lang.en
        variable = variable[:-3]
      # Searches the variable in the current language or English.
      value = ''
      if variable not in language:
        print('[Warn] Cannot find variable %s.' % variable)
        break
        if variable not in Lang.en:
          print('[Error] Cannot find variable %s.' % variable)
          break
        else:
          value = Lang.en[variable]
      else:
        value = language[variable]
      # Parses the value of the variable, adds links, and converts Markdown to HTML.
      value = Compiler.parse_markdown(value)
      line = line.replace(ans.group(0), value)
      ans = Regex.VARIABLE.search(line)
    return line
