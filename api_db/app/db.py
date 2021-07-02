from databases import Database
from sqlalchemy import create_engine, MetaData
from app.config.app_config import get_settings
from app.util.singleton import Singleton


@Singleton
class DatabaseConnection:
    def __init__(self):
        settings = get_settings()
        self.engine = create_engine(settings.DB_URI)
        self.metadata = MetaData()
        self.metadata.create_all(self.engine)
        self.database = Database(settings.DB_URI)
