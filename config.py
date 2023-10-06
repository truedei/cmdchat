#!/usr/bin/python3
import json

class Config:
    def __init__(self):
        self.config_path = "./config.json" 

        # 创建config_data,用于存储json数据
        self.config_data = None

        self.read()

    # 读取json配置文件
    def read(self):
        # 需要增加异常捕捉等代码
        with open(self.config_path, 'r') as file:
            self.config_data = json.load(file)
        return self.config_data

    # 写入json配置文件
    def write(self, config_data):
        with open(self.config_path, 'w') as file:
            json.dump(config_data, file, indent=4)


