import pika
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import certifi
import pymongo
from pymongo.mongo_client import MongoClient

app = Flask(__name__)
uri = "mongodb+srv://dnmeghana2003:Meghanadevadiga@cluster0.wkexzw4.mongodb.net/test"
client = MongoClient(uri,tlsCAFile=certifi.where())
db = client['studentdb']
collection = db["student"]

print('Consumer_two connecting to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='insert_record', durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body)
    dict1 = {"SRN": data["SRN"],"Name":data["Name"],"Section":data["Section"]}
    collection.insert_one(dict1)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return "Student saved successfully!"
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='insert_record', on_message_callback=callback)
channel.start_consuming()

