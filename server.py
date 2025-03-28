import os
from flask import Flask, request, jsonify
import cv2
import numpy as np
import PoseModule as pm
from flask_cors import CORS  # Import CORS



app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Pose detection server is running. Use /upload_video to process a video."

@app.route('/upload_video', methods=['POST'])
def upload_video():
    print("int the post")
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Initialize variables for processing
    detector = pm.poseDetector()
    count = 0
    dir = 0

    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        return jsonify({"error": "Failed to open video file"}), 500

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break

        img = cv2.resize(img, (1280, 720))
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            angle = detector.findAngle(img, 12, 14, 16)
            per = np.interp(angle, (50, 160), (100, 0))

            if per >= 98 and dir == 0:
                count += 1
                dir = 1

            elif per <= 5 and dir == 1:
                dir = 0

    cap.release()

    # Return response as dictionary
    return jsonify({"message": "Processing complete", "repetition_count": count}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
