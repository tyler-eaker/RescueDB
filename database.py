# Artifact Three - database.py
# Tyler Eaker
# SNHU CS-499
# December 2025

import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

# FIXED: Renamed class from AnimalShelter to Database to match your notebook import
class Database(object):
    # CRUD operations for the database using MongoDB.

    def __init__(self, username, password):
        # Initialize the MongoClient and connect to the database.
        # Loads the connection string from an environment variable for security.
        #
        # params:
        #   username: Not used in the current Atlas URI but retained for structure.
        #   password: Not used in the current Atlas URI but retained for structure.
        
        # 1. Attempt to load the connection string from the environment variable
        # The key we are looking for is 'ATLAS_URI'
        atlas_uri = os.getenv('ATLAS_URI')
        
        # 2. If the environment variable is not set, use the hardcoded string as a fallback.
        # IMPORTANT: In a production environment, you should raise an error here 
        # instead of providing a fallback, to ensure security is maintained.
        if not atlas_uri:
            print("WARNING: ATLAS_URI environment variable not found. Using hardcoded URI.")
            # Fallback hardcoded Atlas connection string
            atlas_uri = "mongodb+srv://tylerjameseaker_db_user:6djpBLADk9kZ8NOo@cluster0.mxat9xk.mongodb.net/?retryWrites=true&w=majority"

        # Establish connection to the MongoDB cluster
        self.client = MongoClient(atlas_uri)

        # Select the 'AAC' database (created automatically if it doesn't exist)
        self.database = self.client["AAC"]

    def create(self, data):
        # Inserts a new document into the 'animals' collection.
        #
        # params:
        #   data: A dictionary containing the document to insert.
        # return: 
        #   True if insert is successful, else False.
        
        if data is not None:
            try:
                # Validate data before insertion to ensure data integrity
                data = self.validate_document(data)
                
                # Insert document into the 'animals' collection
                result = self.database.animals.insert_one(data)
                
                # Return True if an ID was assigned (successful insert)
                return True if result.inserted_id else False
            except Exception as e:
                print("Error inserting document:", e)
                return False
        else:
            return False

    def read(self, query=None):
        # Queries the 'animals' collection.
        #
        # params:
        #   query: A dictionary containing the key/value pairs to search for.
        #          Defaults to empty dict (returns all).
        # return: 
        #   A list of dictionaries (documents), or an empty list on failure.

        if query is None:
            query = {}

        try:
            # Check for unsafe characters/operators
            query = self.sanitize_query(query)
            
            # Execute find(), convert the cursor to a list, and return result
            data = list(self.database.animals.find(query))
            return data
        except Exception as e:
            print("Error reading documents:", e)
            return []
    
    def update(self, query, new_values):
        # Updates a document in the 'animals' collection.
        #
        # params:
        #   query: The search criteria to find the document(s).
        #   new_values: The dictionary of fields to update.
        # return: 
        #   True if a document was modified, else False.

        if query is None or new_values is None:
            return False

        try:
            query = self.sanitize_query(query)
            
            # $set operator is used to update only specific fields without overwriting the whole doc
            result = self.database.animals.update_one(query, {"$set": new_values})
            
            # Return True if at least one document was modified
            return result.modified_count > 0
        except Exception as e:
            print("Error updating document:", e)
            return False

    def delete(self, query):
        # Deletes a document from the 'animals' collection.
        #
        # params:
        #   query: The search criteria to find the document to delete.
        # return: 
        #   True if a document was deleted, else False.

        if query is None:
            return False

        try:
            query = self.sanitize_query(query)
            
            # Delete the first document matching the query
            result = self.database.animals.delete_one(query)
            
            # Return True if the count of deleted items is > 0
            return result.deleted_count > 0
        except Exception as e:
            print("Error deleting document:", e)
            return False

    def analytics(self):
        # Returns aggregated statistics grouped by animal type.
        #
        # Calculates:
        #   - total animals per type
        #   - average age per type
        #   - list of outcome types associated with that animal type

        try:
            # MongoDB Aggregation Pipeline
            pipeline = [
                {
                    # Group documents by the 'type' field (e.g., Dog, Cat)
                    "$group": {
                        "_id": "$type", 
                        "total_animals": {"$sum": 1},      # Count occurrences
                        "average_age": {"$avg": "$age"},   # Average the age field
                        "outcomes": {"$addToSet": "$outcome_type"} # Collect unique outcomes
                    }
                },
                {
                    # Sort results by total_animals in descending order (-1)
                    "$sort": {"total_animals": -1}
                }
            ]

            results = list(self.database.animals.aggregate(pipeline))
            return results

        except Exception as e:
            print("Error running analytics:", e)
            return []
    
    def sanitize_query(self, query):
        # Security Utility: Prevents the use of dangerous MongoDB operators.
        #
        # params:
        #   query: The query dictionary.
        # return: 
        #   The query if safe, raises ValueError otherwise.

        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary.")

        # Iterate over keys to ensure no injection attacks (keys starting with $)
        for key in query.keys():
            if key.startswith("$"):
                raise ValueError("Unsafe query operator detected.")

        return query

    def validate_document(self, doc):
        # Validation Utility: Ensures required fields exist and data types are correct.
        #
        # params:
        #   doc: The document dictionary to check.
        # return: 
        #   The document if valid, raises ValueError otherwise.

        required = ["name", "type", "age"]
        
        # Check for presence of keys
        for field in required:
            if field not in doc:
                raise ValueError(f"Missing required field: {field}")

        # Check age logic
        if not isinstance(doc["age"], int) or doc["age"] < 0:
            raise ValueError("Age must be a positive integer.")

        return doc