from fastapi import FastAPI

app = FastAPI(title="AI Support Intelligence")

@app.get("/")
def home():
    return {"message": "AI Support Intelligence API is running"}