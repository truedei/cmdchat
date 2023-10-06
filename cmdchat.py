#!/usr/bin/python3
import requests
import json
import config # 引入配置文件操作工具

import audio_ai as audio_ai

class APIQianfan:
    def __init__(self):
        # 创建 Config 对象
        self.cf = config.Config()

        # 配置文件赋值
        self.url = self.cf.config_data["qianfan_conf"]["url"]
        self.APIKey = self.cf.config_data["qianfan_conf"]["APIKey"]
        self.SecretKey = self.cf.config_data["qianfan_conf"]["SecretKey"]

        if "access_token" in self.cf.config_data["qianfan_conf"]:
            self.access_token = self.cf.config_data["qianfan_conf"]["access_token"]
        else:
            self.access_token = ""

        # audio
        self.audio_ai = audio_ai.Audio_AI()

    # 检查是否过期
    def token_is_valid(self):
        # .......
        return True
    
    def get_token(self):
        # 1、检查token是否存在
        if self.access_token != "":
            # 存在，检查是否过期
            if self.token_is_valid():
                # 存在token,并且没过期直接返回给用户
                return self.access_token
        
        # 2、否则重新获取一遍token
        params = {
            "grant_type" : "client_credentials",
            "client_id" : self.APIKey,
            "client_secret" : self.SecretKey,
        }
        response = requests.post(self.url, timeout=10, params=params)
        if response.status_code == 200:
            # 转成JSON
            jsondata = json.loads(response.text)
            # print(jsondata)
            self.access_token = jsondata["access_token"]

            # 保存到config.json中
            self.cf.config_data["qianfan_conf"]["access_token"] = self.access_token
            self.cf.write(self.cf.config_data)
            return self.access_token
        else:
            print("请求失败")
        return ""
    
    def send_chat(self, msg):
        recv_msg = ""
        _url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant"
        # 1、发送消息
        # 封装query消息
        params = { "access_token" : self.get_token() }

        # 封装body参数
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": msg
                }
            ]
        }
        headers = { "Content-Type": "application/json" }
        # 使用 json.dumps() 方法将字典转换为 JSON 格式字符串
        json_data = json.dumps(body, indent=4)  # indent 参数可选，用于格式化输出
        # print("封装body参数=", body)
        # print("封装json_data参数=", json_data)
        response = requests.post(_url, timeout=10, params=params, data=json_data ,headers=headers)
        if response.status_code == 200:
            # 转成JSON
            jsondata = json.loads(response.text)
            # print(jsondata)
            recv_msg = jsondata["result"]
        else:
            print("请求失败")
        # 2、接受&处理 消息
        return recv_msg
    
    def run_loop(self):
        while True:
            # print("##########################")
            # # 使用 input() 函数接收用户输入
            # user_input_msg = input("问:")
            # recv_msg = self.send_chat(user_input_msg)
            # print("答:", recv_msg)
            # print("##########################")

            while True:
                print("##########################")
                # 使用 input() 函数接收用户输入
                print("#指令---> 1:语音输入;2:手动输入;")
                user_input_msg = input("指令:")
                if user_input_msg == "1":
                    print(" 语音输入 ")
                    # 1.录制声音
                    audio_filename = self.audio_ai.audio_record()

                    # 2.识别结果
                    results = self.audio_ai.run_audio_asr(audio_filename)

                    print("问:", results)
                    print("问:", results[0])

                    # 3.将识别结果发送至千帆大模型
                    recv_msg = self.send_chat(results[0])
                    print("答:", recv_msg)

                elif user_input_msg == "2":
                    print(" 手动输入 ")
                    print("##########################")
                    # 使用 input() 函数接收用户输入
                    user_input_msg = input("问:")
                    recv_msg = self.send_chat(user_input_msg)
                    print("答:", recv_msg)
                    print("##########################")
                print("##########################")
    
if __name__ == "__main__":
    print ("########## run main() #############")
    qf = APIQianfan()
    qf.run_loop()