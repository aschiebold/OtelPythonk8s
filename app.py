from flask import Flask, request, jsonify
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.flask import FlaskInstrumentor
import os

app = Flask(__name__)

# OpenTelemetry setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")))
)
metrics.set_meter_provider(
    MeterProvider(
        metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")))]
    )
)
meter = metrics.get_meter(__name__)
square_counter = meter.create_counter("square_calculations", description="Number of square calculations")

FlaskInstrumentor().instrument_app(app)

@app.route('/square', methods=['POST'])
def calculate_square():
    data = request.get_json()
    number = data.get('number')
    if not isinstance(number, (int, float)):
        return jsonify({"error": "Invalid input"}), 400
    with tracer.start_as_current_span("calculate_square"):
        result = number ** 2
        square_counter.add(1)
    return jsonify({"number": number, "square": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)