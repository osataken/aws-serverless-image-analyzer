#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infrastructure.serverless_image_analyzer_stack import ServerlessImageAnalyzerStack
from infrastructure.pipeline_stack import ServerlessImageAnalyzerPipelineStack

app = cdk.App()

# Uncomment/Comment below code to run the pipeline or the stack respectively.
ServerlessImageAnalyzerStack(app, "ServerlessImageAnalyzerStack")
# ServerlessImageAnalyzerPipelineStack(app, "ServerlessImageAnalyzerPipelineStack")

app.synth()
