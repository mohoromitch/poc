#!/usr/bin/env python3

from aws_cdk import core

from example_endpoint.example_endpoint_stack import ExampleServiceStack
from internal_api_stack import InternalApiStack

# TODO: Create stage context variable and add https://yshen4.github.io/infrastructure/AWS/CDK_context.html
app = core.App()

# TODO: Add stage to name (get this from a CLI stage argument?)
internalApiStack = InternalApiStack(app, "internal-api", env={"region": "us-east-2"})

app.synth()
