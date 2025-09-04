from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get JSON body
        data = request.get_json()
        num1 = float(data.get('num1'))
        num2 = float(data.get('num2'))
        operation = data.get('operation')  # add, subtract, multiply, divide

        result = None

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return jsonify({"error": "Division by zero is not allowed"}), 400
            result = num1 / num2
        else:
            return jsonify({"error": "Invalid operation"}), 400

        return jsonify({
            "num1": num1,
            "num2": num2,
            "operation": operation,
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
