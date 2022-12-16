import base64
import json

def handler(event, context):
    print(event[0])

    for payload in event:
        print("Decoded payload: " + str(base64.b64decode(payload["data"])))

        decoded_payload_string = base64.b64decode(payload["data"])
        print(decoded_payload_string.decode("utf-8"))

        add_player_entries = {
                "source": "ingest-api",
                "detail-type": "player",
                "detail": decoded_payload_string
            }

        print(json.dumps(add_player_entries))

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(add_player_entries)
        }