import sys
import json
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scripts.utils.autobib import *

DOI = '10.1145/3379337.3415881'
e = get_bibtex_entry(DOI)
print(e)

p = {}
p[e['doi']] = e

with open('scripts/utils/test_data/citations.json', 'w') as f:
  f.write(json.dumps(p, indent=2))

e = get_bibtex_entry(DOI)
print(e)
