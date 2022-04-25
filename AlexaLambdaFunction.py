#ask_sdk_core == 1.13.0

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name

import requests
import json
import smtplib

sb = SkillBuilder()
postAPI = "*"
updateAPI = "*"
getAPI = "*"
sheetLink = "*"



class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Welcome to the Age Intent Alexa skill")
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print(exception)
        handler_input.response_builder.speak("Please try again!!")
        return handler_input.response_builder.response



class testSaveIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("testSaveIntent")(handler_input)

    def handle(self, handler_input):
        item = handler_input.request_envelope.request.intent.slots['random'].value
        location = handler_input.request_envelope.request.intent.slots['loc'].value

        data = {
            "item": item,
            "location": location
        }
        response = requests.post(postAPI, json=(data))
        res = str(response.content)
        res = res.split(" ")

        if "already" in res:
            response = requests.post(updateAPI, json=(data))
            if response.status_code == 200:
                res =  f"Successfully updated the {item}'s location"
        else : res =  f"Successfully recorded the {item}'s location"       

        speech_text = f"{res}"
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class ResponseIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ResponseIntent")(handler_input)

    def handle(self, handler_input):
        item = handler_input.request_envelope.request.intent.slots['item'].value
        res = "Test"
        data = {
            "item":item
            }
        response = requests.get(getAPI, json=(data))
        res = (response.content)
        res = res.decode('utf-8')
        speech_text = f"{res}"
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class WorkoutIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return is_intent_name("WorkoutIntent")(handler_input)

    def handle(self, handler_input):
        exercise = handler_input.request_envelope.request.intent.slots['exercise'].value
        mins = handler_input.request_envelope.request.intent.slots['mins'].value
        name = handler_input.request_envelope.request.intent.slots['name'].value
        funcParam = f"{mins} mins of {exercise}"
        
        workoutAPI = "https://6lvazub0pj.execute-api.us-west-2.amazonaws.com/pr"
        data = {
            "exercise": funcParam,
            "name":name
        }
        response = requests.post(workoutAPI, json=(data))

         
        speech_text = f"Workout Sheet Updated"
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

class MailIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("MailIntent")(handler_input)

    def handle(self, handler_input):
        my_email = "**"
        password = "**"

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="**",
                msg=f"Subject:Workouts Sheet\n\n {sheetLink}."
        )

        speech_text = f"Check your inbox for link to workout file."
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(testSaveIntentHandler())
sb.add_request_handler(ResponseIntentHandler())
sb.add_request_handler(WorkoutIntentHandler())
sb.add_request_handler(MailIntentHandler())





sb.add_exception_handler(CatchAllExceptionHandler())


def lambda_handler(event, context):
    return sb.lambda_handler()(event, context)
