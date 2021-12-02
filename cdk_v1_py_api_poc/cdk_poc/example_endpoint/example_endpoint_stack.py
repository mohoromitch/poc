from aws_cdk import (
    aws_sqs as sqs,
    aws_sns as sns,
    aws_lambda as aws_lambda,
    aws_sns_subscriptions as subs,
    aws_apigateway as apigateway,
    core
)

from mapped_gateway_stack import MappedGatewayStack


class ExampleServiceStack(MappedGatewayStack):
    def __init__(self, scope: core.Construct,
                 construct_id: str,
                 api_id: str,
                 root_resource_id: str,
                 authorizer: apigateway.IAuthorizer,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, api_id, root_resource_id, **kwargs)

        # Initialize Function
        # Function can be run locally using SAM
        # https://aws.amazon.com/blogs/compute/better-together-aws-sam-and-aws-cdk/
        # allows `curl --location --request GET 'http://localhost:3000'` to be possible
        handler_function = aws_lambda.Function(self, "handler-function",
                                               runtime=aws_lambda.Runtime.PYTHON_3_8,
                                               code=aws_lambda.Code.from_asset("lambda/example_endpoint"),
                                               handler="index.handler"
                                               # There are _many_ other options available, simply press cmd+P
                                               )

        # Route Mapping
        example_endpoint = self.api.root.add_resource("example-endpoint")
        example_endpoint.add_method("GET",
                                    apigateway.LambdaIntegration(handler=handler_function),
                                    authorizer=authorizer)

        # Includes constructs for all supporting infrastructure
        queue = sqs.Queue(
            self, "CdkPocQueue",
            visibility_timeout=core.Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "CdkPocTopic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))

        # Adding Permissions
        topic.grant_publish(handler_function)
