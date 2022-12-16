from constructs import Construct
from aws_cdk import (
    Stage
)
from player.lambda_function.infrastructure.stream_add_player_stack import StreamAddPlayerStack


class StreamAddPlayerStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = StreamAddPlayerStack(self, 'StreamAddPlayerStack')
