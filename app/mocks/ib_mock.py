from ib_async import IB
import pickle


class MockIB(IB):
  def __init__(self, pickle_file=None):
    super().__init__()
    self.pickle_file = pickle_file
    self._positions = []
    if pickle_file:
      self._load_pickle_data()

  def _load_pickle_data(self):
    with open(self.pickle_file, "rb") as f:
      self._positions = pickle.load(f)

  def connect(self, *args, **kwargs):
    # Mock connection - always succeeds
    return True

  def positions(self):
    return self._positions
