import boto3
import base64
import json

client = boto3.client('events')

def handler(event, context):
    print(event[0])

    for payload in event:
        print("Decoded payload: " + str(base64.b64decode(payload["data"])))

        add_player_entries = {
                'source': 'ingest-api',
                'detail-type': 'player',
                'detail': str(base64.b64decode(payload["data"])),
                'EventBusName': 'CoreEventBus'
            }

        print(add_player_entries)

        #client.put_events(
        #    Entries=add_player_entries
        #)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(add_player_entries)
        }