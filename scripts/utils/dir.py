import os


class Dir:
  """Manages common directories to use."""
  templates = 'templates'
  data = '~/'
  builds = 'builds'
  css = 'css'
  js = 'js'
  cites = 'cites'
  references = 'references'
  abstracts = 'abstracts'
  images = 'images'
  videos = 'videos'
  slides = 'slides'
  papers = 'papers'
  posters = 'posters'
  project = 'project'
  projects = 'projects'
  data = 'data'
  teasers = 'teasers'
  gifs = 'gifs'
  arts = 'arts'
  talks = 'talks'
  softwares = 'softwares'
  medias = 'medias'
  citations = 'citations'
  reviews = 'reviews'
  experiences = 'experiences'
  third_party = 'third_party'
  cwp = os.path.dirname(os.path.abspath(__file__))
  cwd = os.getcwd()
  builds_path = os.path.join(os.getcwd(), builds)

  @staticmethod
  def ensure_dir(file_path):
    """Ensures that the file_path is writable by creating missing dirs."""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
      os.makedirs(directory)

  @staticmethod
  def safe_write_to_file(file_path, contents):
    Dir.ensure_dir(file_path)
    with open(file_path, 'w', encoding='utf8') as f:
      f.write(contents)
