from pymongo import MongoClient
from pymongo.server_api import ServerApi
from app.core.config import settings

class MongoDB:
    client: MongoClient = None
    db = None

    def connect(self):
        try:
            self.client = MongoClient(settings.MONGODB_URL, server_api=ServerApi('1'))
            self.db = self.client[settings.DATABASE_NAME]
            # Verify connection
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Connection failed: {e}")
            raise e

    def close(self):
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")

db = MongoDB()
