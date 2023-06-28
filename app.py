from potassium import Potassium, Request, Response
from transformers import pipeline
import torch
from datasets import load_dataset

app = Potassium("my_app")

# @app.init runs at startup, and loads models into the app's context
@app.init
def init():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = pipeline(
        # "automatic-speech-recognition",
        model="openai/whisper-large",
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

    print(request.json)
    # ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
    # sample = ds[0]["audio"]
    # print(sample)

    with open(request.json.get("path"), "rb") as f:
        sample = f.read()
        model = context.get("model")
        outputs = model(
            sample, 
            batch_size=8
        )

        # prompt = request.json.get("prompt")
        # outputs = model(prompt)

        return Response(
            json = {"outputs": outputs}, 
            status=200
        )

if __name__ == "__main__":
    app.serve()
