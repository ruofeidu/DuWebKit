import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scripts.utils.ducrawler import DuCrawler

if __name__ == '__main__':
  test_url = 'https://scholar.google.com/citations?user=mRI6AogAAAAJ'
  test_id = 'gsc_prf_pup-img'
  data = DuCrawler.download_image(
      test_url, 'scripts/utils/test_data/test.png', id=test_id)
  test_url = 'https://scholar.google.com/citations?user=9uxs6G4AAAAJ'
  data = DuCrawler.download_image(
      test_url, 'scripts/utils/test_data/test2.png', id=test_id)

  kwargs = {'class': 'pv-top-card-section__photo'}
  test_url = 'https://www.linkedin.com/in/ming-chuang-87aa921b/'
  data = DuCrawler.download_image(
      test_url, 'scripts/utils/test_data/test3.png', id='ember52')
