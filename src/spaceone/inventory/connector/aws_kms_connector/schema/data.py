import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


class Key(Model):
    aws_account_id = StringType(deserialize_from="AWSAccountId")
    key_id = StringType(deserialize_from="KeyId")
    arn = StringType(deserialize_from="Arn")
    alias_name = StringType(deserialize_from="AliasName")
    alias_arn = StringType(deserialize_from="AliasArn")
    creation_date = DateTimeType(deserialize_from="CreationDate")
    enabled = BooleanType(deserialize_from="Enabled")
    description = StringType(deserialize_from="Description")
    key_usage = StringType(deserialize_from="KeyUsage", choices=("SIGN_VERIFY",
                                                                 "ENCRYPT_DECRYPT"))
    key_state = StringType(deserialize_from="KeyState", choices=("Enabled",
                                                                 "Disabled",
                                                                 "PendingDeletion",
                                                                 "PendingImport",
                                                                 "Unavailable"))
    deletion_date = DateTimeType(deserialize_from="DeletionDate")
    valid_to = DateTimeType(deserialize_from="ValidTo")
    origin = StringType(deserialize_from="Origin", choices=("AWS_KMS",
                                                            "EXTERNAL",
                                                            "AWS_CLOUDHSM"))
    custom_key_store_id = StringType(deserialize_from="CustomKeyStoreId")
    cloud_hsm_cluster_id = StringType(deserialize_from="CloudHsmClusterId")
    expiration_model = StringType(deserialize_from="ExpirationModel", choices=("KEY_MATERIAL_EXPIRES",
                                                                               "KEY_MATERIAL_DOES_NOT_EXPIRE"))
    key_manager = StringType(deserialize_from="KeyManager", choices=("AWS", "CUSTOMER"))
    key_type_path = StringType(default="")
    customer_master_key_spec = StringType(deserialize_from="CustomerMasterKeySpec", choices=("RSA_2048",
                                                                                             "RSA_3072",
                                                                                             "RSA_4096",
                                                                                             "ECC_NIST_P256",
                                                                                             "ECC_NIST_P384",
                                                                                             "ECC_NIST_P521",
                                                                                             "ECC_SECG_P256K1",
                                                                                             "SYMMETRIC_DEFAULT"))
    encryption_algorithms = ListType(StringType, deserialize_from="EncryptionAlgorithms")
    signing_algorithms = ListType(StringType, deserialize_from="SigningAlgorithms")
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/kms/home?region={self.region_name}#/kms/{self.key_type_path}/{self.key_id}/"
        }

    @serializable
    def cloudwatch(self):
        return {
            "namespace": "AWS/KMS",
            "dimensions": [
                {
                    "Name": "KeyId",
                    "Value": self.key_id
                }
            ],
            "region_name": self.region_name
        }