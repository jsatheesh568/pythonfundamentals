# app.py
from flask import Flask, jsonify
import pyautogui

app = Flask(__name__)

@app.route("/write-message", methods=["GET"])
def write_message():
    message = "Hello SatheeshKumar Subramanian! GenAI Architect"
    filename = "genai.txt"

    # Save into file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(message)

    # (Optional) also simulate typing
    pyautogui.typewrite(message, interval=0.05)

    return jsonify({
        "status": "success",
        "file": filename,
        "message": message
    })


if __name__ == "__main__":
    app.run(debug=True)
