import torch
from PIL import Image
import os

class SafetyDetector:
    def __init__(self, model_path='./model/best.pt', save_dir='./detection_results'):
        """
        初始化安全帽檢測器
        
        參數:
            model_path (str): YOLO模型路徑
            save_dir (str): 檢測結果保存目錄
        """
        self.model_path = model_path
        self.save_dir = save_dir
        
        # 檢查並確保保存目錄存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            print(f"創建檢測結果目錄: {save_dir}")
        else:
            print(f"使用已存在的檢測結果目錄: {save_dir}")
    
    def detect_objects(self, image_path):
        """
        使用YOLO模型檢測圖片中的物件
        
        參數:
            image_path (str): 要檢測的圖片路徑
        
        回傳:
            detections: 包含檢測詳細資訊的DataFrame
            safety_status: 字典，包含檢測結果的安全狀態
        """
        # 載入模型
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path)
        
        # 載入圖片
        image = Image.open(image_path)
        
        # 進行物件檢測
        results = model(image)
        
        # 保存檢測結果圖片，使用覆蓋模式
        results.save(save_dir=self.save_dir, exist_ok=True)  # 允許覆蓋已存在的檔案
        
        # 獲取檢測詳細結果
        detections = results.pandas().xyxy[0]
        
        # 分析安全狀態 - 新增事件原因欄位
        safety_status = {
            'file_name': os.path.basename(image_path),
            'has_person': False,
            'event_type': '一般',
            'event_reason': ''
        }
        
        # 檢查是否有人員
        for _, detection in detections.iterrows():
            if detection['name'] == 'person':
                safety_status['has_person'] = True
                break
        
        # 修改後的判斷邏輯：只要有人就標記為危險事件，並加入事件原因
        if safety_status['has_person']:
            safety_status['event_type'] = '危險'
            safety_status['event_reason'] = '未戴安全帽'
        
        return detections, safety_status
    
    def print_detection_results(self, detections):
        """
        列印檢測結果的統計資訊
        
        參數:
            detections: 檢測結果DataFrame
        """
        print(f"總共檢測到 {len(detections)} 個物件")
        
        # 顯示每個檢測物件的類別
        class_counts = {}
        for _, detection in detections.iterrows():
            class_name = detection['name']
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        for class_name, count in class_counts.items():
            print(f"檢測到 {count} 個 {class_name}")


# 使用範例
if __name__ == "__main__":
    # 初始化檢測器
    detector = SafetyDetector()
    
    # 檢測圖片
    image_path = 'test1.jpg'
    detections, safety_status = detector.detect_objects(image_path)
    
    # 印出檢測結果
    print("檢測結果:")
    detector.print_detection_results(detections)
    
    # 印出安全狀態
    print("\n安全狀態:")
    print(f"文件名稱: {safety_status['file_name']}")
    print(f"檢測到人員: {'是' if safety_status['has_person'] else '否'}")
    print(f"事件類型: {safety_status['event_type']}")
    if safety_status['event_type'] == '危險':
        print(f"事件原因: {safety_status['event_reason']}")