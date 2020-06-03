import time
import logging
from typing import List

import boto3
import json

from spaceone.inventory.connector.aws_sqs_connector.schema.data import QueData, RedrivePolicy
from spaceone.inventory.connector.aws_sqs_connector.schema.resource import SQSResponse, QueResource
from spaceone.inventory.connector.aws_sqs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class SQSConnector(SchematicAWSConnector):
    response_schema = SQSResponse
    service_name = 'sqs'

    def get_resources(self) -> List[SQSResponse]:
        print("** SQS START **")
        start_time = time.time()

        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)

            # merge data
            for data in self.request_data(region_name):
                yield self.response_schema(
                    {'resource': QueResource({'data': data,
                                              'reference': ReferenceModel(data.reference)})})

        print(f' SQS Finished {time.time() - start_time} Seconds')

    def request_data(self, region_name) -> List[QueData]:
        resource = self.session.resource('sqs')
        # resource = boto3.resource('sqs')
        for que in resource.queues.all():
            attr = que.attributes
            if 'RedrivePolicy' in attr:
                attr['RedrivePolicy'] = RedrivePolicy(json.loads(attr.get('RedrivePolicy')), strict=False)

            result = QueData(attr)
            result.region_name = region_name
            result.url = que.url
            result.account_id = self.account_id
            yield result
