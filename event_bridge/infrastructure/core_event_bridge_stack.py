from constructs import Construct
from aws_cdk import (
    Stack,
    aws_logs as logs,
    aws_events as events,
    aws_events_targets as target,
    aws_lambda as _lambda,
    Duration,
    aws_iam as iam,
    RemovalPolicy
)
import os


class CoreEventBridgeStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        ### Create Core Event Bus ###
        core_event_bus = events.EventBus(self,
                                         id='core-event-bus',
                                         event_bus_name='CoreEventBus'
                                         )

        ### Create Core Event Bus Archive ###
        core_event_bus.archive('CoreEventBusArchive',
                               archive_name='CoreEventBusArchive',
                               description='CoreEventBus Archive',
                               event_pattern=events.EventPattern(
                                   account=[Stack.of(self).account]
                               ),
                               retention=Duration.days(1)
                               )

        ### Creating Change Player Rule in Infrastructure, not sure if this ###
        ### should live somewhere else in the package structure ###
        player_api_event_rule = events.Rule(self, "player_api_event_rule",
                                         event_bus=core_event_bus,
                                         event_pattern=events.EventPattern(
                                             source=["ingest-api"],
                                             detail_type=["PLAYER"],
                                         )
                                        )

        extra_rule = events.Rule(self, "extra_rule",
                                         event_bus=core_event_bus,
                                         event_pattern=events.EventPattern(
                                             source=["extra"],
                                         )
                                        )

        player_api_event_rule.add_target(target.EventBus(
            events.EventBus.from_event_bus_arn(self,
                                               "player-event-bus",
                                               "arn:aws:events:us-east-1:{}:event-bus/PlayerEventBus".format(os.getenv(
                                                   'CDK_DEFAULT_ACCOUNT')))))

        event_bridge_log_group = logs.LogGroup(
            self, 
            "CoreEventBridgeLogs",
            removal_policy=RemovalPolicy.DESTROY,
            retention=logs.RetentionDays.ONE_DAY
        )

        logging_rule = events.Rule(
            self,
            "logging_rule",
            event_bus=core_event_bus,
            event_pattern={"account": [Stack.of(self).account]}
            )

        logging_rule.add_target(target.CloudWatchLogGroup(event_bridge_log_group, max_event_age=Duration.days(1)))
