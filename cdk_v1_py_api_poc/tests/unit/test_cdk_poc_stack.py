import json
import pytest

from aws_cdk import core
from cdk_poc.cdk_poc_stack import CdkPocStack


def get_template():
    app = core.App()
    CdkPocStack(app, "cdk-poc")
    return json.dumps(app.synth().get_stack("cdk-poc").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
