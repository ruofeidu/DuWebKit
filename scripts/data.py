"""Global sinleton of data.

This class manages global data.
"""


class Data:
  papers = None
  people = None
  arts = None
  pids = set()
  html = {}
  my_name = ''

  # Returns whehter a property id exists in the data properties.
  @staticmethod
  def has_pid(pid):
    return pid in Data.pids
