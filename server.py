from flask import Flask, send_from_directory
import os


app = Flask(__name__)


IMAGE_FOLDER = "unknown_faces"


@app.route("/unknown/<filename>")
def send_image(filename):

    return send_from_directory(
        IMAGE_FOLDER,
        filename
    )



if __name__ == "__main__":

    print("Image server running")

    app.run(
        host="0.0.0.0",
        port=5000
    )