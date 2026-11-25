from pymongo import MongoClient
from pymongo.database import Database
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBConnection:
    _instance = None
    _client: MongoClient = None
    _db: Database = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish MongoDB connection"""
        try:
            self._client = MongoClient(settings.MONGODB_URL)
            self._db = self._client[settings.MONGODB_DB_NAME]
            # Test connection
            self._client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            self._initialize_collections()
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _initialize_collections(self):
        """Initialize required collections"""
        collections = [
            "employees",
            "projects",
            "tasks",
            "messages",
            "logs",
            "company_memory",
            "project_memory",
            "artifacts"
        ]
        
        existing_collections = self._db.list_collection_names()
        
        for collection in collections:
            if collection not in existing_collections:
                self._db.create_collection(collection)
                logger.info(f"Created collection: {collection}")
    
    def get_database(self) -> Database:
        """Get database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed")

# Global instance
mongodb = MongoDBConnection()