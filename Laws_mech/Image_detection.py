import torch
from PIL import Image
import os

def detect_objects(image_path, model_path='./weights/best.pt', save_dir='./ph_result'):
    """
    使用自訓練的YOLO模型檢測圖片中的物件
    
    參數:
        image_path (str): 要檢測的圖片路徑
        model_path (str): YOLO模型路徑，預設為'./weights/best.pt'
        save_dir (str): 檢測結果保存目錄，預設為'my_results'
    
    回傳:
        results: YOLOv5檢測結果物件
        detections: 包含檢測詳細資訊的DataFrame
    """
    # 加載您自訓練的模型
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    
    # 加載影像檔案
    image = Image.open(image_path)
    
    # 進行推論（物件檢測）
    results = model(image)
    
    # 創建保存目錄（如果不存在）
    os.makedirs(save_dir, exist_ok=True)
    
    # 保存檢測結果影像到文件
    results.save(save_dir=save_dir)
    
    # 獲取檢測的詳細結果
    detections = results.pandas().xyxy[0]  # 將結果轉為 DataFrame
    
    return results, detections

def print_detection_results(detections):
    """
    列印檢測結果的統計資訊
    
    參數:
        detections: 檢測結果DataFrame
    """
    print(f"總共檢測到 {len(detections)} 個物件")
    
    # 顯示每個檢測物件的類別和置信度
    for i, detection in detections.iterrows():
        print(f"物件 {i+1}: 類別={detection['name']}, 置信度={detection['confidence']:.4f}")

# 範例使用方式
if __name__ == "__main__":
    # 基本用法
    results, detections = detect_objects('test1.jpg')
    
    # 顯示檢測結果
    results.show()
    
    # 列印檢測結果統計
    print(detections)
    print_detection_results(detections)
    
    # 進階用法示例 - 自定義模型路徑和保存目錄
    # results2, detections2 = detect_objects(
    #     image_path='other_image.jpg',
    #     model_path='./weights/other_model.pt',
    #     save_dir='custom_results'
    # )