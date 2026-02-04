import cv2
from deepface import DeepFace

# buka webcam
cap = cv2.VideoCapture(0)

print("🔹 Tekan 'q' untuk keluar")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # deteksi emosi real-time
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']

        # tampilkan di layar
        cv2.putText(frame, f"Emotion: {emotion}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except Exception as e:
        print("Error:", e)

    cv2.imshow("Real-Time Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
