#coding=utf-8
from flask import Flask,request
from core import keyword
app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True
@app.route('/',methods=["POST"])
def hello_world():
    if request.get_json().get('message_type')=='private':
        uid=request.get_json().get('sender').get('user_id')
        message=request.get_json().get('raw_message')
        keyword(message,uid)
    if request.get_json().get('message_type')=='group':
        gid=request.get_json().get('group_id')
        uid=request.get_json().get('sender').get('user_id')
        message=request.get_json().get('raw_message')
        keyword(message,uid,gid)
    print("hello")
    return 'Hello, World!'
if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=5000)