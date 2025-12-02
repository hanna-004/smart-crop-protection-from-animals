import cv2
import pygame
import os
import smtplib
import time
from email.message import EmailMessage
from twilio.rest import Client
from ultralytics import YOLO

# -----------------------------
# Initialize YOLOv8 Model
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# Filter unwanted detections
# -----------------------------
FILTERED_CLASSES = {"bottle", "chair", "refrigerator", "traffic light", "tv", "cup", "keyboard"}

# -----------------------------
# Email Configuration (ADD YOUR DETAILS)
# -----------------------------
EMAIL_ADDRESS = "your_email_here"
EMAIL_PASSWORD = "your_app_password_here"
RECEIVER_EMAIL = "receiver_email_here"

# -----------------------------
# Twilio Phone Call Configuration (ADD YOUR DETAILS)
# -----------------------------
TWILIO_SID = "your_twilio_sid_here"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token_here"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number_here"
USER_PHONE_NUMBER = "your_phone_number_here"

# -----------------------------
# EMAIL ALERT FUNCTION
# -----------------------------
def send_email_alert(detected_animal, frame):
    try:
        image_path = f"{detected_animal}.jpg"
        cv2.imwrite(image_path, frame)

        msg = EmailMessage()
        msg["Subject"] = f"ALERT: {detected_animal.capitalize()} Detected!"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECEIVER_EMAIL
        msg.set_content(
            f"An animal ({detected_animal}) was detected. Please check the attached image."
        )

        with open(image_path, "rb") as img_file:
            msg.add_attachment(
                img_file.read(),
                maintype="image",
                subtype="jpeg",
                filename=f"{detected_animal}.jpg"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"📧 Email alert sent for {detected_animal}")

        os.remove(image_path)

    except Exception as e:
        print(f"❌ Email sending failed: {e}")

# -----------------------------
# PHONE CALL ALERT FUNCTION
# -----------------------------
def make_phone_call(detected_animal):
    try:
        print("⏳ Waiting 15 seconds before calling...")
        time.sleep(15)

        print("📞 Making phone call...")
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        call = client.calls.create(
            twiml=f'<Response><Say>Alert! A {detected_animal} has been detected.</Say></Response>',
            to=USER_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER
        )

        print(f"✅ Call placed successfully: {call.sid}")

    except Exception as e:
        print(f"❌ Phone call failed: {e}")

# -----------------------------
# START CAMERA
# -----------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Camera not found.")
    exit()

# -----------------------------
# MAIN DETECTION LOOP
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Cannot read frame")
        break

    results = model(frame)
    detected_animal = None

    for result in results:
        for det in result.boxes:
            x1, y1, x2, y2 = map(int, det.xyxy[0])
            conf = det.conf[0].item()
            cls = int(det.cls[0])
            label = model.names[cls].lower()

            if conf < 0.6 or label in FILTERED_CLASSES:
                continue

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{label} ({conf:.2f})",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

            detected_animal = label

    if detected_animal:
        print(f"🐾 Detected: {detected_animal}")
        send_email_alert(detected_animal, frame)
        make_phone_call(detected_animal)

    cv2.imshow("Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
