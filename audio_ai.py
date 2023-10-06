import pyaudio
import wave
import requests
import json
import base64
import time

timer = time.perf_counter

API_KEY = 'zlUS37GiwB7XwZH1lVfoeUoZ'
SECRET_KEY = '8czlwga9ruQHAz6cyTwOx8AkteyiKbp8'

# 需要识别的文件
# AUDIO_FILE = './16k.pcm'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
AUDIO_FILE = './recorded_audio.pcm'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
# 文件格式
FORMAT = AUDIO_FILE[-3:]  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式

CUID = '123456PYTHON'
# 采样率
RATE = 16000  # 固定值

# 普通版
DEV_PID = 1537  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
ASR_URL = 'http://vop.baidu.com/server_api'

TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'

    
class Audio_AI:
    def __init__(self):
        # 配置录音参数
        self.FORMAT = pyaudio.paInt16  # 音频格式，可以根据需要选择
        self.CHANNELS = 1  # 声道数（单声道）
        self.RATE = 16000  # 采样率，可以根据需要选择
        self.RECORD_SECONDS = 5  # 录制时长（秒）
        self.OUTPUT_FILENAME = "recorded_audio.pcm"  # 输出文件名

    def audio_record(self):
        # 初始化PyAudio
        audio = pyaudio.PyAudio()

        # 打开音频输入流
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=1024)

        print("开始录制...")

        frames = []

        # 录制音频
        for i in range(0, int(self.RATE / 1024 * self.RECORD_SECONDS)):
            data = stream.read(1024)
            frames.append(data)

        print("录制完成.")

        # 停止音频流
        stream.stop_stream()
        stream.close()

        # 关闭PyAudio
        audio.terminate()

        # 保存录音结果为WAV文件
        with wave.open(self.OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

        # print(f"音频已保存为 {self.OUTPUT_FILENAME}")
        return self.OUTPUT_FILENAME
    
    def get_token(self):
        # 组装数据
        params = {
                'grant_type': 'client_credentials',
                'client_id': API_KEY,
                'client_secret': SECRET_KEY
        }

        response = requests.post(TOKEN_URL, timeout=10, params=params)
        if response.status_code == 200:
            # 转成JSON
            result = json.loads(response.text)
            # print(result)
            if ('access_token' in result.keys() and 'scope' in result.keys()):
                return result['access_token']
            else:
                print("获取token失败!")
        else:
            print("请求失败")
    def read_audio_data(self, audio_filename):
        speech_data = []
        with open(audio_filename, 'rb') as speech_file:
            speech_data = speech_file.read()
        return speech_data
    
    def asr_audio(self, speech_data, length, token):
        # 进行base64编码
        speech = base64.b64encode(speech_data)
        speech = str(speech, 'utf-8')

        headers = { "Content-Type": "application/json" }
        
        # 封装识别API请求的参数
        body = {'dev_pid': DEV_PID,
                #"lm_id" : LM_ID,    #测试自训练平台开启此项
                'format': FORMAT,
                'rate': RATE,
                'token': token,
                'cuid': CUID,
                'channel': 1,
                'speech': speech,
                'len': length
                }
        
        result = {}

        begin = timer()

        json_data = json.dumps(body, indent=4)  # indent 参数可选，用于格式化输出

        response = requests.post(ASR_URL,headers=headers, timeout=10, data=json_data)

        # print(response.status_code)
        if response.status_code == 200:
            # 转成JSON
            result_json = json.loads(response.text)
            result = result_json["result"]
        else:
            print("请求失败")
        
        print ("Request time cost %f" % (timer() - begin))

        return result
    
    def run_audio_asr(self, audio_filename):
        # 获取token
        token = self.get_token()
        # print("get token:", token)

        # 读取音频文件
        speech_data = self.read_audio_data(audio_filename)

        length = len(speech_data)
        if length == 0:
            print("发送识别失败，录音数据可能为空")
        else:
            result = self.asr_audio(speech_data, length, token)
            print(result)
            return result