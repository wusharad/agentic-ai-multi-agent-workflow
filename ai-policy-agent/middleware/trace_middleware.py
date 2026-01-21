from fastapi import Request
from utils.trace import set_trace_id, generate_trace_id


async def trace_middleware(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-Id")

    # If router forgot to send it, generate one
    if not trace_id:
        trace_id = generate_trace_id()

    set_trace_id(trace_id)

    response = await call_next(request)

    # Optional: return trace_id in response header
    response.headers["X-Trace-Id"] = trace_id

    return response
