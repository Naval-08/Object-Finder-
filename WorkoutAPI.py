import json
import random
import requests
import datetime as dt


def nutro(exercise,name):
    APP_ID = "**"
    API_KEY = "**"

    nutronix_header = {
        "x-app-id":APP_ID,
        "x-app-key":API_KEY
    }

    nutronix_endpoint = "**"
    sheet_endpoint = "**"

    params = {
        "query":exercise,
    }

    exercise_response = requests.post(url=nutronix_endpoint, json=params, headers=nutronix_header)
    exercise_response.raise_for_status()
    exer = exercise_response.json()
    
    sheetRes = ""
    for exercise in exer["exercises"]:
        sheet_inputs = {
            "workout": {
                "date": str(dt.datetime.now().date()),
                "time": dt.datetime.now().strftime("%X"),
                "exercise": exercise["name"].title(),
                "calories": exercise["nf_calories"],
                "name":name
            }
        }

        sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)
        sheetRes = (sheet_response.status_code)
        
    return (sheetRes)

def lambda_handler(event, context):

    if not 'exercise' in event:
        return {
            'statusCode': 200,
            'body': json.dumps('Error: Please specify the parameters (exercise).')
        }

    nutro_status_code = nutro(event['exercise'],event['name'])

    return {
        'statusCode': 200,
        'body': nutro_status_code
    }
