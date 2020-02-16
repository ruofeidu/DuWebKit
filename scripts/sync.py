from scripts.utils import gsheets
from scripts.papers import Papers
from scripts.people import People
from scripts.arts import Arts
from scripts.data import Data


class Sync:
  service = None
  publication = ''
  people = ''

  def run(self):
    if not self.service:
      self.service = gsheets.get_service()

    rows = gsheets.get_people(self.service, self.people)
    Data.people = People(rows)

    rows = gsheets.get_publications(self.service, self.publication)
    Data.papers = Papers(rows)

    rows = gsheets.get_arts(self.service, self.publication)
    Data.arts = Arts(rows)
    pass
