from fastapi import FastAPI


app = FastAPI(
    title="FinTrack"
)


@app.get("/")
def main():
    return {"message": "OK"}
