from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

'''
CONNECTION
'''
cst_connection = CloudServiceTypeResource()
cst_connection.name = 'Connection'
cst_connection.provider = 'aws'
cst_connection.group = 'DirectConnect'
cst_connection.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
    'spaceone:is_major': 'true',
}

cst_connection_meta = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Id', 'data.connection_id'),
        TextDyField.data_source('Name', 'data.connection_name'),
        EnumDyField.data_source('State', 'data.connection_state', default_state={
            'safe': ['available'],
            'available': ['requested'],
            'alert': ['down', 'rejected'],
            'warning': ['ordering', 'pending', 'deleting'],
            'disable': ['unknown', 'deleted']
        }),
        TextDyField.data_source('Region', 'data.region'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Bandwidth', 'data.bandwidth'),
    ],
    search=[
        SearchField.set(name='Connection ID', key='data.connection_id'),
        SearchField.set(name='Name', key='data.connection_name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='State', key='data.connection_state',
                        enums={'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                               'requested': {'label': 'Requested', 'icon': {'color': 'blue.400'}},
                               'down': {'label': 'Down', 'icon': {'color': 'red.500'}},
                               'rejected': {'label': 'Rejected', 'icon': {'color': 'red.500'}},
                               'ordering': {'label': 'Ordering', 'icon': {'color': 'yellow.500'}},
                               'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                               'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                               'unknown': {'label': 'Unknown', 'icon': {'color': 'gray.400'}},
                               'deleted': {'label': 'Deleted', 'icon': {'color': 'gray.400'}}
                               }),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Vlan', key='data.vlan'),
        SearchField.set(name='Partner Name', key='data.partner_name'),
        SearchField.set(name='Lag ID', key='data.lag_id'),
        SearchField.set(name='AWS Device', key='data.aws_device'),
        SearchField.set(name='Provider Name', key='data.provider_name'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)
cst_connection._metadata = cst_connection_meta

'''
DIRECT CONNECT GATEWAY
'''
cst_dc_gw = CloudServiceTypeResource()
cst_dc_gw.name = 'DirectConnectGateway'
cst_dc_gw.provider = 'aws'
cst_dc_gw.group = 'DirectConnect'
cst_dc_gw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
    'spaceone:is_major': 'false',
}
cst_dc_gw_meta = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Id', 'data.direct_connect_gateway_id'),
        TextDyField.data_source('Name', 'data.direct_connect_gateway_name'),
        EnumDyField.data_source('State', 'data.direct_connect_gateway_state', default_state={
            'safe': ['available'],
            'disable': ['deleted'],
            'warning': ['pending', 'deleting']
        }),
    ],
    search=[
        SearchField.set(name='Direct Connect Gateway ID', key='data.direct_connect_gateway_id'),
        SearchField.set(name='Name', key='data.direct_connect_gateway_name'),
        SearchField.set(name='State', key='data.direct_connect_gateway_state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'gray.400'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}}
                        }),
        SearchField.set(name='Amazon Side ASN', key='data.amazon_side_asn'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)
cst_dc_gw._metadata = cst_dc_gw_meta


'''
VIRTUAL PRIVATE GATEWAY
'''
cst_vp_gw = CloudServiceTypeResource()
cst_vp_gw.name = 'VirtualPrivateGateway'
cst_vp_gw.provider = 'aws'
cst_vp_gw.group = 'DirectConnect'
cst_vp_gw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
    'spaceone:is_major': 'false',
}
cst_vp_gw_meta = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Id', 'data.virtual_gateway_id'),
        EnumDyField.data_source('State', 'data.virtual_gateway_state', default_state={
            'safe': ['available'],
            'warning': ['pending', 'deleting'],
            'disable': ['deleted']
        }),
        TextDyField.data_source('Region', 'data.region'),
    ],
    search=[
        SearchField.set(name='Virtual Private Gateway ID', key='data.virtual_gateway_id'),
        SearchField.set(name='State', key='data.virtual_gateway_state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'gray.400'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}}
                        }),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)
cst_vp_gw._metadata = cst_vp_gw_meta


'''
LAG
'''
cst_lags = CloudServiceTypeResource()
cst_lags.name = 'LAG'
cst_lags.provider = 'aws'
cst_lags.group = 'DirectConnect'
cst_lags.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
    'spaceone:is_major': 'false',
}
cst_lags_meta = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.lag_id'),
        TextDyField.data_source('Name', 'data.lag_name'),
        EnumDyField.data_source('State', 'data.lag_state', default_state={
            'available': ['requested'],
            'safe': ['available'],
            'warning': ['deleting'],
            'alert': ['down'],
            'disable': ['unknown', 'deleted']
        }),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Region', 'data.region'),
    ],
    search=[
        SearchField.set(name='Lag ID', key='data.lag_id'),
        SearchField.set(name='Name', key='data.log_name'),
        SearchField.set(name='State', key='data.lag_state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'requested': {'label': 'Available', 'icon': {'color': 'blue.400'}},
                            'deleting': {'label': 'Deleted', 'icon': {'color': 'yellow.500'}},
                            'down': {'label': 'Pending', 'icon': {'color': 'red.500'}},
                            'unknown': {'label': 'Deleting', 'icon': {'color': 'gray.400'}}
                        }),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Connection Count', key='data.number_of_connections', data_type='integer'),
        SearchField.set(name='Bandwidth', key='data.connections_bandwidth'),
        SearchField.set(name='Minimum Links', key='data.minimum_links', data_type='integer'),
        SearchField.set(name='AWS Device', key='data.aws_device'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)
cst_lags._metadata = cst_lags_meta


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_connection}),
    CloudServiceTypeResponse({'resource': cst_dc_gw}),
    CloudServiceTypeResponse({'resource': cst_vp_gw}),
    CloudServiceTypeResponse({'resource': cst_lags}),
]
