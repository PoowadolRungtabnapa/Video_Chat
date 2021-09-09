from flask import Flask, render_template, request

app = Flask(__name__)
Message = []
@app.route('/', methods=["GET",'POST'])
def index() :
    
    if request.method == "POST" and "name" in request.form :
        msg = request.form['name']
        Message.append(msg)
        return render_template("index.html", msg=Message)
    else :
        msg = ""
        return render_template("index.html", msg=msg)

if __name__ == '__main__' :
    app.run(debug=True)