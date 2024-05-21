import numpy as np
import cv2
import imutils
import datetime
import matplotlib.pyplot as plt
import winsound

gun_cascade = cv2.CascadeClassifier('cascade.xml')
camera = cv2.VideoCapture(0)
firstFrame = None
gun_exist = False

while True:
    ret, frame = camera.read()
    if frame is None:
        break
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gun = gun_cascade.detectMultiScale(gray, 1.3, 20, minSize=(100, 100))
    if len(gun) > 0:
        gun_exist = True
        # Play a beep sound when gun is detected
        winsound.Beep(1000, 400)  # Adjust the frequency and duration as needed
    for (x, y, w, h) in gun:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
    if firstFrame is None:
        firstFrame = gray
        continue
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S %p"),
                (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)
    if gun_exist:
        print("Guns detected")
        plt.imshow(frame)
        from email.message import EmailMessage
        import ssl
        import smtplib

        email_sender = "jrn03540@gmail.com"
        email_password = "jimzlkimpykmlaqh"
        email_receiver = "lioneljames987@gmail.com"
        subject = "Security alert!!!!"
        body = "Alert, An weapon is detected in your property!!!.\n\nPlease be at your highest alertness and take appropriate actions immediately.\nSincerely,\nYour Security System."
        en = EmailMessage()
        en['From'] = email_sender
        en['To'] = email_receiver
        en['subject'] = subject
        en.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,en.as_string())
        break
    else:
        cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()