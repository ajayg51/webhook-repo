from flask import Flask, render_template
from app import create_app

# from app.template import *

# app = create_app()


app = Flask(__name__,  template_folder='template')

@app.route('/', methods=["GET"])
def get_root():
    # return "Hello world"
    return render_template('home.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)
