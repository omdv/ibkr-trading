from pathlib import Path
from sqlmodel import create_engine, Session, SQLModel

from settings import Settings


class DB:
  """Database connection manager"""

  def __init__(self, config: Settings, echo: bool = False):
    self.db_file = Path(config.storage_path)
    self.echo = echo
    self._engine = None

  @property
  def engine(self):
    """Lazy initialization of database engine"""
    if self._engine is None:
      self._engine = create_engine(f"sqlite:///{self.db_file}", echo=self.echo)
      SQLModel.metadata.create_all(self._engine)

    return self._engine

  def get_session(self) -> Session:
    """Get a new database session"""
    return Session(self.engine)
