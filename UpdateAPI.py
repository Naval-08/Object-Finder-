import json
from pymongo import MongoClient


def sendData(item, location):
    client = MongoClient(
    "**")

    db = client.get_database('alexa')

    table = db.skill
    newvalues = { "$set": { "item":item, "location":location}}

    post = {"item": item}

    if not len(list(table.find({'item':post["item"]}))) == 0:
        table.update_one(post, newvalues)
        return True
    else :
        return False
       
        
    
def lambda_handler(event, context):
    
    body=json.loads(event["body"])
    if not 'item' in body.keys() or not 'location' in body.keys():
        return {
            'statusCode': 404,
            'body': json.dumps('Error: Please specify the parameters (item & location).')
        }
    
    item = body["item"]
    location = body["location"]

    res = sendData(item, location)
    if res == True:
        return {
        "statusCode": 200,
        'headers': {
            "Content-Type" : "application/json",
            "Access-Control-Allow-Origin" : "*",
            "X-Requested-With" : "*"
        },
        "body": f"{item} location Updated"
    }
    else:
        return {
        "statusCode": 200,
        'headers': {
            "Content-Type" : "application/json",
            "Access-Control-Allow-Origin" : "*",
            "X-Requested-With" : "*"
        },
        "body": f"{item} not found"
    }
        
        

    
