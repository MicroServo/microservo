from skywalking import Component
from skywalking.trace.context import SpanContext, get_context
from skywalking.trace.tags import Tag

context: SpanContext = get_context()

with context.new_entry_span(op='https://github.com/apache') as span:
    span.component = Component.Flask
