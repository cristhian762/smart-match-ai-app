from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# from resume_ranker import rank_resumes  # sua função de ranqueamento

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index.html", "r") as f:
        return HTMLResponse(f.read())


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")

    # Aqui você chama sua lógica de busca + LLM
    # top5 = rank_resumes(user_input)

    return JSONResponse({"response": []})

