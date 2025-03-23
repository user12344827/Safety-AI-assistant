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
        
        # 創建保存目錄（如果不存在）
        os.makedirs(save_dir, exist_ok=True)
    
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
        
        # 保存檢測結果圖片
        results.save(save_dir=self.save_dir)
        
        # 獲取檢測詳細結果
        detections = results.pandas().xyxy[0]
        
        # 分析安全狀態
        safety_status = {
            'file_name': os.path.basename(image_path),
            'has_person': False,
            'has_helmet': False,
            'risk_level': '一般',
            'event_type': '一般',
            'detection_details': []
        }
        
        for _, detection in detections.iterrows():
            object_class = detection['name']
            confidence = detection['confidence']
            
            # 記錄檢測到的物件詳情
            safety_status['detection_details'].append({
                'class': object_class,
                'confidence': confidence
            })
            
            # 檢查是否有人員
            if object_class == 'person':
                safety_status['has_person'] = True
            
            # 檢查是否有安全帽
            if object_class == 'helmet':
                safety_status['has_helmet'] = True
        
        # 判斷危險等級和事件類型
        if safety_status['has_person'] and not safety_status['has_helmet']:
            safety_status['risk_level'] = '危險'
            safety_status['event_type'] = '未戴安全帽'
        
        return detections, safety_status
    
    def print_detection_results(self, detections):
        """
        列印檢測結果的統計資訊
        
        參數:
            detections: 檢測結果DataFrame
        """
        print(f"總共檢測到 {len(detections)} 個物件")
        
        # 顯示每個檢測物件的類別和置信度
        for i, detection in detections.iterrows():
            print(f"物件 {i+1}: 類別={detection['name']}, 置信度={detection['confidence']:.4f}")


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
    print(f"檢測到安全帽: {'是' if safety_status['has_helmet'] else '否'}")
    print(f"風險等級: {safety_status['risk_level']}")
    print(f"事件類型: {safety_status['event_type']}")