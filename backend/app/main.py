from fastapi import FastAPI

app = FastAPI(title="Weather Backend (dev)")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/hello")
async def hello():
    return {"msg": "Hello from Weather backend"}


