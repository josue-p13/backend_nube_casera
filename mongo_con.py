from pymongo.mongo_client import MongoClient
import  certifi

uri  =  "ruta a tu db, casi dejo la mia xdddddddd"
client  =  MongoClient(uri, tlsCAFile=certifi.where())

db  =  client.user
collection  =  db["nube_casera_users"]
