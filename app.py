from flask import Flask, request, jsonify
from opentelemetry import metrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# Initialize OpenTelemetry Flask instrumentation
FlaskInstrumentor().instrument_app(app)

#test4
# Custom metric for square calculations
meter = metrics.get_meter(__name__)
square_counter = meter.create_counter("square_calculations", description="Number of square calculations")

@app.route('/square', methods=['POST'])
def calculate_square():
    data = request.get_json()
    number = data.get('number')
    if not isinstance(number, (int, float)):
        return jsonify({"error": "Invalid input"}), 400
    result = number ** 2
    square_counter.add(1)  # Increment custom metric
    return jsonify({"number": number, "square": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)