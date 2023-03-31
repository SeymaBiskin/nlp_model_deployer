from flask import Flask, render_template, request
from chat import chat_logic

app = Flask(__name__)

@app.route("/")
def home():    
    return render_template("home.html") 


@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')
    response = chat_logic(userText)
    # print(response)
    return str(response) 


if __name__ == "__main__":    
    app.run(host= "0.0.0.0",port=4000)