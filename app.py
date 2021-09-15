import os

from aws_cdk import core

from cdk_apollo.cdk_apollo_stack import CdkApolloStack

app = core.App()
CdkApolloStack(
    app, "CdkApolloStack",
)

app.synth()
