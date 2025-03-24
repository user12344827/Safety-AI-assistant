# 專案製作：工安影像管理與處理系統

## 主要程式碼

分為四個段落：
1. 影像管理系統 - Image_managrment
2. 法規資料庫爬蟲 - Laws_crawlimg
3. LLM問答系統 - Laws_LLM
4. 影像處理 - Laws_mech

### 影像管理系統 - Image_managrment

運用虛假的影像資料，進行影像管理與分類，包含影像事件定義(一般、危險)、儲存時間。

建立搜尋欄位，便於篩選利特定日期之影像。

code：
```bash=
image_man.py
```

成果展示：
![圖片描述](photo/result_Im.png)

### 法規資料庫爬蟲 - Laws_crawlimg

由老師編寫的爬蟲程式。
從法規資料庫中，爬取法規，存入資料庫中。

code：
```bash=
# 連接資料庫
db_utils.py

# 爬蟲
scraper.py
```
### LLM問答系統 - Laws_LLM

爬取法規資料庫中的法規條文，並存入資料庫中。
運用虛假的影像資訊，讓AI根據資料庫內容進行違規法條判斷。

code：
```bash=
# 連接資料庫
db_utils.py

# 爬蟲
scraper.py

# LLM
AI_assisant.py
```

成果展示：
![圖片描述](photo/result_LLM.png)

### 影像處理 - Laws_mech

運用自己訓練好的Yolo模型，進行工地照片判斷。
判斷是否有配戴安全帽。

code：
```bash=
# 訓練好的yolo模型
best.py

# 工安照片檢測
Image_dectection.py
```

## 最終成品檔案（Integration）

1. det_man：工安圖像管理系統

根據yolo模型檢測，將照片分為兩種事件類別（一般、危險），被分為危險事件的照片會被存在Csv檔案中供AI讀取。

code：
```bash=
# 檢測工安照片
safety_detector.py

# 管理工安照片
safety_image_manager.py

# 主要執行程式
main.py

# 儲存的Csv檔
safety_records.csv
```

2. result_LLM：AI助手回應

將AI連接儲存工安法規之資料庫，設定模板和提示詞，並串接LineBot，AI在讀取Csv檔案內容後，能透過LINE通訊介面，回答違規法條。

code：
```bash=
# 連接資料庫
db_utils.py

# 爬蟲
scraper.py

# LLM（添加聊天函數，用於LineBot串接）
AI_assisant.py

# LineBot回應
Linebot.py
```

注意事項：
LineBot使用前，需先使用Ngrok進行反向代理，再前往
Line Developers頁面中的**Messaging API settings**更改**Webhook URL**。