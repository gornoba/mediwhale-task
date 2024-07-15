from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json

class SuccessInterceptor(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = ['/docs', '/redoc', '/docs-json', '/openapi.json']
        if any(path in request.url.path for path in excluded_paths):
            return await call_next(request)

        response = await call_next(request)

        if response.status_code == 200 and response.headers.get("content-type") == "application/json":
            response_body = [section async for section in response.__dict__['body_iterator']]
            response_body = b''.join(response_body).decode('utf-8')
            
            if response_body:
                try:
                  data = json.loads(response_body)
                  new_response_body = {"success": True, "data": data}
                  return JSONResponse(content=new_response_body, status_code=response.status_code)
                except json.JSONDecodeError:
                        return response
        
        return response