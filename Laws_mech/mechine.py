import torch
from PIL import Image

# 設定模型（預設使用 YOLOv5s 小型模型）
# 可選模型：yolov5s.pt, yolov5m.pt, yolov5l.pt, yolov5x.pt
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# 加載影像檔案（更換為你的影像路徑）
image_path = 'image.jpg'  # 替換為你的影像檔案
image = Image.open(image_path)

# 進行推論（物件檢測）
results = model(image)

# 顯示檢測結果
results.show()  # 顯示影像和檢測框
# 保存檢測結果影像到文件
results.save(save_dir='runs/detect')

# 獲取檢測的詳細結果
detections = results.pandas().xyxy[0]  # 將結果轉為 DataFrame
print(detections)

# DataFrame 的結構
# - xmin: 邊界框左上角 x 坐標
# - ymin: 邊界框左上角 y 坐標
# - xmax: 邊界框右下角 x 坐標
# - ymax: 邊界框右下角 y 坐標
# - confidence: 檢測置信度
# - class: 類別索引
# - name: 類別名稱
