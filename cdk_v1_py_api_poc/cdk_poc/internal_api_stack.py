from aws_cdk import (
    aws_apigateway as gateway,
    aws_lambda as aws_lambda,
    core
)

from example_endpoint.example_endpoint_stack import ExampleServiceStack
from example_endpoint.health_check_stack import HealthCheckStack


class InternalApiStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO: Create JWT Authorizer for V1 API Gateway (example below is for experimental V2)
        # jwt_authorizer = gateway2auths.HttpJwtAuthorizer(
        #     jwt_audience=["https://api.locallogic.co/"],
        #     jwt_issuer="https://locallogic.auth0.com/"
        # )

        # TODO: certificate generation (already done in RedirectStack.ts)
        # TODO: certificate mapping (already done in RedirectStack.ts)
        # TODO: domain name generation (already done in Redirectstack.ts)

        # TODO: Add stage (from App context) to name
        # TODO: Add CORS API Gateway settings
        # TODO: custom domain mapping

        # Init Authorizer Function
        token_authorizer = self.get_token_authorizer()

        # Init API Gateway
        api = gateway.RestApi(self, "internal-api",
                              description="Internal Local Logic API",
                              default_method_options=gateway
                              .MethodOptions(authorization_type=gateway.AuthorizationType.CUSTOM,
                                             authorizer=token_authorizer))
        api.root.add_method('ANY')

        # Add all API Stacks below, using the structure from AWS's docs here:
        # https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigateway-readme.html#breaking-up-methods-and-resources-across-stacks
        HealthCheckStack(self, 'heath-check-endpoint',
                         api_id=api.rest_api_id,
                         root_resource_id=api.rest_api_root_resource_id,
                         authorizer=token_authorizer,
                         **kwargs)

        ExampleServiceStack(self, 'example-endpoint',
                            api_id=api.rest_api_id,
                            root_resource_id=api.rest_api_root_resource_id,
                            authorizer=token_authorizer,
                            **kwargs)

    def get_token_authorizer(self):
        token_authorizer_function = aws_lambda.Function(self, "token-authorizer-function",
                                                        runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                        code=aws_lambda.Code.from_asset("lambda/token-authorizer"),
                                                        handler="index.handler")
        token_authorizer = gateway.RequestAuthorizer(self, "token-authorizer",
                                                     handler=token_authorizer_function,
                                                     identity_sources=[
                                                         gateway.IdentitySource.header('Authorization')])
        return token_authorizer
