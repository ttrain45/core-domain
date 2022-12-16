from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as python,
    aws_events as events,
)
from constructs import Construct


class StreamAddPlayerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### Stream Add Player Lambda ###
        stream_add_player = python.PythonFunction(self, "StreamAddPlayer",
                                            entry="player/lambda_function/runtime",  # required
                                            runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                            index="stream_add_player.py",  # optional, defaults to 'index.py'
                                            handler="handler",
                                            memory_size=256,
                                            function_name="StreamAddPlayer"
                                            )
        ### Update and grant invoke Lambda permission to this lambda ###
        ### from event bridge events ###
        principal = iam.ServicePrincipal("events.amazonaws.com")
        stream_add_player.grant_invoke(principal)

        ### Retrieve Core Event Bus from event bus name ###
        core_event_bus = events.EventBus.from_event_bus_name(
            self, "CoreEventBus", "CoreEventBus")

        ### Grant Ingest Api permissions for Core Event Bus put events ###
        core_event_bus.grant_put_events_to(stream_add_player)
