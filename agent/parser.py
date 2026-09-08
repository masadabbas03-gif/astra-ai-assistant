import json


def parse_response(response):

    try:

        return json.loads(response)

    except:

        return {
            "type": "chat",
            "response": response
        }