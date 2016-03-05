# coding=utf-8
__author__ = 'jing'

from flask import Flask, render_template # 导入渲染函数
import pymongo
from settings import MONGO_URI, MONGO_DATABASE

app = Flask(__name__)  # 用内置变量__name__来实例化Flask框架

@app.route("/")  # 这里的路径是基本域名之后的路径! 当返回路径为"/"时,即返回路径为基本域名时,用这个hello()处理
def hello():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    jokes = db["QiubaiItem"].find()
    client.close()
    return render_template("qiubai_index.html", p_jokes=jokes) # render_template()里面添加的任何参数变量可以在qiubai_index.html中用liquid tag和output的方式显示出来!

if __name__ == "__main__":
    app.run()
