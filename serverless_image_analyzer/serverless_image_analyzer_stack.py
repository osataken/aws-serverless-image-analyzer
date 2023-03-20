from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
    aws_s3 as _s3,
    aws_s3_notifications,
    aws_s3_deployment as _s3_deployment,
    aws_cloudfront as _cf,
    aws_cloudfront_origins as _origins,
    aws_dynamodb as _ddb,
    aws_iam as _iam,
)
from constructs import Construct


class ServerlessImageAnalyzerStack(Stack):

    @property
    def presigned_url_api(self):
        return self._presigned_url_api
    
    def generate_html(self) :
        # Read in the file
        with open('src/static/index.html', 'r') as file :
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('<<PRESIGNED_URL>>', self._presigned_url_api.url)
        return filedata

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 for uploading images, lambda and DynamoDB
        image_uploaded_bucket = _s3.Bucket(
            self, 'img-upload-bucket',
            cors=[_s3.CorsRule(
                allowed_headers=["*"],
                allowed_methods=[
                    _s3.HttpMethods.PUT, 
                    _s3.HttpMethods.GET, 
                    _s3.HttpMethods.HEAD,
                    _s3.HttpMethods.DELETE,
                    _s3.HttpMethods.POST
                ],
                allowed_origins=["*"])
            ]
        )

        image_metadata_table = _ddb.Table(
            self, 'ResultsTable',
            partition_key={'name': 'id', 'type': _ddb.AttributeType.STRING}
        )

        image_analyzer_lambda = _lambda.Function(
            self, "ImageAnalyzerLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('src/lambda'),
            handler='image_analyzer.lambda_handler',
            environment={
                'TABLE_NAME': image_metadata_table.table_name,
            }
        )

        s3_notification = aws_s3_notifications.LambdaDestination(
            image_analyzer_lambda)
        
        # Presigned URL Lambda and API Gateway
        presigned_url_lambda = _lambda.Function(
            self, "PresignedUrlLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('src/lambda'),
            handler='presigned_url.lambda_handler',
            environment={
                'IMAGE_UPLOAD_BUCKET': image_uploaded_bucket.bucket_name,
            }
        )

        self._presigned_url_api = _apigw.LambdaRestApi(
            self, 'PresignedUrlEndpoint',
            handler=presigned_url_lambda,
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_origins=_apigw.Cors.ALL_ORIGINS,
                allow_methods=_apigw.Cors.ALL_METHODS
            )
        )

        # Web Content and CloudFront Distribution
        image_upload_static_web_bucket = _s3.Bucket(
            self, 'static-web-bucket',
        )

        _s3_deployment.BucketDeployment(
            self, "s3-deployment",
            sources=[
                _s3_deployment.Source.data("index.html", self.generate_html()),
                _s3_deployment.Source.asset("src/static/favicon.ico")],
            destination_bucket=image_upload_static_web_bucket
        )

        cf_dist = _cf.Distribution(
            self, 'image-upload-dist',
            default_behavior=_cf.BehaviorOptions(
                origin=_origins.S3Origin(image_upload_static_web_bucket),
                response_headers_policy=_cf.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS)
        )

        # Permission Settings
        image_analyzer_lambda.add_to_role_policy(_iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            actions=["rekognition:DetectText", "rekognition:DetectLabels"],
            resources=["*"]))

        image_metadata_table.grant_read_write_data(image_analyzer_lambda)

        image_uploaded_bucket.grant_read(image_analyzer_lambda)
        image_uploaded_bucket.grant_put(presigned_url_lambda)
        image_uploaded_bucket.add_event_notification(
            _s3.EventType.OBJECT_CREATED, s3_notification)

        CfnOutput(self, "Web URL", value=cf_dist.domain_name)
