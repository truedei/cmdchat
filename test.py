import json

# 打开 JSON 配置文件进行读取
with open('config.json', 'r') as file:
    config_data = json.load(file)

# 现在，config_data 包含了 JSON 配置文件中的数据，可以按需使用它
print(config_data)

config_data["qianfan_info"]["access_token"] = "abc"

# 将配置数据写入 JSON 配置文件
with open('config.json', 'w') as file:
    json.dump(config_data, file, indent=4)


# 打开 JSON 配置文件进行读取
with open('config.json', 'r') as file:
    config_data = json.load(file)

# 现在，config_data 包含了 JSON 配置文件中的数据，可以按需使用它
print(config_data)
