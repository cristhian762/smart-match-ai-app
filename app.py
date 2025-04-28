from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from search import matches, models

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index.html", "r") as f:
        return HTMLResponse(f.read())


@app.get("/models")
async def get_models():
    return JSONResponse({"response": models()})


@app.post("/upload")
async def upload(
    model: str = Form(...),
    sumarized: str = Form(...),
    n_results: int = Form(...),
    file: UploadFile = File(...),
):
    content = await file.read()

    results = matches(model, n_results, content.decode("utf-8"), sumarized)

    return JSONResponse({"response": results})


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()

    model = data.get("model")
    sumarized = data.get("sumarized")
    n_results = data.get("n_results")
    message = data.get("message")

    results = matches(model, int(n_results), message, sumarized)

    return JSONResponse({"response": results})
