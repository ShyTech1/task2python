from flask import Flask, render_template, request, Response
from datetime import datetime
from threading import Lock
from pathlib import Path


app = Flask(__name__)


BASE_DIR = Path(__file__).resolve().parent
CHATS_DIR = BASE_DIR / "chats"
CHATS_DIR.mkdir(exist_ok=True)

file_lock = Lock()

def room_file(room):
    return CHATS_DIR / f"{room}.txt"

def format_line(username, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{ts}] {username}: {msg}"

@app.get("/")
def restart():
    return render_template("index.html")

@app.get("/<room>")
def hello_world(room):
    return render_template("index.html")
    


@app.post("/api/chat/<room>")
def post_chat(room):
    username = (request.form.get("username") or "").strip()
    message = (request.form.get("msg") or "").strip()


    if not username or not message:
        return Response("Missing data", status=400)
    
    path = room_file(room)
    line = format_line(username, message)

    with file_lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    return Response("OK", status=201)


@app.get("/api/chat/<room>")
def get_chat(room):
    path = room_file(room)
    lines = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            lines.append(line)
    
    return lines

    

    




if __name__ == "__main__":
    app.run(debug=True)