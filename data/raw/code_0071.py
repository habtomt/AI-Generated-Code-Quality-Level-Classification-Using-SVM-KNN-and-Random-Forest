from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import uvicorn
from sklearn.linear_model import LogisticRegression

app = FastAPI(title="ML Prediction API")

# ----- Train a simple dummy model -----
X_train = np.array([
    [0, 0],
    [1, 1],
    [1, 0],
    [0, 1]
])
y_train = np.array([0, 1, 1, 0])

model = LogisticRegression()
model.fit(X_train, y_train)

# ----- Request schema -----
class InputData(BaseModel):
    features: list[float]

# ----- Health check -----
@app.get("/")
def root():
    return {"message": "ML API is running"}

# ----- Prediction endpoint -----
@app.post("/predict")
def predict(data: InputData):
    try:
        features = np.array(data.features, dtype=float).reshape(1, -1)

        if features.shape[1] != 2:
            raise HTTPException(
                status_code=400,
                detail="Expected input feature vector of size 2"
            )

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features).tolist()

        return {
            "prediction": int(prediction),
            "probability": probability
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----- Run server -----
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)