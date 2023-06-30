from potassium import Potassium, Request, Response
from transformers import pipeline
import torch

app = Potassium("my_app")

# @app.init runs at startup, and loads models into the app's context
@app.init
def init():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = pipeline(
        # "automatic-speech-recognition",
        model="openai/whisper-base",
        chunk_length_s=30,
        device=device,
    )
   
    context = {
        "model": model
    }

    return context

# @app.handler runs for every call
@app.handler()
def handler(context: dict, request: Request) -> Response:
    import boto3
    import os

    # get bucket from environment variable
    bucket = os.environ.get("AWS_BUCKET")

    # get file path from request.json dict
    path = request.json.get("path")

    # set up boto3 client with credentials from environment variables
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # download file from bucket
    s3.download_file(bucket, path, "sample.wav")

    with open("sample.wav", "rb") as f:
        sample = f.read()
        model = context.get("model")
        outputs = model(
            sample, 
            batch_size=8
        )

        return Response(
            json = {"outputs": outputs}, 
            status=200
        )

if __name__ == "__main__":
    app.serve()
