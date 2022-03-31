import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


from models.vector import Vector

templates = Jinja2Templates(directory="/home/emin/PycharmProjects/crona/searcher/templates")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={'request': request})


@app.post("/")
async def search(request: Request, query= Form(...)):
    result = Vector().search((str(query)))
    return templates.TemplateResponse("index.html", context={'request': request, 'result': result})

if __name__ == '__main__':
    uvicorn.run(app)
