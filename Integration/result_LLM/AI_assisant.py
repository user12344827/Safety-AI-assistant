import json
import os
import openai
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

# 初始化資料庫、LLM
def init_db_and_llm():
    # 檢查環境變數是否設置
    if not all([db_user, db_password, db_host, db_name, api_key]):
        print("錯誤：未設置完整的環境變數，請檢查.env檔案")
        return None, None
    
    # 設置資料庫連接字串
    database_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
    
    # 初始化資料庫
    try:
        db = SQLDatabase.from_uri(database_url)
    except Exception as e:
        print(f"資料庫連接錯誤: {e}")
        return None, None
    
    # 初始化 LLM
    llm = ChatOpenAI(
        temperature=0.7,
        model_name="gpt-4",
        openai_api_key=api_key
    )
    
    return db, llm

# 原有的 OpenAI 聊天函數
def general_chat(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": text}
        ]
    )
    
    print(completion)
    return completion.choices[0].message.content

# 工地安全法規分析函數
def safety_analysis(text):
    db, llm = init_db_and_llm()
    if not db or not llm:
        return "系統錯誤：無法連接資料庫或初始化AI模型。請確認環境設定正確。"
    
    # 提取法規
    try:
        laws_text = db.run("SELECT * FROM laws;")
    except Exception as e:
        print(f"資料庫查詢錯誤: {e}")
        return f"資料庫查詢錯誤: {e}"
    
    # 分析使用者訊息，嘗試提取事件類型
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
    
    使用者提問或描述的違規情況:
    {user_text}
    
    請根據法規資料分析此情況是否違反相關法規，並提供詳細說明。如果使用者只是打招呼或提出與工地安全無關的問題，請回覆「您好，我是工地安全法規顧問，可以幫您分析工地安全相關法規問題。」
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # 獲取回應
    try:
        response = chain.run(
            system_message=system_message,
            laws_text=laws_text,
            user_text=text
        )
        return response
    except Exception as e:
        print(f"AI分析錯誤: {e}")
        return f"AI分析發生錯誤: {e}"

# 主要的聊天函數，只回覆工地安全法規相關問題
def chat(text):
    # 判斷是否為工地安全相關問題
    safety_keywords = ["工地", "安全帽", "安全帶", "危險", "違規", "法規", "勞工", "高空作業", "意外", "事故", "職災", "營造", "工安"]
    
    # 檢查訊息是否包含安全關鍵字
    is_safety_related = any(keyword in text for keyword in safety_keywords)
    
    if is_safety_related:
        # 使用法規分析功能
        return safety_analysis(text)
    else:
        # 不回覆非工地安全相關問題
        return "您好，我是工地安全法規顧問，僅能回答工地安全與相關法規問題。請提出與工地安全、職業安全衛生法規相關的問題，我將為您提供專業分析。"

# 測試用
if __name__ == "__main__":
    test_text = "工地上有人未戴安全帽，這違反了哪些法規？"
    print(chat(test_text))