import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.serverless_image_analyzer_stack import ServerlessImageAnalyzerStack


def test_infrastructure_created():
    app = core.App()
    stack = ServerlessImageAnalyzerStack(app, "serverless-image-analyzer")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::S3::Bucket", 2)
    template.resource_count_is("AWS::Lambda::Function", 4)
    template.resource_count_is("AWS::DynamoDB::Table", 1)
    template.resource_count_is("AWS::CloudFront::Distribution", 1)


def test_api_gateway_created():
    app = core.App()
    stack = ServerlessImageAnalyzerStack(app, "serverless-image-analyzer")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::ApiGateway::RestApi", 1)
    template.resource_count_is("AWS::ApiGateway::Resource", 1)
    template.resource_count_is("AWS::ApiGateway::Method", 4)
    template.resource_count_is("AWS::ApiGateway::Deployment", 1)
    template.resource_count_is("AWS::ApiGateway::Stage", 1)
