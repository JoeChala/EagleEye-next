from fastapi import FastAPI

app = FastAPI(
    title="Eagle Eye Platform",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Eagle Eye API running"}