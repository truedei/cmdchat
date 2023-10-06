import config

cf = config.Config()
config_data = cf.read()
print(config_data)

config_data["aaa"]="sss"

cf.write(config_data)

