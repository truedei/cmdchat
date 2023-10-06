# cmdchat
由千帆大模型平台实现的命令行问答助手，支持语音识别，文字手动输入；

（Command line question and answer assistant, supports speech recognition and manual text input）



# 功能


目前实现了：

1、语音问答助手;
2、文字问答助手;

# 学习资料

Linux命令行机器人之---1.初识百度智能云千帆大模型平台: https://cloud.baidu.com/qianfandev/topic/267409

Linux命令行机器人之---2.初学者快速入门千帆大模型平台: https://cloud.baidu.com/qianfandev/topic/267410

Linux命令行机器人之---3.千帆大模型平台HelloWorld实例: https://cloud.baidu.com/qianfandev/topic/267411

Linux命令行机器人之---(4.)100行代码挑战开发一个完整的命令行机器人: https://cloud.baidu.com/qianfandev/topic/267413

Linux命令行机器人之---5. 语音识别+千帆大模型实现个人专属语音助理: https://cloud.baidu.com/qianfandev/topic/267428


# 其他


config.json:

```json
{
    "qianfan_conf":{
        "url": "https://aip.baidubce.com/oauth/2.0/token",
        "APIKey": "VsysBQ2sY44B47Li712OGyna",
        "SecretKey": "uMQX9PMyAMZdESQm0awlwbmitO868TGH"
    }
}
```


如果想测试音频，可以使用ffplay:
```shell
 ffplay -f s16le -ar 16000 -ac 1 recorded_audio.pcm
```

