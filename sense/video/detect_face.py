import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def main():
    # Load the trained model
    model_best = load_model('sense/video/face_model.h5') # set your machine model file path here

    # Classes 7 emotional states
    class_names = ['Angry', 'Disgusted', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    # Load the pre-trained face cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open a connection to the webcam (0 is usually the default camera)
    video_path = 'PLACEHOLDER'  # Set your video file path here
    cap = cv2.VideoCapture(video_path) # set your machine video file path here

    # Initialize a dictionary to keep track of emotion counts
    emotion_counts = {emotion: 0 for emotion in class_names}

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract the face region
            face_roi = frame[y:y + h, x:x + w]

            # Resize the face image to the required input size for the model
            face_image = cv2.resize(face_roi, (48, 48))
            face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            face_image = image.img_to_array(face_image)
            face_image = np.expand_dims(face_image, axis=0)
            face_image = np.vstack([face_image])

            # Predict emotion using the loaded model
            predictions = model_best.predict(face_image)
            emotion_label = class_names[np.argmax(predictions)]
            emotion_counts[emotion_label] += 1

            # Display the emotion label on the frame
            cv2.putText(frame, f'Emotion: {emotion_label}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 0, 255), 2)

            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Display the resulting frame
        # cv2.imshow('Emotion Detection', frame)
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #     break

    if any(emotion_counts.values()):
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        print("\nEmotion Counts:")
        for emotion, count in emotion_counts.items():
            print(f"{emotion}: {count}")
        print(f"\nThe most dominant emotion detected was: {dominant_emotion}")
    else:
        print("No emotions were detected.")