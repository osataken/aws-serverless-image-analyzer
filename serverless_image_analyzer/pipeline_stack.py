from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines
)

from serverless_image_analyzer.pipeline_stage import ServerlessImageAnalyzerPipelineStage

class ServerlessImageAnalyzerPipelineStack(Stack):
    def __init__ (self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repository = codecommit.Repository(
            self, 'ServerlessImageAnalyzerRepo',
            repository_name='ServerlessImageAnalyzerRepo'
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repository, "main"),
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages
                    "cdk synth",
                ]
            )
        )

        deploy = ServerlessImageAnalyzerPipelineStage(self, "deploy")
        deploy_stage = pipeline.add_stage(deploy)

