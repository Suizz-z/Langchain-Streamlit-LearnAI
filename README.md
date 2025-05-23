# Langchain-Streamlit-LearnAI
AI 编程学习助手项目
一、项目概述
AI 编程学习助手是一个基于 Python 和 Streamlit 构建的在线编程学习平台，旨在帮助用户学习各种编程语言。该平台集成了 LangChain 和 DeepSeek 等 AI 技术，提供了学习路径规划、练习题生成、AI 对话等功能，让用户可以更高效地学习编程。
二、功能特性
学习路径规划：根据用户选择的编程语言，生成相应的学习树，帮助用户梳理知识点。
练习题生成：根据用户的学习水平和需求，生成选择题、判断题、填空题等练习题，并提供答案分析和学习建议。
AI 对话：用户可以与 AI 助手进行实时对话，获取编程问题的解答和学习建议。
学习状态总结：定期总结用户的学习状态，包括答题频率、答题内容难度、学习态度等，帮助用户了解自己的学习进度。
用户管理：支持用户注册、登录和注销功能，用户的学习记录会被保存到数据库中。
三、技术栈
前端：Streamlit
后端：Python
数据库：SQLite
AI 模型：DeepSeek
框架：LangChain
四、项目结构
plaintext
ai_aides/
├── .idea/                      # IDE配置文件
│   ├── misc.xml
│   ├── modules.xml
│   ├── .gitignore
│   ├── inspectionProfiles/
│   │   ├── Project_Default.xml
│   │   └── profiles_settings.xml
│   ├── workspace.xml
│   └── dbnavigator.xml
├── Study_tree.py               # 学习树生成模块
├── utils.py                    # 工具函数模块
├── Generate_exercises.py       # 练习题生成模块
├── Study_node.py               # 节点学习模块
├── AI_conversations.py         # AI对话模块
├── prompt.py                   # 提示词配置文件
├── helpers.py                  # 辅助函数模块
├── database.py                 # 数据库操作模块
├── Login_Registration.py       # 用户登录注册模块
└── users.db                    # 用户数据库
└── message_history.db          # 消息历史数据库
五、安装与运行
1. 克隆项目
bash
git clone https://github.com/your-repo/ai_aides.git
cd ai_aides
2. 创建虚拟环境
bash
python -m venv venv
source venv/bin/activate  # 对于Windows用户，使用 `venv\Scripts\activate`
3. 安装依赖
bash
pip install -r requirements.txt
4. 运行项目
bash
streamlit run Login_Registration.py
5. 访问项目
在浏览器中打开 http://localhost:8501 即可访问项目。
六、使用方法
注册与登录：在首页输入用户名、密码和邮箱进行注册，注册成功后即可登录。
学习树生成：登录后，选择想要学习的编程语言，点击 “生成文案” 按钮，系统会生成相应的学习树。
练习题生成：在练习题生成页面，选择编程语言、学习水平、题目类型和数量，点击 “生成练习题” 按钮，系统会生成相应的练习题。
AI 对话：在 AI 对话页面，输入聊天 ID 和聊天内容，即可与 AI 助手进行对话。
学习状态总结：登录后，在首页会显示近期学习总结，帮助用户了解自己的学习进度。
七、注意事项
请确保你已经安装了 Python 3.12 及以上版本。
在使用 AI 功能时，请确保你的网络连接正常。
项目中的 api_key 是示例密钥，请替换为你自己的 DeepSeek API 密钥。
八、贡献
如果你对本项目有任何建议或改进意见，欢迎提交 Pull Request 或 Issue。
九、许可证
本项目采用MIT 许可证。
