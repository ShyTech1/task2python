from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def hello_world():
    return render_template("index.html")

@app.get("/room")
def room():
    return render_template("index.html")

@app.get("/api/chat/<room>")
def get(room):
    return f"We are at room {room}"

@app.post("/api/chat/<room>") #post some data to the server
def post():
    "<h1>POST metod</h1>"


if __name__ == "__main__":
    app.run(debug=True)