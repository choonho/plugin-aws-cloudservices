import time
import logging
from typing import List

from spaceone.inventory.connector.aws_auto_scaling_connector.schema.data import AutoScalingGroup, LaunchConfiguration, \
    AutoScalingPolicy, LifecycleHook, NotificationConfiguration, ScheduledAction
from spaceone.inventory.connector.aws_auto_scaling_connector.schema.resource import AutoScalingGroupResource, \
    LaunchConfigurationResource, AutoScalingGroupResponse, LaunchConfigurationResponse
from spaceone.inventory.connector.aws_auto_scaling_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class AutoScalingConnector(SchematicAWSConnector):
    _launch_configurations = None

    service_name = 'autoscaling'

    def get_resources(self):
        print("** Auto Scaling Start **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_launch_configuration_data,
                'resource': LaunchConfigurationResource,
                'response_schema': LaunchConfigurationResponse
            },
            {
                'request_method': self.request_auto_scaling_group_data,
                'resource': AutoScalingGroupResource,
                'response_schema': AutoScalingGroupResponse
            },
        ]

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            # print(f'[ AutoScaling {region_name} ]')
            self._launch_configurations = []
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' Auto Scaling Finished {time.time() - start_time} Seconds')
        return resources

    def request_auto_scaling_group_data(self, region_name) -> List[AutoScalingGroup]:
        paginator = self.client.get_paginator('describe_auto_scaling_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        policies = None
        notification_configurations = None

        for data in response_iterator:
            for raw in data.get('AutoScalingGroups', []):

                if policies is None:
                    policies = self._describe_policies()

                if notification_configurations is None:
                    notification_configurations = self._describe_notification_configurations()

                match_lc = self._match_launch_configuration(raw.get('LaunchConfigurationName', ''))
                match_policies = self._match_policies(policies, raw.get('AutoScalingGroupName'))
                match_noti_confs = self._match_notification_configuration(notification_configurations,
                                                                          raw.get('AutoScalingGroupName'))

                raw.update({
                    'launch_configuration': LaunchConfiguration(match_lc, strict=False),
                    'policies': list(map(lambda policy: AutoScalingPolicy(policy, strict=False), match_policies)),
                    'notification_configurations': list(map(lambda noti_conf: NotificationConfiguration(noti_conf,
                                                                                                        strict=False),
                                                            match_noti_confs)),
                    'scheduled_actions': list(map(lambda scheduled_action: ScheduledAction(scheduled_action,
                                                                                           strict=False),
                                                  self._describe_scheduled_actions(raw['AutoScalingGroupName']))),
                    'lifecycle_hooks': list(map(lambda lifecycle_hook: LifecycleHook(lifecycle_hook, strict=False),
                                                self._describe_lifecycle_hooks(raw['AutoScalingGroupName']))),
                    'region_name': region_name,
                    'account_id': self.account_id
                })
                res = AutoScalingGroup(raw, strict=False)
                yield res

    def request_launch_configuration_data(self, region_name) -> List[LaunchConfiguration]:
        paginator = self.client.get_paginator('describe_launch_configurations')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('LaunchConfigurations', []):
                raw.update({
                    'region_name': region_name,
                    'account_id': self.account_id
                })
                res = LaunchConfiguration(raw, strict=False)
                self._launch_configurations.append(res)
                yield res

    def _match_launch_configuration(self, lc):
        return next((launch_configuration for launch_configuration in self._launch_configurations
                     if launch_configuration.launch_configuration_name == lc), '')

    @staticmethod
    def _match_policies(policies, asg_name):
        match_policies = []

        for _policy in policies:
            if _policy['AutoScalingGroupName'] == asg_name:
                match_policies.append(_policy)

        return match_policies

    @staticmethod
    def _match_notification_configuration(notification_configurations, asg_name):
        match_noti_confs = []

        for _noti_conf in notification_configurations:
            if _noti_conf['AutoScalingGroupName'] == asg_name:
                match_noti_confs.append(_noti_conf)

        return match_noti_confs

    @staticmethod
    def _match_lifecycle_hook(lifecycle_hooks, asg_name):
        match_lifecycle_kooks = []

        for _lifecycle_hook in lifecycle_hooks:
            if _lifecycle_hook['AutoScalingGroupName'] == asg_name:
                match_lifecycle_kooks.append(_lifecycle_hook)

        return match_lifecycle_kooks

    def _describe_launch_configuration(self):
        res = self.client.describe_launch_configurations()
        return res.get('LaunchConfigurations', [])

    def _describe_policies(self):
        res = self.client.describe_policies()
        return res.get('ScalingPolicies', [])

    def _describe_lifecycle_hooks(self, auto_scaling_group_name):
        res = self.client.describe_lifecycle_hooks(AutoScalingGroupName=auto_scaling_group_name)
        return res.get('LifecycleHooks', [])

    def _describe_notification_configurations(self):
        res = self.client.describe_notification_configurations()
        return res.get('NotificationConfigurations', [])

    def _describe_scheduled_actions(self, auto_scaling_group_name):
        res = self.client.describe_scheduled_actions(AutoScalingGroupName=auto_scaling_group_name)
        return res.get('ScheduledUpdateGroupActions', [])