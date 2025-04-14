from pymongo.mongo_client import MongoClient
import  certifi

uri  =  "mongodb+srv://jpinzav:3ZC3qZqGqFFNdSXN@cluster01.wzgwg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01"
client  =  MongoClient(uri, tlsCAFile=certifi.where())

db  =  client.user
collection  =  db["nube_casera_users"]