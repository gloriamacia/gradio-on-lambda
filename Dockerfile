# Use the latest available slim version of Python 3.12
FROM public.ecr.aws/docker/library/python:3.12-slim

# Copy the AWS Lambda Web Adapter
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.0 /lambda-adapter /opt/extensions/lambda-adapter

# Set the working directory
WORKDIR /var/task

# Copy and install dependencies efficiently
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Run the application
CMD ["python3", "app.py"]
