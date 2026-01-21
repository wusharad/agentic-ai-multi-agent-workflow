# Reads trace_id from header
# Stores it in context
# Makes it available everywhere (logs, agent, utils)
from contextvars import ContextVar


"""
Why ContextVar?
1. ContextVar is thread-safe
2. Works with async, sync, background tasks
"""
# Holds trace_id per request / execution context
trace_id_ctx: ContextVar[str | None] = ContextVar(
    "trace_id",
    default=None
)
