# Third-party imports
from fastapi import FastAPI
from modal import Image, Stub, asgi_app, Mount

APP_NAME = "goldendj"

image = Image.debian_slim().from_dockerfile(
    'Dockerfile',
    context_mount=Mount.from_local_dir(
        local_path='.',
        remote_path='.',
        condition=lambda pth: not any(
            [i in pth for i in ['.pyc', '.mp3', '.wav']]
        )
    )
)

stub = Stub(
    "golden-dj",
    image=image
)

with image.imports():
    from telephony_server import telephony

app = FastAPI(docs_url=None)

@app.get('/')
def hello():
    return "Hi, this is your favorite DJ."

app.include_router(telephony.get_router())

@stub.function()
@asgi_app(label=APP_NAME)
def entrypoint():
    return app