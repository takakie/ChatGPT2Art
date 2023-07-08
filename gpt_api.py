import json
import requests
import uuid


# 请求pandora,代理gpt接口实现中文转英文
class ImageDescriptionGenerator:
    def __init__(self, config_file):
        self.config_data = self.load_config(config_file)
        self.init_prompt = self.config_data["init_prompt"]
        self.GPT_URL = self.config_data["gpt_url"]
        self.model = self.config_data["model"]
        self.parent_message_id = str(uuid.uuid4())
        self.conversation_id = ""

    # 用于加载配置文件
    def load_config(self, config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        return config_data

    # 用于调用GPTAPI实现中文转因为prompt
    def generate_description(self, prompt):
        # 设置请求参数
        question = {
            "prompt": self.init_prompt + prompt,
            "model": self.model,
            "message_id": str(uuid.uuid4()),
            "parent_message_id": self.parent_message_id,
            "conversation_id": self.conversation_id,
            "stream": ""
        }
        self.init_prompt = ""
        response = requests.post(url=f'{self.GPT_URL}/api/conversation/talk', json=question)
        message = ""
        # 通过响应码判断是否请求成功
        if response.status_code == 200:
            response_json = response.json()
            # message_josn即为chatgpt的回答内容
            message_json = response_json["message"]["content"]["parts"][0]
            # 但是我们定义的规则就是让chatgpt返回json数据格式，格式为{"prompt": "英文提示词"}
            # message为英文提示词字符串
            message = json.loads(message_json)["prompt"]
            # conversation_id 在当前会话中并不发生改变，在第一次响应包中获取
            self.conversation_id = response_json["conversation_id"]
            # 在每次响应包中获取回答消息的id，设置为下次请求时的父消息id
            self.parent_message_id = response_json["message"]["id"]
            print("生成提示词：" + message)
        else:
            print("Error:", response.status_code)
        return message
