from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_auto_scaling_connector.schema.data import AutoScalingGroup, LaunchConfiguration
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout, \
    SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
AUTO SCALING GROUP
'''
# TAB - AutoScaling
asg_meta_autoscaling = ItemDynamicLayout.set_fields('Auto Scaling', fields=[
    TextDyField.data_source('Name', 'data.auto_scaling_group_name'),
    TextDyField.data_source('Launch Configuration', 'data.launch_configuration_name'),
    TextDyField.data_source('ARN', 'data.auto_scaling_group_arn'),
    TextDyField.data_source('Desired Capacity', 'data.desired_capacity'),
    TextDyField.data_source('Min Size', 'data.min_size'),
    TextDyField.data_source('Max Size', 'data.max_size'),
    TextDyField.data_source('Default CoolDown', 'data.default_cooldown'),
    ListDyField.data_source('Availability Zones', 'data.availability_zones', default_badge={'type': 'outline'}),
    EnumDyField.data_source('Health Check Type', 'data.health_check_type', default_outline_badge=['EC2', 'ELB']),
    TextDyField.data_source('Health Check Grace Period', 'data.health_check_grace_period'),
    TextDyField.data_source('Service Linked Role ARN', 'data.service_linked_role_arn'),
    ListDyField.data_source('Target Group ARNs', 'data.target_group_arns'),
    ListDyField.data_source('Load Balancer Names', 'data.load_balancer_names'),
    BadgeDyField.data_source('Termination Policies', 'data.termination_policies'),
    DateTimeDyField.data_source('Creation Time', 'data.created_time'),
])

# TAB - Launch Configuration
asg_meta_lc = ItemDynamicLayout.set_fields('Launch Configuration', fields=[
    TextDyField.data_source('Name', 'data.launch_configuration.launch_configuration_name'),
    TextDyField.data_source('ARN', 'data.launch_configuration.launch_configuration_arn'),
    TextDyField.data_source('AMI', 'data.launch_configuration.image_id'),
    TextDyField.data_source('Instance Type', 'data.launch_configuration.instance_type'),
    EnumDyField.data_source('Monitoring', 'data.launch_configuration.instance_monitoring.enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('IAM Instance Profile', 'data.launch_configuration.iam_instance_profile'),
    TextDyField.data_source('Kernel ID', 'data.launch_configuration.kernel_id'),
    ListDyField.data_source('Security Groups', 'data.launch_configuration.security_groups',
                            default_badge={'type': 'outline'}),
    TextDyField.data_source('Spot Price', 'data.launch_configuration.kernel_id'),
    TextDyField.data_source('RAM Disk ID', 'data.launch_configuration.ramdisk_id'),
    EnumDyField.data_source('EBS Optimized', 'data.launch_configuration.ebs_optimized', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Creation Time', 'data.launch_configuration.created_time'),
])

# TAB - Instance
asg_meta_instance = TableDynamicLayout.set_fields('Instances', 'data.instances', fields=[
    TextDyField.data_source('Instance ID', 'instance_id'),
    EnumDyField.data_source('Lifecycle', 'lifecycle_state', default_state={
        'safe': ['InService'],
        'available': ['Standby'],
        'warning': ['Pending', 'Pending:Wait', 'Pending:Proceed', 'Quarantined', 'Detaching', 'EnteringStandby',
                    'Terminating', 'Terminating:Wait', 'Terminating:Proceed'],
        'disable': ['Detached'],
        'alert': ['Terminated']
    }),
    TextDyField.data_source('Instance Type', 'instance_type'),
    TextDyField.data_source('AZ', 'availability_zone'),
    EnumDyField.data_source('Health Status', 'health_status', default_state={
        'safe': ['Healthy'], 'alert': ['Unhealthy']
    }),
    EnumDyField.data_source('Protected from Scale In', 'protected_from_scale_in', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Weighted Capacity', 'weighted_capacity'),
])

# TAB - Policy
asg_meta_policy = TableDynamicLayout.set_fields('Policies', 'data.policies', fields=[
    TextDyField.data_source('Policy Name', 'policy_name'),
    TextDyField.data_source('Policy Type', 'policy_type'),
    EnumDyField.data_source('Enabled', 'enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Metric Type (Predefined)',
                            'target_tracking_configuration.predefined_metric_specification.predefined_metric_type)'),
    TextDyField.data_source('Target Value', 'target_tracking_configuration.target_value'),
    EnumDyField.data_source('Disable Scale In', 'target_tracking_configuration.disable_scale_in', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

# TAB - Notification
asg_meta_notification = TableDynamicLayout.set_fields('Notifications', 'data.notification_configurations', fields=[
    TextDyField.data_source('Topic ARN', 'topic_arn'),
    TextDyField.data_source('Notification Type', 'notification_type'),
])

# TAB - Scheduled Action
asg_meta_scheduled_action = TableDynamicLayout.set_fields('Scheduled Actions', 'data.scheduled_actions', fields=[
    TextDyField.data_source('Name', 'scheduled_action_name'),
    TextDyField.data_source('Recurrence', 'recurrence'),
    TextDyField.data_source('Desired Capacity', 'desired_capacity'),
    TextDyField.data_source('Min', 'min_size'),
    TextDyField.data_source('Max', 'max_size'),
    DateTimeDyField.data_source('Start Time', 'start_time'),
    DateTimeDyField.data_source('End Time', 'end_time'),
])

# TAB - Lifecycle Hooks
asg_meta_lifecycle_hooks = TableDynamicLayout.set_fields('Lifecycle Hooks', 'data.lifecycle_hooks', fields=[
    TextDyField.data_source('Name', 'lifecycle_hook_name'),
    TextDyField.data_source('Lifecycle Transaction', 'lifecycle_transition'),
    TextDyField.data_source('Default Result', 'default_result'),
    TextDyField.data_source('Heartbeat Timeout (Seconds)', 'heartbeat_timeout'),
    TextDyField.data_source('Notification Target ARN', 'notification_target_arn'),
    TextDyField.data_source('Role ARN', 'role_arn'),
])

# TAB - Tags
asg_meta_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
    EnumDyField.data_source('Tag New Instances', 'propagate_at_launch', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])
asg_meta = CloudServiceMeta.set_layouts([asg_meta_autoscaling, asg_meta_lc, asg_meta_instance, asg_meta_policy,
                                         asg_meta_notification, asg_meta_scheduled_action, asg_meta_lifecycle_hooks,
                                         asg_meta_tags])


'''
LAUNCH CONFIGURATION
'''
# TAB - BASE - Launch Configuration
lc_meta_base_lc = ItemDynamicLayout.set_fields('Launch Configuration', fields=[
    TextDyField.data_source('Name', 'data.launch_configuration_name'),
    TextDyField.data_source('ARN', 'data.launch_configuration_arn'),
    TextDyField.data_source('AMI', 'data.image_id'),
    TextDyField.data_source('Instance Type', 'data.instance_type'),
    EnumDyField.data_source('Monitoring', 'data.instance_monitoring.enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('IAM Instance Profile', 'data.iam_instance_profile'),
    TextDyField.data_source('Kernel ID', 'data.kernel_id'),
    ListDyField.data_source('Security Groups', 'data.security_groups', default_badge={'type': 'outline'}),
    TextDyField.data_source('Spot Price', 'data.kernel_id'),
    TextDyField.data_source('RAM Disk ID', 'data.ramdisk_id'),
    EnumDyField.data_source('EBS Optimized', 'data.ebs_optimized', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Creation Time', 'data.created_time'),
])

# TAB - BASE - Block Devices
lc_meta_base_bd = SimpleTableDynamicLayout.set_fields('Block Devices', 'data.block_device_mappings', fields=[
    TextDyField.data_source('Device Name', 'device_name'),
    EnumDyField.data_source('Type', 'ebs.volume_type', default_outline_badge=['standard', 'io1', 'gp2', 'st1', 'sc1']),
    TextDyField.data_source('Size(GB)', 'ebs.volume_size'),
    TextDyField.data_source('IOPS', 'ebs.iops'),
    EnumDyField.data_source('Delete on Termination', 'data.delete_on_termination', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Encrypted', 'data.encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

lc_meta = CloudServiceMeta.set_layouts([lc_meta_base_lc, lc_meta_base_bd, ])


class AutoScalingResource(CloudServiceResource):
    cloud_service_group = StringType(default='AutoScaling')


class AutoScalingGroupResource(AutoScalingResource):
    cloud_service_type = StringType(default='AutoScalingGroup')
    data = ModelType(AutoScalingGroup)
    _metadata = ModelType(CloudServiceMeta, default=asg_meta, serialized_name='metadata')


class LaunchConfigurationResource(AutoScalingResource):
    cloud_service_type = StringType(default='LaunchConfiguration')
    data = ModelType(LaunchConfiguration)
    _metadata = ModelType(CloudServiceMeta, default=lc_meta, serialized_name='metadata')


class AutoScalingGroupResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.auto_scaling_group_arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(AutoScalingGroupResource)


class LaunchConfigurationResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.launch_configuration_arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(LaunchConfigurationResource)
