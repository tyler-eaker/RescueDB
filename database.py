import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class Database(object):
    """CRUD operations for the AAC MongoDB database using Environment Variables."""

    def __init__(self):
        """
        Initializes the connection to MongoDB Atlas.
        Exclusively uses the 'ATLAS_URI' environment variable.
        """
        # Load the connection string from environment variable
        self.atlas_uri = os.getenv('ATLAS_URI')
        
        # Security Check: Stop execution if the URI is missing
        if not self.atlas_uri:
            raise EnvironmentError(
                "CRITICAL ERROR: 'ATLAS_URI' environment variable not set. "
                "The application cannot connect to the database without a valid URI."
            )

        try:
            # Connect with a 5-second timeout to avoid long hangs
            self.client = MongoClient(self.atlas_uri, serverSelectionTimeoutMS=5000)
            # Verify connection
            self.client.admin.command('ping')
            self.database = self.client["AAC"]
        except ConnectionFailure:
            raise ConnectionError(
                "Failed to connect to MongoDB. Please verify your URI and "
                "ensure your IP is whitelisted in MongoDB Atlas Network Access."
            )

    def read(self, query=None):
        """Queries the 'animals' collection and returns a list of documents."""
        if query is None:
            query = {}
        try:
            return list(self.database.animals.find(query))
        except Exception as e:
            print(f"Error reading documents: {e}")
            return []

    def create(self, data):
        """Inserts a document into the 'animals' collection."""
        if data:
            try:
                result = self.database.animals.insert_one(data)
                return True if result.inserted_id else False
            except Exception as e:
                print(f"Error inserting: {e}")
        return False

    def update(self, query, new_values):
        """Updates documents matching the query."""
        if query and new_values:
            try:
                result = self.database.animals.update_one(query, {"$set": new_values})
                return result.modified_count > 0
            except Exception as e:
                print(f"Error updating: {e}")
        return False

    def delete(self, query):
        """Deletes a document matching the query."""
        if query:
            try:
                result = self.database.animals.delete_one(query)
                return result.deleted_count > 0
            except Exception as e:
                print(f"Error deleting: {e}")
        return False