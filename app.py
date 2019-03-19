from flask import Flask, render_template, request
import recognizeOnline

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("./index.html")

@app.route('/receiver', methods = ['POST'])
def receiver():
    data = request.get_data()
    result = data.decode("utf-8")
    result = result.split("X")
    result = [i[1:len(i)-2] for i in result]
    Xcoord, Ycoord = [(int)(i) for i in result[0].split(",")], [(int)(i) for i in result[1].split(",")]
    Xcoord, Ycoord = Xcoord[:len(Xcoord)-1], Ycoord[:len(Xcoord)-1]
    if (len(Xcoord) < 35):
        return "Try again with more points!"
    string, score = recognizeOnline.recognize(Xcoord, Ycoord)
    return ('Predicted Shape: %s\n Score: %s'%(string, score))

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 80)
