# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 10:48 PM
# @Author  : Python疯子
# @File    : main.py
# @Software: PyCharm

import time
import requests

# 在线合成音频标贝
from thread_tools import MyThread

AI_URL = "http://39.104.162.93:8027/tts?user_id=speech&domain=1&language=zh&speed=5&text={}"

def set_voice(text):
    tts_start_time = time.time()  # 进入函数时计一个时间

    voice_url = AI_URL.format(text)
    f = requests.get(voice_url)
    voice = f.content

    tts_time_data = int((time.time() - tts_start_time) * 1000)
    print("tts_time_data：", tts_time_data)

    return voice


def normal_voice(list):
    start_time = time.time()  # 进入函数时计一个时间

    # 音频数据拼接
    voice_data = bytes()
    for obj in list:
        temp_data = set_voice(obj)
        voice_data += temp_data

    time_data = int((time.time() - start_time) * 1000)
    print("time_data：", time_data)

    save_voice(voice_data)

def save_voice(voice_data):
    with open("./voice.wav", "wb") as f:
        f.write(voice_data)

'''--------------------------分割线-------------------------'''

def set_voice2(info):
    tts_start_time = time.time()  # 进入函数时计一个时间
    text = info.get("sentence")
    voice_url = AI_URL.format(text)
    f = requests.get(voice_url)
    voice = f.content

    tts_time_data = int((time.time() - tts_start_time) * 1000)
    print(str(info.get("sort")) + "--tts_time_data：", tts_time_data)

    voice_info = {
        "voice":voice,
        "sort":info.get("sort")
        }

    return voice_info


def my_thread(my_list):
    start_time = time.time()  # 进入函数时计一个时间

    tts_list = []
    voice_list = []
    # 排序，添加序号
    for index in range(len(my_list)):
        tmp_dict = {"sentence":my_list[index],
                    "sort":index}

        tts_list.append(tmp_dict)

    li = []
    for tts_info in tts_list:
        t = MyThread(set_voice2, args=(tts_info,))
        li.append(t)
        t.start()
    for t in li:
        t.join()  # 一定要join，不然主线程比子线程跑的快，会拿不到结果

        # 接收返回结果
        voice_list.append(t.get_result())

    # 先根据sort排序 在遍历拼接
    voice_list.sort(key=lambda temp: temp['sort'])
    voice_data = bytes()

    for voice in voice_list:
        voice_data += voice.get("voice")

    time_data = int((time.time() - start_time) * 1000)
    print("time_data：", time_data)

    save_voice(voice_data)



    # [{'sentence': '我的公众号是Python疯子', 'sort': 0}, {'sentence': '内容没有花架子', 'sort': 1},
    #  {'sentence': '都是真实案例', 'sort': 2}, {'sentence': '欢迎您的关注', 'sort': 3}]


if __name__ == '__main__':
    my_list = ["我的公众号是Python疯子", "内容没有花架子", "都是真实案例","欢迎您的关注"]
    # normal_voice(my_list)
    my_thread(my_list)
