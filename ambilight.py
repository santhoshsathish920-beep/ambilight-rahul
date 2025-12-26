from flask import Flask, jsonify
import mss
import numpy as np
import cv2

app = Flask(__name__)

latest_color = {"r": 0, "g": 0, "b": 0}

def capture_screen_color():
    global latest_color
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # main screen
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Resize for speed
        img_small = cv2.resize(img, (50, 50))

        avg_color = img_small.mean(axis=(0, 1))
        b, g, r = avg_color

        latest_color = {
            "r": int(r),
            "g": int(g),
            "b": int(b)
        }

@app.route("/color")
def get_color():
    return jsonify(latest_color)

if __name__ == "__main__":
    import threading
    import time

    def loop():
        while True:
            capture_screen_color()
            time.sleep(0.1)  # update 10 times/sec

    threading.Thread(target=loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
