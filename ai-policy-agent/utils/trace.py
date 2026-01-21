import uuid
from utils.trace_context import trace_id_ctx


def generate_trace_id() -> str:
    return uuid.uuid4().hex


def set_trace_id(trace_id: str | None):
    if trace_id:
        trace_id_ctx.set(trace_id)


def get_trace_id() -> str:
    return trace_id_ctx.get() or "UNKNOWN_TRACE"
