from constructs import Construct
from aws_cdk import (
    Stage
)
from event_bridge.infrastructure.core_event_bridge_stack import CoreEventBridgeStack


class CoreEventBridgeStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = CoreEventBridgeStack(self, 'CoreEventBridge')
