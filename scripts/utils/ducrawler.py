""" DuCrawler is a network finder and crawler.

"""
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os

DU_CRAWLER_HEADER = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
}

DU_CRAWLER_TIMEOUT = 2


class DuCrawler:

  @staticmethod
  def _request_bytes(url):
    res = requests.get(
        url, headers=DU_CRAWLER_HEADER, timeout=DU_CRAWLER_TIMEOUT)
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

  # Downloads an image into local filename. Returns if it is successful.
  @staticmethod
  def download_image(url, filename, **kwargs):
    src = DuCrawler.crawl_image(url, **kwargs)
    if src:
      data = DuCrawler._request_bytes(src)
      with open(filename, "wb") as f:
        f.write(data)
      return True
    return False

  # Downloads a file from url.
  @staticmethod
  def download_file(url, filename):
    data = DuCrawler._request_bytes(url)
    if not data:
      return False
    with open(filename, "wb") as f:
      f.write(data)
    return True
