import os
from pathlib import Path
from dotenv import load_dotenv  
from constructs import Construct
from aws_cdk import App, Stack, Environment, Duration, CfnOutput
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode, Architecture, FunctionUrlAuthType

# Load environment variables 
load_dotenv()

# Set the AWS environment using values from environment variables
env = Environment(
    account=os.getenv("AWS_ACCOUNT_ID"),  
    region=os.getenv("AWS_REGION")  
)

# Define a stack for deploying a Lambda function running a Gradio application
class GradioLambda(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create an AWS Lambda function using a Docker image
        lambda_fn = DockerImageFunction(
            self,
            "GradioApp", 
            code=DockerImageCode.from_image_asset(
                str(Path.cwd()),  # Path to the directory containing the Dockerfile
                file="Dockerfile"  # Specify the Dockerfile to use for building the image
            ),
            architecture=Architecture.X86_64,  # Specify the CPU architecture (x86_64)
            memory_size=128,  
            timeout=Duration.minutes(5),  # Set a timeout of 5 minutes
        )
        
        # Create a function URL (public endpoint) to invoke the Lambda function
        fn_url = lambda_fn.add_function_url(auth_type=FunctionUrlAuthType.NONE)  # No authentication required
        
        # Output the function URL to the AWS CloudFormation stack outputs
        CfnOutput(self, "functionUrl", value=fn_url.url)

# Create an AWS CDK application
app = App()

# Instantiate the GradioLambda stack and deploy it within the specified AWS environment
GradioLambda(app, "GradioLambda", env=env)

# Synthesize the CloudFormation template for deployment
app.synth()
