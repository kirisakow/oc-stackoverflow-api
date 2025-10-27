from fastapi import FastAPI, Request
from typing import Any
import argparse
import uvicorn

app = FastAPI(description="L'API HTTP pour mon projet OpenClassrooms «Étiquetage des questions Stackoverflow»", )


@app.post("/predict")
async def predict(req: Request) -> Any:
    data = await req.json()
    print(f'input: {data}')
    data['foo'] *= 10
    print(f'output: {data}')
    return data


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True,
                        help="Port number to run the server on")
    args = parser.parse_args()
    port = int(args.port)

    try:
        uvicorn.run(app, host="127.0.0.1", port=port)
    except KeyboardInterrupt:
        pass
