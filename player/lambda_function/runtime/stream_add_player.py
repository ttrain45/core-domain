import boto3
import base64

client = boto3.client('events')

def lambda_handler(event, context):
    print(event[0])

    for payload in event:
        print("Decoded payload: " + str(base64.b64decode(payload["data"])))

        add_player_entries = [
            {
                'Source': 'ingest-api',
                'DetailType': 'team',
                'Detail': payload["data"],
                'EventBusName': 'CoreEventBus'
            },
        ]

        print(add_player_entries)

        client.put_events(
            Entries=add_player_entries
        )