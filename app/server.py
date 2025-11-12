from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import compile_graph

app = FastAPI(title="LangGraph Demo API")
graph = compile_graph()

class InferenceRequest(BaseModel):
    user_input: str

@app.get("/")
def home():
    return {"message": "LangGraph Demo API is running. Use POST /run to interact."}

@app.post("/run")
def run_graph(req: InferenceRequest):
    result = graph.invoke({"user_input": req.user_input})
    # 'result' is the final state dict; include both summary and full state
    return {"response": result.get("response"), "state": result}
