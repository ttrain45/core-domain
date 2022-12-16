import base64
import json

def handler(event, context):
    print(event[0])

    for payload in event:
        print("Decoded payload: " + str(base64.b64decode(payload["data"])))

        add_player_entries = {
                "source": "ingest-api",
                "detail-type": "player",
                "detail": json.loads(base64.b64decode(payload["data"]).decode("utf-8"))
            }

        print(json.dumps(add_player_entries))

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": add_player_entries
        }