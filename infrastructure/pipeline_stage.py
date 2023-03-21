from constructs import Construct
from aws_cdk import (
    Stage,
)

from .serverless_image_analyzer_stack import ServerlessImageAnalyzerStack

# CodePipeline Stage
class ServerlessImageAnalyzerPipelineStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = ServerlessImageAnalyzerStack(self, 'ServerlessImageAnalyzerStack')