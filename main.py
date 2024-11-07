from fastapi import FastAPI
from pydantic import BaseModel
import json
from TP1_SOAP.services.verify_solvability import is_solvable
from TP1_SOAP.services.information_extraction import extract_infos
from TP1_SOAP.services.property_evaluation import evaluate_property

app = FastAPI()


# Pydantic models for validation
class DataExtractionRequest(BaseModel):
    text: str


class SolvencyCheckRequest(BaseModel):
    data: str
    estimated_value: float


class PropertyEvaluationRequest(BaseModel):
    data: str


class DecisionRequest(BaseModel):
    client_solvable: bool


@app.post("/extract-data/")
async def extract_data(request: DataExtractionRequest):
    """Extracts information from provided text."""
    data = extract_infos(request.text)
    return json.dumps(data)


@app.post("/check-solvency/")
async def check_solvency(request: SolvencyCheckRequest):
    """Checks if the client is solvable based on given data and estimated value."""
    data = json.loads(request.data)
    solvable_client = is_solvable(
        name=data["personal_information"]["name"],
        monthly_cost_of_the_property=request.estimated_value,
    )
    return json.dumps(solvable_client)


@app.post("/evaluate-property/")
async def estimate_property(request: PropertyEvaluationRequest):
    """Evaluates the property value based on provided data."""
    data = json.loads(request.data)
    estimated_value = evaluate_property(
        address=data["property_details"]["address"],
        region=data["property_details"]["region"],
        area_sqm=data["property_details"]["surface"],
        condition=data["property_details"]["description"][-1].split(" ")[0],
    )
    return json.dumps(estimated_value)


@app.post("/make-decision/")
async def make_decision(request: DecisionRequest):
    """Makes a decision on solvency based on client solvability status."""
    decision = ""
    if request.client_solvable:
        decision = "Final decision : Yes, client is solvable."
    else:
        decision = "Final decision : No, client is not solvable."
    return json.dumps(decision)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
