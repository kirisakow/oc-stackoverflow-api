from fastapi import FastAPI, Request
from typing import Any
import argparse
import pickle
import uvicorn

app = FastAPI(description="L'API HTTP pour mon projet OpenClassrooms «Prédiction de l'étiquetage des questions Stackoverflow»", )


@app.post("/predict")
async def predict(req: Request) -> Any:
    req_data = (await req.body()).decode()
    result = model.predict(
        vectorizer.transform([req_data])[:, :944]
    ) # result = array([[0, 1, 1, 0, ...]])
    result = mlb.inverse_transform(result)[0] # result = ('tag1', 'tag2', 'tag3', ...)
    return result


if __name__ == "__main__":
    with    open('models/model.pkl', 'rb') as fmodel, \
            open('models/vectorizer_filtered.pkl', 'rb') as fvec, \
            open('models/mlb.pkl', 'rb') as fmlb:
        model = pickle.load(fmodel)
        vectorizer = pickle.load(fvec)
        mlb = pickle.load(fmlb)

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True,
                        help="Port number to run the server on")
    args = parser.parse_args()
    port = int(args.port)

    try:
        uvicorn.run(app, host="127.0.0.1", port=port)
    except KeyboardInterrupt:
        pass
