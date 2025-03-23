import os
from dotenv import load_dotenv
from langchain.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

# 載入環境變數
load_dotenv()

# 從環境變數獲取設定
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
api_key = os.getenv("OPENAI_API_KEY")

# 檢查環境變數是否設置
if not all([db_user, db_password, db_host, db_name, api_key]):
    print("錯誤：未設置完整的環境變數，請檢查.env檔案")
    import sys
    sys.exit(1)

# 設置資料庫連接字串
database_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"

# 初始化資料庫、LLM
db = SQLDatabase.from_uri(database_url)
llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-4",
    openai_api_key=api_key
)

# 提取法規
laws_text = db.run("SELECT * FROM laws;")

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

system_message = """你是一個專業的工地安全法規顧問，能夠根據提供的法規資料回答問題。
請提供以下分析：
1. 違規事實：詳細說明違規情況
2. 違反法規：列出所有被違反的具體法規條文
3. 建議處理：根據法規提供改善建議
4. 可能影響：分析此違規對工地安全的潛在影響
"""

# 建立提示模板
template = """
{system_message}

法規資料:
{laws_text}

問題:
根據 workshop_law 中的法規，分析此影像是否觸犯相關法規。

影像資訊:
- 檔案: {image_file}
- 時間: {timestamp}
- 違規類型: {event_type}

請逐一列出違反的法規條文。
"""

prompt = ChatPromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

# 分析所有影像
if __name__ == "__main__":
    for image in images:
        # 獲取回應
        response = chain.run(
            system_message=system_message,
            laws_text=laws_text,
            image_file=image['file'],
            timestamp=image['timestamp'],
            event_type=image['event_type']
        )
        
        # 輸出結果
        print(f"\n=== 違規分析報告 ===")
        print(f"影像檔案: {image['file']}")
        print(f"違規類型: {image['event_type']}")
        print(f"時間: {image['timestamp']}")
        print("\n分析結果:")
        print(response)
        print("="* 50)