import pyautogui
import time

def write_message():
    message = "Hello SatheeshKumar Subramanian! GenAI Architect"
    filename = "genai.txt"

    # Simulate typing delay just for fun (like a human typing)
    pyautogui.typewrite(message, interval=0.05)

    # Also save it into a text file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(message)

    return {"status": "success", "file": filename, "message": message}


if __name__ == "__main__":
    print(write_message())
