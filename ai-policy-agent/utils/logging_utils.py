import logging

class TraceLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return msg, {"extra": {"trace_id": self.extra.get("trace_id", "N/A")}}
