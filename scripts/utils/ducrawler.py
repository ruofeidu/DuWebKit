""" DuCrawler is a high-level interface to crawl contents from the Internet."""
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
from scripts.utils.utils import Utils

DU_CRAWLER_HEADER = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
}

DU_CRAWLER_TIMEOUT_SECONDS = 5


class DuCrawler:

  @staticmethod
  def _request_bytes(url):
    res = requests.get(url,
                       headers=DU_CRAWLER_HEADER,
                       timeout=DU_CRAWLER_TIMEOUT_SECONDS)
    return res.content if res else ''

  @staticmethod
  def get_soup(url, header):
    return BeautifulSoup(
        requests.get(url, headers=header).content, 'html.parser')

  @staticmethod
  def get_soup_by_text(html_content):
    return BeautifulSoup(html_content, 'html.parser')

  @staticmethod
  def crawl(url, element, **kwargs):
    soup = DuCrawler.get_soup(url, DU_CRAWLER_HEADER)
    res = soup.find(element, **kwargs)
    base = os.path.dirname(url)
    print(res)

    if not res or not res['src']:
      return ''
    return urljoin(base, res['src']) if res else ''

  @staticmethod
  def crawl_image(url, **kwargs):
    return DuCrawler.crawl(url, 'img', **kwargs)

  @staticmethod
  def download_image(url, filename, **kwargs):
    """Downloads an image into local filename. Returns if it is successful."""
    src = DuCrawler.crawl_image(url, **kwargs)
    if src:
      data = DuCrawler._request_bytes(src)
      with open(Utils.file_nameable(filename), 'wb') as f:
        f.write(data)
      return True
    return False

  @staticmethod
  def download_file(url, filename):
    """Downloads a file from URL."""
    try:
      data = DuCrawler._request_bytes(url)
      if not data:
        return False
      with open(Utils.file_nameable(filename), 'wb') as f:
        f.write(data)
    except:
      print('An exception occurred with ' + url)
      return False
    return True
