#!/usr/bin/env python3
import os

import aws_cdk as cdk

from serverless_image_analyzer.serverless_image_analyzer_stack import ServerlessImageAnalyzerStack
from serverless_image_analyzer.pipeline_stack import ServerlessImageAnalyzerPipelineStack


app = cdk.App()
ServerlessImageAnalyzerStack(app, "ServerlessImageAnalyzerStack")
# ServerlessImageAnalyzerPipelineStack(app, "ServerlessImageAnalyzerPipelineStack")

app.synth()
