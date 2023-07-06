import json
import requests
import uuid


class ImageDescriptionGenerator:
    def __init__(self, config_file):
        self.config_data = self.load_config(config_file)
        self.init_prompt = self.config_data["init_prompt"]
        self.GPT_URL = self.config_data["gpt_url"]
        self.model = self.config_data["model"]
        self.parent_message_id = str(uuid.uuid4())
        self.conversation_id = ""

    def load_config(self, config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        return config_data

    def generate_description(self, prompt):
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
        if response.status_code == 200:
            response_json = response.json()
            message_json = response_json["message"]["content"]["parts"][0]
            message = json.loads(message_json)["prompt"]
            self.conversation_id = response_json["conversation_id"]
            self.parent_message_id = response_json["message"]["id"]
            print("生成提示词：" + message)
        else:
            print("Error:", response.status_code)
        return message



