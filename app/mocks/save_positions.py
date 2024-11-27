import pickle
from ib_async import IB


def save_positions_to_pickle():
  ib = IB()
  ib.connect(host="localhost", port=8888, clientId=1001)

  positions = ib.positions()

  with open("./data/positions.pickle", "wb") as f:
    pickle.dump(positions, f)

  ib.disconnect()


if __name__ == "__main__":
  save_positions_to_pickle()
