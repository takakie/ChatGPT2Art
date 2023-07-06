# 调用ChatGPT API开发 实现中文AI绘画

## 1.框架

一个主程序MAIN，两个类,一个json格式的配置文件。

### 1.1.ImageDescriptionGenerator

​	这个类用来实现调用我搭建好的pandora chatgpt API接口，根据我们提供的中文描述，生成英文AI绘画提示词。

### 1.2.MessageToImageProcessor

​	通过生成的AI提升词，调用stable diffusion 的API 的文生图接口实现AI绘画出图。

### 1.3.主程序main 

​	实现对两个类的调用，同时设置可选参数。

### 1.4.配置config.json

​	配置初始的配置参数。

