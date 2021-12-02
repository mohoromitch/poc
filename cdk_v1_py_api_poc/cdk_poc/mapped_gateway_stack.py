from aws_cdk import (
    aws_apigateway as apigateway,
    core
)


class MappedGatewayStack(core.NestedStack):

    def __init__(self,
                 scope: core.Construct,
                 construct_id: str,
                 api_id: str,
                 root_resource_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id)

        self.api = apigateway.RestApi.from_rest_api_attributes(self, 'mapped-api-gateway',
                                                               rest_api_id=api_id,
                                                               root_resource_id=root_resource_id)
