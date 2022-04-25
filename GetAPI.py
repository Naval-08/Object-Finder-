import json
from pymongo import MongoClient


def sendData(item):
    client = MongoClient(
    "**")

    db = client.get_database('alexa')

    table = db.skill

    post = {"item": item}
    
    db = []
    for data in table.find({},{ "item": 1, "location": 1, "_id":0}):
        db.append(data)


    for i in range(len(db)):
        t = db[i]
        if t["item"]==item:
            res = t["location"]
            return [True, res]

    else:
        return [False]
       
        
    



def lambda_handler(event, context):
    
    body=json.loads(event["body"])
    if not 'item' in body.keys():
        return {
            'statusCode': 404,
            'body': json.dumps('Error: Please specify the parameters (item).')
        }
    
    item = body["item"]

    res = sendData(item)
    if res[0] == True:
        return {
        "statusCode": 200,
        'headers': {
            "Content-Type" : "application/json",
            "Access-Control-Allow-Origin" : "*",
            "X-Requested-With" : "*"
        },
        "body": f"{item}'s location is {res[1]}"
    }
    elif res[0] == False:
        return {
        "statusCode": 200,
        'headers': {
            "Content-Type" : "application/json",
            "Access-Control-Allow-Origin" : "*",
            "X-Requested-With" : "*"
        },
        "body": f"The location of {item} is not in database"
    }
        
        

    
