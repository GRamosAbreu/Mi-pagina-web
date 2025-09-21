from pymongo import MongoClient
# db_client = MongoClient().local

db_client = MongoClient("mongodb+srv://test:test@cluster0.onrq8l4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").base
