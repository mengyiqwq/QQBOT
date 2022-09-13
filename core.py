import time
import requests
import os
import hashlib
from pydub import AudioSegment
translate_type = {
    "中": "zh-CHS",
    "英": "en"
}

def sexpic():
    pic = requests.get("https://www.dmoe.cc/random.php").url
    cqcode = "[CQ:image,file={0}]".format(pic)
    return cqcode


def mcpic():
    pic = requests.get(
        "https://api.likepoems.com/img/fast/mc.php/?type=JSON").json()["url"]
    cqcode = "[CQ:image,file={0}]".format(pic)
    return cqcode


def perodog():
    words = requests.get("https://api.ixiaowai.cn/tgrj/index.php")
    return words.text


def sayLang(lang_type, role, text):
    if lang_type == 0:
        sounds = "https://moegoe.azurewebsites.net/api/speak?text={0}&id={1}".format(
            text, role)
    if lang_type == 1:
        sounds = "https://moegoe.azurewebsites.net/api/speakkr?text={0}&id={1}".format(
            text, role)
    text=requests.get(sounds).content
    # print(text)
    if os.path.isfile("test.ogg"):
       os.remove("test.ogg")
    # os.remove("/usr/share/nginx/html/sounds/test.mp3")

    with open(r"test.ogg",'ab') as f:
        f.write(text)
        f.flush()
    sourcefile = AudioSegment.from_ogg("test.ogg")
    data=str(time.time())
    filename=hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()+".mp3"
    sourcefile.export("/usr/share/nginx/html/sounds/"+filename, format="mp3")
    # cqcode = "[CQ:record,file={0}]".format(sounds)
    link="http://www.wustone.cn/sounds/"+filename 
    cqcode="[CQ:record,file={0}]".format(link)
    print("音频为", cqcode)
    return cqcode


def translate(type, text):
    word = requests.get(
        "http://fanyi.youdao.com/translate?doctype=json&type={0}&i={1}".format(type, text)).json()
    return word["translateResult"][0][0]["tgt"]


def send_to_person(uid, msg):
    return requests.get(url='http://127.0.0.1:5700/send_private_msg?user_id={0}&&message={1}'.format(uid, msg))


def send_to_group(uid, gid, msg):
    return requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&&message={1}'.format(gid, msg))


def keyword(message, uid, gid=None):
    print(message, uid, gid)
    text = requests.get("https://open.drea.cc/bbsapi/chat/get?keyWord=" +
                        message+"&userName=type%3Dbbs").json()
    if text['isSuccess'] == False:
        pic = "现在我还没有脑袋，请稍后"
    else:
        pic = text['data']['reply']
    if gid != None and message.find("[CQ:at,qq=3298006350]") != -1:
        message = message.replace("[CQ:at,qq=3298006350]", "")
        message = message.lstrip()
        if message.find("涩图") != -1:
            return send_to_group(uid, gid, sexpic())
        if message.find("表情") != -1:
            return send_to_group(uid, gid, mcpic())
        if message.find("舔") != -1:
            return send_to_group(uid, gid, perodog())
        if message.find("让宁宁说") != -1:
            print("宁宁要说了")
            message = message.replace("让宁宁说", "")
            reco= sayLang(0, 0, message)
            return send_to_group(uid,gid,reco)
        if len(message)>3 and message[1] == "译":
            if(translate_type.get(message[0]) != None and translate_type.get(message[2]) != None):
                return send_to_group(uid, gid, translate(translate_type[message[0]]+"2"+translate_type[message[2]], message[3:]))
            return send_to_group(uid, gid, translate("AUTO", message[2:]))
        return send_to_group(uid, gid, pic)
    if gid == None:
        if message.find("涩图") != -1:
            return send_to_person(uid, sexpic())
        if message.find("舔") != -1:
            return send_to_person(uid, perodog())
        if message.find("让宁宁说") != -1:
            print("宁宁要说了")
            message = message.replace("让宁宁说", "")
            reco= sayLang(0, 0, message)
            return send_to_person(uid,reco)
        if message.find("表情") != -1:
            return send_to_group(uid, gid, mcpic())
        if len(message)>=3 and message[1] == "译":
            if(translate_type.get(message[0]) != None and translate_type.get(message[2]) != None):
                return send_to_person(uid, translate(translate_type[message[0]]+"2"+translate_type[message[2]], message[3:]))
            return send_to_person(uid, translate("AUTO", message[2:]))
        return send_to_person(uid, pic)
