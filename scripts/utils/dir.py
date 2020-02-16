import os


class Dir:
  templates = 'templates'
  builds = 'builds'
  css = 'css'
  js = 'js'
  cites = 'cites'
  images = 'images'
  videos = 'videos'
  slides = 'slides'
  data = 'data'
  teasers = 'teasers'
  arts = 'arts'

  @staticmethod
  def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
      os.makedirs(directory)
