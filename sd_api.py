import io
import base64
import json

import requests
from datetime import datetime
from PIL import Image, PngImagePlugin


class MessageToImageProcessor:
    def __init__(self, config_file):
        # 加载数据
        self.config_data = self.load_config(config_file)
        self.SD_URL = self.config_data["sd_url"]
        # 设置初始化参数
        self.checkpoint = self.config_data["sd_model_checkpoint"]
        self.vae = self.config_data["sd_vae"]
        self.clip_skip = self.config_data["CLIP_stop_at_last_layers"]
        self.set_options()
        # 设置绘画参数
        self.message_add = self.config_data["message_add"]
        self.negative_prompt = self.config_data["negative_prompt"]
        self.sampler_name = self.config_data["sampler_name"]
        self.steps = self.config_data["steps"]
        self.cfg_scale = self.config_data["cfg_scale"]
        self.width = self.config_data["width"]
        self.height = self.config_data["height"]
        self.last_seed = -1

    # 该方法用于加载配置文件
    def load_config(self, config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        return config_data

    # 用于设置模型，vae，clip等参数
    def set_options(self):
        option_payload = {
            "sd_model_checkpoint": self.checkpoint,
            "sd_vae": self.vae,
            "CLIP_stop_at_last_layers": self.clip_skip
        }
        response = requests.post(url=f'{self.SD_URL}/sdapi/v1/options', json=option_payload)
        if response.status_code == 200:
            print("-----------SD初始化成功------------")
        else:
            print("-----------SD初始化失败------------")

    def process_message_to_image(self, prompt, symbol_list):

        payload = {
            "prompt": self.message_add + prompt,
            "steps": self.steps,
            "negative_prompt": self.negative_prompt,
            "width": self.width,
            "height": self.height,
            "cfg_scale": self.cfg_scale,
            "sampler_name": self.sampler_name,
            "seed": -1,
            "batch_size": 1
        }
        # 用于判断用户[]中输入的字符
        # 输入#固定上次种子数.在#后跟种子号，[#265233378]表示自定义种子号
        # 输入[*6]表示表示一次性画6张该提示词的图像
        for i in symbol_list:
            if i[0] == "#":
                if len(i) == 1:
                    payload["seed"] = self.last_seed
                else:
                    payload["seed"] = int(i[1:])
            if i[0] == "*" and len(i) != 1:
                payload["batch_size"] = int(i[1:])
        # 请求文生图功能API，获取图像信息，
        response = requests.post(url=f'{self.SD_URL}/sdapi/v1/txt2img', json=payload)
        r = response.json()
        num = 0
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
            png_payload = {
                "image": "data:image/png;base64," + i
            }
            response2 = requests.post(url=f'{self.SD_URL}/sdapi/v1/png-info', json=png_payload)
            pnginfo = PngImagePlugin.PngInfo()

            # 获取到Seed值，用于之后固定Seed
            info = response2.json().get("info")
            # 获取图片信息字典数据
            split_string = info.split(", ")
            for item in split_string:
                # 变量字典获取到种子这条数据，并且复制给self.lash_seed 用于在下次请求时使用
                if "Seed:" in item:
                    seed_string = item.split(": ")
                    self.last_seed = int(seed_string[1])
                    break

            # 以时间命名保存生成的图片
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d%H%M%S")
            name = "./output/" + formatted_time + str(num if num else "") + '.png'
            num += 1
            # 将获取到的图片信息保存到图片中
            pnginfo.add_text("parameters", info)
            image.save(name, pnginfo=pnginfo)
