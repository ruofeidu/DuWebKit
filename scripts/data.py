"""Global sinleton of data.

This class manages global data.
"""


class Data:
  """Singleton class to manage all the data."""
  papers = None
  people = None
  arts = None
  ready_to_destroy = False
  pids = set()
  html = {}
  # List of files to build.
  build_files = []
  my_name = ''

  # Returns whehter a property id exists in the data properties.
  @staticmethod
  def has_pid(pid):
    return pid in Data.pids
