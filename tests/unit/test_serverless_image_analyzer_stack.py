import aws_cdk as core
import aws_cdk.assertions as assertions

from serverless_image_analyzer.serverless_image_analyzer_stack import ServerlessImageAnalyzerStack

# example tests. To run these tests, uncomment this file along with the example
# resource in serverless_image_analyzer/serverless_image_analyzer_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ServerlessImageAnalyzerStack(app, "serverless-image-analyzer")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
