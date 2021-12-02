from aws_cdk import (
    aws_lambda as aws_lambda,
    aws_apigateway as apigateway,
    core
)

from mapped_gateway_stack import MappedGatewayStack


class HealthCheckStack(MappedGatewayStack):

    def __init__(self, scope: core.Construct,
                 construct_id: str,
                 api_id: str,
                 root_resource_id: str,
                 authorizer: apigateway.IAuthorizer,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, api_id, root_resource_id, **kwargs)

        # Initialize Function
        health_check_handler_function = aws_lambda.Function(self, "handler-function",
                                                            runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                            code=aws_lambda.Code.from_asset("lambda/health-check"),
                                                            # Could simply just read a Dockerfile from the above dir
                                                            # code=aws_lambda.Code.from_asset_image,
                                                            handler="index.handler")

        # Route Mapping
        health_check_endpoint = self.api.root.add_resource("health-check")
        health_check_endpoint.add_method("GET",
                                         apigateway.LambdaIntegration(handler=health_check_handler_function),
                                         authorizer=authorizer)
