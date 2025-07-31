from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

##     python -m uvicorn main:app --reload

app = FastAPI()

TARGET_API_URL = "https://api.nopaperforms.io/application/v1/list"

@app.post("/mit-studentfetch")
async def proxy_handler(request: Request):
    # Read incoming request body and headers
    incoming_body = await request.body()
    incoming_headers = dict(request.headers)

    # Optional: clean up headers if required
    # e.g., remove 'host', 'content-length' or sensitive ones if needed
    excluded_headers = {"host", "content-length", "accept-encoding", "content-type"}
    headers_to_forward = {k: v for k, v in incoming_headers.items() if k.lower() not in excluded_headers}
    headers_to_forward["Content-Type"] = "application/json"

    # Forward request to target API using HTTPX
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TARGET_API_URL,
            content=incoming_body,
            headers=headers_to_forward
        )

    # Return response from target API to the original customer
    return JSONResponse(
        content=response.json(),
        status_code=response.status_code,
        headers=dict(response.headers)
    )
