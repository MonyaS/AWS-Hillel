from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,
    RemovalPolicy
)

from constructs import Construct


class UrlShoarterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        table = ddb.Table(
            self,
            "UrlsTable",
            partition_key={"name": "short_code", "type": ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Shorten URL Lambda
        shorten_lambda = _lambda.Function(
            self,
            "ShortenLambdaSalabai",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="shortener.lambda_handler",
            code=_lambda.Code.from_asset("lambdas"),
            environment={"TABLE_NAME": table.table_name},
        )

        # Redirect Lambda
        redirect_lambda = _lambda.Function(
            self,
            "RedirectLambdaSalabai",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="redirect.lambda_handler",
            code=_lambda.Code.from_asset("lambdas"),
            environment={"TABLE_NAME": table.table_name},
        )

        # Info Lambda
        info_lambda = _lambda.Function(
            self,
            "InfoLambdaSalabai",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="info.lambda_handler",
            code=_lambda.Code.from_asset("lambdas"),
            environment={"TABLE_NAME": table.table_name},
        )

        # Grant permissions to both Lambdas
        table.grant_read_write_data(shorten_lambda)
        table.grant_read_write_data(redirect_lambda)
        table.grant_read_data(info_lambda)

        # API Gateway
        api = apigw.RestApi(
            self,
            "UrlShortenerAPISalabai",
            default_cors_preflight_options={"allow_origins": apigw.Cors.ALL_ORIGINS},
        )

        # Shorten URL endpoint
        shorten_resource = api.root.add_resource("shorten")
        shorten_resource.add_method("POST", apigw.LambdaIntegration(shorten_lambda))

        # Redirect endpoint
        redirect_resource = api.root.add_resource("{short_code}")
        redirect_resource.add_method("GET", apigw.LambdaIntegration(redirect_lambda))

        # Info endpoint
        redirect_resource.add_method("POST", apigw.LambdaIntegration(info_lambda))
