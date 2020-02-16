""" DuMark is a helper class for Markdown parser to provide customized Markdown sentence.

"""
from scripts.utils.constants import FACEBOOK, LINKEDIN, SCHOLAR, TWITTER, MAILTO, VIMEO, GITHUB, INSTAGRAM, YOUTUBE, RESEARCH_GATE, GOOGLE_SEARCH
from scripts.utils.utils import Utils
from scripts.app import App


class DuMark:
  LINK2 = '[%s](%s)'
  LINK3 = '[%s](%s "%s")'
  IMAGE2 = '![%s](%s)'
  IMAGE3 = '![%s](%s "%s")'
  CODE = '\n```%s\n%s\n```\n'
  TABLE_VERTICAL = '|'
  TABLE_HORIZONTAL = '---'
  QUOTE = '> '
  HORIZONTAL_LINE = '---'

  @staticmethod
  def get_url(url, title, description=None):
    if url:
      url = Utils.filter_url(url)
      return DuMark.LINK3 % (title, url, description
                            ) if description else DuMark.LINK2 % (title, url)
    else:
      return ''

  @staticmethod
  def get_h1(title):
    return '\n# %s\n' % title

  @staticmethod
  def get_h2(title):
    return '\n## %s\n' % title

  @staticmethod
  def get_h3(title):
    return '\n### %s\n' % title

  @staticmethod
  def get_h4(title):
    return '\n#### %s\n' % title

  @staticmethod
  def get_h5(title):
    return '\n##### %s\n' % title

  @staticmethod
  def get_image(url, title, description=None):
    if url:
      return DuMark.IMAGE3 % (title, url, description
                             ) if description else DuMark.IMAGE2 % (title, url)
    else:
      return ''

  @staticmethod
  def get_paper(filename, title=None, description=None):
    if len(filename) < 2:
      return ''
    return DuMark.get_url('%spapers/%s.pdf' % (App.root, filename),
                          title if title else 'Paper', description)

  @staticmethod
  def get_website(website, title=None):
    if len(website) < 4:
      return ''
    if (website[:4] != 'http'):
      website = 'http://' + website
    return DuMark.get_url(website, title if title else 'Website')

  @staticmethod
  def get_facebook(username, title=None):
    return DuMark.get_url(
        Utils.get_url(FACEBOOK, username), title if title else 'Facebook')

  @staticmethod
  def get_linkedin(username, title=None):
    return DuMark.get_url(
        Utils.get_url(LINKEDIN, username), title if title else 'LinkedIn')

  @staticmethod
  def get_scholar(user, title=None):
    return DuMark.get_url(
        Utils.get_url(SCHOLAR, user), title if title else 'Scholar')

  @staticmethod
  def get_twitter(username, title=None):
    return DuMark.get_url(
        Utils.get_url(TWITTER, username), title if title else 'Twitter')

  @staticmethod
  def get_vimeo(username, title=None):
    return DuMark.get_url(
        Utils.get_url(VIMEO, username), title if title else 'Vimeo')

  @staticmethod
  def get_youtube(username, title=None):
    return DuMark.get_url(
        Utils.get_url(YOUTUBE, username), title if title else 'Youtube')

  @staticmethod
  def get_instagram(username, title=None):
    return DuMark.get_url(
        Utils.get_url(INSTAGRAM, username), title if title else 'Instagram')

  @staticmethod
  def get_github(username, title=None):
    return DuMark.get_url(
        Utils.get_url(GITHUB, username), title if title else 'Github')

  @staticmethod
  def get_researchgate(username, title=None):
    return DuMark.get_url(
        Utils.get_url(RESEARCH_GATE, username),
        title if title else 'ResearchGate')

  @staticmethod
  def get_email(username, title=None):
    return DuMark.get_url(
        Utils.get_url(MAILTO, username), title if title else 'Email')

  @staticmethod
  def get_google(query):
    return DuMark.get_url(Utils.get_url(GOOGLE_SEARCH, query), query)
