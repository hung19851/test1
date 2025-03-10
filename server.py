from fastapi import FastAPI, Request, HTTPException
import httpx
import asyncio

app = FastAPI()

@app.post("/proxy")
async def proxy(request: Request):
    data = await request.json()

    target_url = data.get("url")
    if not target_url:
        raise HTTPException(status_code=400, detail="Missing 'url' field")

    method = data.get("method", "GET").upper()
    headers = data.get("headers", {})
    body = data.get("body", None)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.request(
                method=method,
                url=target_url,
                headers=headers,
                content=body
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response.text
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)