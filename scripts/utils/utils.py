from scripts.utils.constants import FILE_TAB, HTML_TAB, FILE_LINE_BREAK, HTML_LINE_BREAK, FILE_SEPARATOR, HTML_SEPARATOR


class Utils:
  _tab = FILE_TAB
  _line_break = FILE_LINE_BREAK
  _separator = FILE_SEPARATOR

  @staticmethod
  def set_line_break(line_break):
    Utils._line_break = line_break

  @staticmethod
  def get_line_break():
    return Utils._line_break

  @staticmethod
  def set_to_print_web():
    Utils._tab = HTML_TAB
    Utils._line_break = HTML_LINE_BREAK
    Utils._separator = HTML_SEPARATOR

  @staticmethod
  def set_to_print_file():
    Utils._tab = FILE_TAB
    Utils._line_break = FILE_LINE_BREAK
    Utils._separator = FILE_SEPARATOR

  @staticmethod
  def set_tab(tab):
    Utils._tab = tab

  @staticmethod
  def get_tab():
    return Utils._tab

  @staticmethod
  def get_url(base, data):
    return base % data if data else None

  @staticmethod
  def get_separator():
    return Utils._separator

  @staticmethod
  def filter_url(url):
    url = url.replace('www.', '')
    if url[-1] == '/':
      url = url[:-1]
    return url

  @staticmethod
  def write_file(filename, s):
    with open(filename, 'w', encoding='utf8') as f:
      f.write(s)

  @staticmethod
  def remove_p(s):
    if s[:3] == '<p>' and s[-4:] == '</p>':
      return s[3:-4]
    else:
      return s
