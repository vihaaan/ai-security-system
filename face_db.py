import cv2
import os
import numpy as np


MODEL_FILE = "face_model.yml"


recognizer = cv2.face.LBPHFaceRecognizer_create()


face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)



# ==========================
# Train Faces
# ==========================

def train_faces():

    faces = []
    labels = []

    label_names = {}

    current_id = 0


    folder = "known_faces"


    if not os.path.exists(folder):

        os.makedirs(folder)

        print(
            "Created known_faces folder"
        )

        return



    for person in os.listdir(folder):


        person_folder = os.path.join(
            folder,
            person
        )


        if not os.path.isdir(person_folder):
            continue



        label_names[current_id] = person



        for image_name in os.listdir(person_folder):


            image_path = os.path.join(
                person_folder,
                image_name
            )


            image = cv2.imread(
                image_path
            )


            if image is None:
                continue



            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY
            )



            detected_faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5
            )



            for (x,y,w,h) in detected_faces:


                face = gray[
                    y:y+h,
                    x:x+w
                ]


                faces.append(face)

                labels.append(
                    current_id
                )



        current_id += 1



    if len(faces) == 0:

        print(
            "No faces found for training"
        )

        return



    recognizer.train(
        faces,
        np.array(labels)
    )


    recognizer.save(
        MODEL_FILE
    )


    print(
        "Training complete"
    )


    print(
        label_names
    )



    return label_names




# ==========================
# Load Model
# ==========================

def load_model():


    if not os.path.exists(MODEL_FILE):

        print(
            "Model not found"
        )

        return None



    recognizer.read(
        MODEL_FILE
    )


    print(
        "Face model loaded"
    )


    return recognizer