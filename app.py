# import os

# from flask import (Flask, redirect, render_template, request,
#                    send_from_directory, url_for)

# app = Flask(__name__)


# @app.route('/')
# def index():
#    print('Request for index page received')
#    return ('hello, I am running')



# if __name__ == '__main__':
#    app.run()

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def root():
   print("Inside function")
   return("Hello world")


if __name__ == '__main__':
   uvicorn.run(app,host="0.0.0.0",port=8000)
