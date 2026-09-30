from fastapi import FastAPI

app = FastAPI(
    title="Pack Manager",
    description="Evidence-first packing verification service",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "Pack Manager",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
