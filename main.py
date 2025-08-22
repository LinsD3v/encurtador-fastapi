from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import random
import string

app = FastAPI(title="Encurtador de URL")
data = {}

def generate_key(length=7):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/url/", response_class=HTMLResponse)
async def encurtar_url(request: Request, url: str = Form(...)):
    key = generate_key()
    data[key] = url
    short_url = f"http://localhost:8000/{key}"
    return f"""
    <html>
        <body>
            <p>URL encurtada:</p>
            <a href="{short_url}">{short_url}</a>
        </body>
    </html>
    """

@app.get("/{key}")
async def get_url(key: str):
    url = data.get(key)
    if url:
        # Adiciona http:// se não tiver
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        return RedirectResponse(url)
    else:
        raise HTTPException(status_code=404, detail="Url não encontrada.")
