from fastapi import FastAPI, Request
from typing import Any
import argparse
import joblib
import uvicorn
from typing import List


def prediction(req_data: str) -> List[str]:
    result = model.predict(
        vectorizer.transform([req_data])
    ) # result = array([[0, 1, 1, 0, ...]])
    result = mlb.inverse_transform(result)[0] # result = ('tag1', 'tag2', 'tag3', ...)
    return result


app = FastAPI(description="L'API HTTP pour mon projet OpenClassrooms «Prédiction de l'étiquetage des questions Stackoverflow»", )


@app.post("/predict")
async def predict(req: Request) -> Any:
    req_data = (await req.body()).decode()
    predicted_tags = prediction(req_data)
    return predicted_tags


if __name__ == "__main__":
    model = joblib.load('models/best_estimator_TfidfVectorizer_80000_LogisticRegression.joblib')
    vectorizer = joblib.load('models/vectorizer_TfidfVectorizer_100000.pkl')
    mlb = joblib.load('models/mlb_100000.pkl')

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True,
                        help="Port number to run the server on")
    args = parser.parse_args()
    port = int(args.port)

    try:
        uvicorn.run(app, host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        pass
