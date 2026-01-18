from flask import Flask, render_template, request
import speech_recognition as sr
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return "No file uploaded"

    file = request.files["audio"]

    if file.filename == "":
        return "No file selected"

    if not file.filename.lower().endswith(".wav"):
        return "Please upload only WAV files"

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)

        # OFFLINE RECOGNITION
        text = recognizer.recognize_sphinx(audio_data)

    except sr.UnknownValueError:
        return "Speech could not be understood"
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

    return f"""
    <h2>Transcribed Text</h2>
    <p>{text}</p>
    <br>
    <a href="/">Upload another audio</a>
    """


if __name__ == "__main__":
    app.run(debug=True)
