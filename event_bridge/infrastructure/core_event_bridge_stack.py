from constructs import Construct
from aws_cdk import (
    Stack,
    aws_events as events,
    aws_events_targets as target,
    aws_lambda as _lambda,
    Duration,
    aws_iam as iam
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

        ### Creating Change Team Rule in Infrastructure, not sure if this ###
        ### should live somewhere else in the package structure ###
        change_team_rule = events.Rule(self, "change-team-rule",
                                       event_bus=core_event_bus,
                                       event_pattern=events.EventPattern(
                                           source=["ingest-api"],
                                           detail_type=["team"],
                                           detail={
                                               "eventName": ["ChangeTeamName"]
                                           },
                                       )
                                       )

        change_team_rule.add_target(target.EventBus(
            events.EventBus.from_event_bus_arn(self,
                                               "team-event-bus",
                                               "arn:aws:events:us-east-1:{}:event-bus/TeamEventBus".format(os.getenv(
                                                   'CDK_DEFAULT_ACCOUNT')))))

        ### Creating Change Player Rule in Infrastructure, not sure if this ###
        ### should live somewhere else in the package structure ###
        change_player_rule = events.Rule(self, "change-player-rule",
                                         event_bus=core_event_bus,
                                         event_pattern=events.EventPattern(
                                             source=["ingest-api"],
                                             detail_type=["player"],
                                             detail={
                                                 "eventName": ["ChangePlayerName"]
                                             },
                                         )
                                         )

        change_player_rule.add_target(target.EventBus(
            events.EventBus.from_event_bus_arn(self,
                                               "player-event-bus",
                                               "arn:aws:events:us-east-1:{}:event-bus/PlayerEventBus".format(os.getenv(
                                                   'CDK_DEFAULT_ACCOUNT')))))

        add_player_rule = events.Rule(self, "add-player-rule",
                                      event_bus=core_event_bus,
                                      event_pattern=events.EventPattern(
                                            source=["ingest-api"],
                                            detail_type=["player"],
                                            detail={
                                                "eventName": ["AddPlayer"]
                                            }
                                      )
                                      )

        add_player_rule.add_target(target.EventBus(events.EventBus.from_event_bus_name(
            self, "add-player-event-bus", "PlayerEventBus")))

        edit_player_rule = events.Rule(self, "edit-player-rule",
                                      event_bus=core_event_bus,
                                      event_pattern=events.EventPattern(
                                            source=["ingest-api"],
                                            detail_type=["player"],
                                            method=["PATCH"]
                                      )
                                      )

        edit_player_rule.add_target(target.EventBus(events.EventBus.from_event_bus_name(
            self, "edit-player-event-bus", "PlayerEventBus")))
