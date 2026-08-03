from face_db import train_faces


print(
    "Starting training..."
)


names = train_faces()



if names:

    print(
        "Registered faces:"
    )

    print(
        names
    )


else:

    print(
        "Training failed"
    )