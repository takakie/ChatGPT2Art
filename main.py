import re

from gpt_api import ImageDescriptionGenerator
from sd_api import MessageToImageProcessor

# 定义配置文件路径
config = "config.json"
# 加载GPT模块
generator = ImageDescriptionGenerator(config)
generator.model = "gpt-3.5"
# 加载stable diffusion模块
sd = MessageToImageProcessor(config)
sd.height = 720
sd.width = 500


while 1:
    symbol_list = []
    description = input("请描述你的图片：")
    if description == "":
        break
    if description[0] == "[":
        symbol_list = re.search(r'\[(.*?)]', description).group(1).split(',')  # 使用逗号进行分割，得到内容列表
        description = re.sub(r'\[(.*?)]', '', description)  # 使用正则表达式删除中括号内容
    print("----------正在生成提示词------------")
    sd_prompt = generator.generate_description(description)
    print("----------正在生成燃烧显卡------------")
    sd.process_message_to_image(sd_prompt, symbol_list)
    print("----------绘画完成------------")
