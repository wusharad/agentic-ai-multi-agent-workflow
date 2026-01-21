import uuid

def generate_trace_id() -> str:
    return f"req-{uuid.uuid4().hex[:12]}"