import cv2
import mediapipe as mp
import serial
import time
import os

from face_db import load_model
from whatsapp import send_whatsapp


# ==========================
# Arduino Connection By Vihaan
# ==========================

try:
    arduino = serial.Serial(
        "COM4",
        115200,
        timeout=1
    )

    time.sleep(2)

    print("Arduino connected")

except Exception as e:

    arduino = None

    print(
        "Arduino not connected:",
        e
    )



# ==========================
# Camera
# ==========================

camera = cv2.VideoCapture(0)

WIDTH = 640
HEIGHT = 480


camera.set(3, WIDTH)
camera.set(4, HEIGHT)



# ==========================
# MediaPipe Detection
# ==========================

mp_face = mp.solutions.face_detection


detector = mp_face.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.6
)



# ==========================
# Recognition
# ==========================

recognizer = load_model()


names = {
    0:"Vihaan"
}



haar = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)



# ==========================
# Unknown Folder
# ==========================

UNKNOWN_FOLDER = "unknown_faces"


os.makedirs(
    UNKNOWN_FOLDER,
    exist_ok=True
)


last_unknown = 0

delay = 15



# ==========================
# Servo
# ==========================

pan = 90
tilt = 90


CENTER_X = WIDTH//2
CENTER_Y = HEIGHT//2


DEAD_ZONE = 40



def send_servo(pan,tilt):

    if arduino:

        command = (
            f"{int(pan)},"
            f"{int(tilt)}\n"
        )

        arduino.write(
            command.encode()
        )



# ==========================
# Main Loop
# ==========================


while True:


    ret, frame = camera.read()


    if not ret:
        break



    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    result = detector.process(rgb)



    name = "Unknown"



    if result.detections:



        detection = result.detections[0]


        box = detection.location_data.relative_bounding_box


        h,w,_ = frame.shape


        x = int(box.xmin*w)
        y = int(box.ymin*h)


        fw = int(box.width*w)
        fh = int(box.height*h)



        cx = x + fw//2
        cy = y + fh//2



        cv2.rectangle(
            frame,
            (x,y),
            (x+fw,y+fh),
            (0,255,0),
            2
        )



        # ==================
        # Servo Tracking
        # ==================


        error_x = cx-CENTER_X
        error_y = cy-CENTER_Y



        if abs(error_x)>DEAD_ZONE:

            pan -= error_x*0.002



        if abs(error_y)>DEAD_ZONE:

            tilt += error_y*0.002



        pan=max(
            0,
            min(180,pan)
        )


        tilt=max(
            20,
            min(160,tilt)
        )


        send_servo(
            pan,
            tilt
        )




        # ==================
        # Recognition
        # ==================


        gray=cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )



        faces=haar.detectMultiScale(
            gray,
            1.2,
            5
        )



        for(fx,fy,fw,fh) in faces:


            face=gray[
                fy:fy+fh,
                fx:fx+fw
            ]



            if recognizer:


                identity,confidence=recognizer.predict(face)



                if confidence < 70:

                    name=names.get(
                        identity,
                        "Unknown"
                    )



        # ==================
        # Unknown Alert
        # ==================


        if name=="Unknown":


            now=time.time()



            if now-last_unknown > delay:


                image_path = (
                    f"{UNKNOWN_FOLDER}/"
                    f"unknown_{int(now)}.jpg"
                )


                cv2.imwrite(
                    image_path,
                    frame
                )

                filename = os.path.basename(image_path)
                print(
                    "Unknown saved:",
                    image_path
                )

                image_url = (
                    "http://YOUR_IP_ADDRESS:5000/unknown/"
                    + filename
                )

                send_whatsapp(image_url)

                print(
                    "Unknown saved:",
                    image_path
                )


                # WhatsApp call
                # Needs public image URL
                # Added in next stage

                last_unknown=now




        cv2.putText(
            frame,
            name,
            (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )




    cv2.imshow(
        "AI Security System",
        frame
    )



    if cv2.waitKey(1)&0xff==ord("q"):
        break




camera.release()

cv2.destroyAllWindows()


if arduino:
    arduino.close()