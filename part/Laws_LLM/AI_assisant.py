import os
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

# 設置
database_url = "mysql+mysqlconnector://admin:123456@192.168.1.148/HK"
api_key = os.getenv("OPENAI_API_KEY")

# 初始化資料庫、LLM
db = SQLDatabase.from_uri(database_url)
llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-4",
    openai_api_key=api_key
)

# 修改：只提取相關法規
def get_relevant_laws(event_type):
    # 根據違規類型篩選相關法規
    query = f"""
    SELECT * FROM laws 
    WHERE content LIKE '%{event_type}%' 
    LIMIT 10;
    """
    return db.run(query)
    
# 測試用假資料
images = [
    {
        "file": "image1.jpg", 
        "timestamp": "2024-12-14T20:53:26.557315", 
        "event_type": "未戴安全帽"
    }, 
    {
        "file": "image2.jpg", 
        "timestamp": "2024-12-16T09:53:26.557353",
        "event_type": "高空作業未繫安全帶"
    },
    {
        "file": "image3.jpg", 
        "timestamp": "2024-12-17T20:53:26.557315", 
        "event_type": "安全帶損毀"
    }
]

template = """
你是一個專業的工地安全法規顧問。根據以下資訊，請分析並提供建議：

違規資訊：
檔案: {image_file}
時間: {timestamp} 
類型: {event_type}

相關法規：
{laws_text}

請列出違反的法規條文
"""

prompt = ChatPromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

# 分析所有影像
for image in images:
    # 獲取相關法規
    relevant_laws = get_relevant_laws(image['event_type'])
    
    # 獲取回應
    data = {
        "laws_text":relevant_laws,
        "image_file":image['file'],
        "timestamp":image['timestamp'],
        "event_type":image['event_type']
    }
    
    response = chain.invoke(data)
    response_text = response.get('text', '')
    
    # 輸出結果
    print(f"\n=== 違規分析報告 ===")
    print(f"影像檔案: {image['file']}")
    print(f"違規類型: {image['event_type']}")
    print(f"時間: {image['timestamp']}")
    print("\n分析結果:")
    print(response_text)
    print("="* 50)
