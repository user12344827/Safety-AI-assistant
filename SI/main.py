import os
from safety_detector import SafetyDetector
from safety_image_manager import SafetyImageManager

def main():
    """主程式：結合安全帽檢測和圖像管理功能"""
    print("===== 工地安全帽檢測與記錄系統 =====")
    
    # 初始化檢測器和圖像管理器
    detector = SafetyDetector()
    image_manager = SafetyImageManager()
    
    # 設定需要處理的圖片目錄
    image_dir = './images'
    
    # 檢查目錄是否存在
    if not os.path.exists(image_dir):
        print(f"圖片目錄 '{image_dir}' 不存在，正在創建...")
        os.makedirs(image_dir)
        print(f"請將要分析的圖片放入 '{image_dir}' 目錄中，然後重新執行程式")
        return
    
    # 獲取目錄中的所有圖片
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print(f"'{image_dir}' 目錄中沒有找到圖片")
        return
    
    print(f"找到 {len(image_files)} 張圖片，開始處理...")
    
    # 處理每一張圖片
    for file_name in image_files:
        image_path = os.path.join(image_dir, file_name)
        print(f"\n處理圖片: {file_name}")
        
        try:
            # 使用YOLO模型檢測物件
            detections, safety_status = detector.detect_objects(image_path)
            
            # 印出檢測結果
            detector.print_detection_results(detections)
            
            # 將安全記錄添加到圖像管理器
            image_manager.add_safety_record(file_name, safety_status)
            
            # 打印安全狀態
            if safety_status['risk_level'] == '危險':
                print(f"⚠️ 警告: 圖片 {file_name} 中檢測到安全問題 - {safety_status['event_type']}")
            else:
                print(f"✓ 圖片 {file_name} 安全檢查通過")
                
        except Exception as e:
            print(f"處理圖片 {file_name} 時出錯: {str(e)}")
    
    print("\n===== 所有圖片處理完成 =====")
    
    # 顯示所有記錄
    print("\n安全檢測記錄摘要:")
    image_manager.display_all_records()
    
    # 過濾危險記錄
    print("\n危險事件記錄:")
    image_manager.filter_by_risk()


if __name__ == "__main__":
    main()