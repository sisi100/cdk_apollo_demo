from aws_cdk import core as cdk
from aws_cdk.aws_apigatewayv2 import CorsHttpMethod, HttpApi, HttpMethod
from aws_cdk.aws_apigatewayv2_authorizers import (
    HttpLambdaAuthorizer,
    HttpLambdaResponseType,
)
from aws_cdk.aws_apigatewayv2_integrations import LambdaProxyIntegration
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_lambda_nodejs import NodejsFunction

APP_NAME = "CdkApollo"


class CdkApolloStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_authorizer = NodejsFunction(
            self,
            f"{APP_NAME}LambdaAuthorizer",
            entry="lib/authorizer.ts",
            handler="handler",
            runtime=Runtime.NODEJS_14_X,
        )
        authorizer = HttpLambdaAuthorizer(
            authorizer_name="hogehoge_authorizer",
            identity_source=["$request.header.HogeAuthorization"],
            response_types=[HttpLambdaResponseType.SIMPLE],
            handler=lambda_authorizer,
        )

        lambda_apollo = NodejsFunction(
            self,
            f"{APP_NAME}LambdaApollo",
            entry="lib/apollo_api.ts",
            handler="handler",
            runtime=Runtime.NODEJS_14_X,
        )
        lambda_integration = LambdaProxyIntegration(handler=lambda_apollo)

        http_api = HttpApi(
            self,
            f"{APP_NAME}HttpApi",
            cors_preflight={
                # 対応はこのあたり`https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html`
                "allow_origins": ["*"],
                "allow_headers": ["HogeAuthorization"],
                "allow_methods": [CorsHttpMethod.GET, CorsHttpMethod.POST],
            },
        )
        http_api.add_routes(
            path="/",
            methods=[HttpMethod.GET, HttpMethod.POST],
            integration=lambda_integration,
            authorizer=authorizer,
        )
