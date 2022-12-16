import base64
import json

def handler(event, context):
    print(event[0])

    for payload in event:
        print("Decoded payload: " + str(base64.b64decode(payload["data"])))

        result = {
            "statusCode": 200,
            "source": "ingest-api",
            "detail-type": "player",
            "headers": {
                "Content-Type": "application/json"
            },
            "detail": json.loads(base64.b64decode(payload["data"]).decode("utf-8")),
        }

        print(result)

        return result