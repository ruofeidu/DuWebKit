import re
from scripts.utils.constants import FILE_TAB, HTML_TAB, FILE_LINE_BREAK, HTML_LINE_BREAK, FILE_SEPARATOR, HTML_SEPARATOR


class Utils:
  """Common utilities and constants for input and output."""
  _tab = FILE_TAB
  _line_break = FILE_LINE_BREAK
  _separator = FILE_SEPARATOR
  _print_file = True
  _last_status = True

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

  _month2num = {
      '': None,
      'jan': 1,
      'feb': 2,
      'mar': 3,
      'apr': 4,
      'may': 5,
      'jun': 6,
      'jul': 7,
      'aug': 8,
      'sep': 9,
      'oct': 10,
      'nov': 11,
      'dec': 12,
  }

  _month_full_map = [
      '',
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
  ]

  @staticmethod
  def date2readable(date):
    if date is None:
      return ''
    year, month, day = Utils.parse_date(date)
    if month is None:
      return str(year)
    else:
      return '%s %d, %d' % (Utils._month_full_map[month], day, year)

  @staticmethod
  def num2month_dot(num):
    return Utils._month_map[num]

  @staticmethod
  def set_line_break(line_break):
    Utils._line_break = line_break

  @staticmethod
  def get_line_break():
    return Utils._line_break

  @staticmethod
  def update_print_symbols():
    if Utils._print_file:
      Utils._tab = FILE_TAB
      Utils._line_break = FILE_LINE_BREAK
      Utils._separator = FILE_SEPARATOR
    else:
      Utils._tab = HTML_TAB
      Utils._line_break = HTML_LINE_BREAK
      Utils._separator = HTML_SEPARATOR

  @staticmethod
  def set_to_print_web():
    Utils._last_status = Utils._print_file
    Utils._print_file = False
    Utils.update_print_symbols()

  @staticmethod
  def set_to_print_file():
    Utils._last_status = Utils._print_file
    Utils._print_file = True
    Utils.update_print_symbols()

  @staticmethod
  def set_to_print_last_status():
    Utils._print_file = Utils._last_status
    Utils.update_print_symbols()

  @staticmethod
  def parse_date(date):
    year = None
    month = None
    day = None
    if date:
      if '/' in date:
        year = int(date[:4])
        date = date[5:]
        if '/' in date:
          month = int(date[:date.find('/')])
          day = int(date[date.find('/') + 1:])
        else:
          month = date
      else:
        year = int(date)
    return year, month, day

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

  @staticmethod
  def read_lines(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
      return f.readlines()

  @staticmethod
  def capitalize_single(w):
    """Capitalizes a single word w."""
    return w[0].upper() + w[1:]

  @staticmethod
  def capitalize_apa(s, spliter=' '):
    """Capitalizes a single word w."""
    LOWER_CASES = {
        'a', 'an', 'the', 'to', 'on', 'in', 'of', 'at', 'by', 'for', 'or',
        'and', 'vs.', 'iOS'
    }

    s = s.strip(',.- ')

    # Reverses wrong order for IEEE proceedings.
    # if comma is found and last word is 'on'.
    if s.rfind(',') > 0 and s[-3:].lower() == ' on':
      p = s.rfind(',')
      s = s[p + 2:] + s[:p]

    # Split the words and capitalize with filters.
    words = s.split(spliter)
    capitalized_words = []
    start = True
    for word in words:
      if len(word) == 0:
        continue
      if not start and word.lower() in LOWER_CASES:
        capitalized_words.append(word.lower())
      else:
        capitalized_words.append(Utils.capitalize_single(word))
      start = word[-1] in '.:'

    s = spliter.join(capitalized_words)

    return s if spliter == '-' else Utils.capitalize_apa(s, '-')

  @staticmethod
  def capitalize_all(s):
    """Capitalizes a title (string)."""
    return ' '.join(list(map(Utils.capitalize_single, s.split(' '))))

  @staticmethod
  def file_nameable(s):
    """Makes a string available for file names.

    Removes all punctuations.
    Converts : to -.
    Removes UTF-8 characters such as °.
    """
    return ''.join(
        re.split(' |\,|\!|\?|\"',
                 s.replace(':', '-').replace('°', '')))

  @staticmethod
  def is_info_letter_num_space(s):
    return
