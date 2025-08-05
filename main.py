from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

TARGET_API_URL = "https://api.nopaperforms.io/application/v1/list"

@app.get("/ping")
@app.head("/ping")
def ping():
    return {"status": "ok"}

@app.post("/mit-studentfetch")
async def proxy_handler(request: Request):
    incoming_body = await request.body()

    # Required headers for the Nopaperforms API
    headers_to_forward = {
        "Content-Type": "application/json",
        "secret-key": "1c58c83c90534ec5b760c3c12ef98e30",
        "access-key": "883fff67e92c496eb4efe2049397a745",
        # Uncomment below if the API also needs a session cookie
        # "Cookie": "PHPSESSID=agtl12dsjsphunai7q8k03u26h"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            TARGET_API_URL,
            content=incoming_body,
            headers=headers_to_forward
        )

    return JSONResponse(
        content=response.json(),
        status_code=response.status_code
    )

