import json


def handler(event, context):
    return {
        "policyDocument":{
            "Version":"2012-10-17",
            "Statement":[
                {
                    "Action":"execute-api:Invoke",
                    "Effect":"Allow",
                    "Resource":"*"
                }
            ]
        },
        "context": {"message": "success!"}
    }
