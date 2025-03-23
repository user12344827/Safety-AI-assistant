from datetime import datetime
import os
import csv
import pandas as pd

class SafetyImageManager:
    def __init__(self, csv_path='safety_records.csv'):
        """
        初始化安全圖像管理器
        
        參數:
            csv_path (str): CSV記錄檔案的路徑
        """
        self.images = {}
        self.csv_path = csv_path
        
        # 創建CSV並添加標題行
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['檔案名稱', '時間戳記', '事件類型', '事件原因'])
    
    def add_safety_record(self, file_name, safety_status, timestamp=None):
        """
        新增安全記錄，只儲存危險事件
        
        參數:
            file_name (str): 圖片檔案名稱
            safety_status (dict): 安全狀態資訊，包含 event_type 和 event_reason
            timestamp (str, optional): 時間戳記，如果未提供，則使用當前時間
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        # 儲存圖片的安全記錄
        if safety_status['event_type'] == '危險':
            self.images[file_name] = {
                'timestamp': timestamp,
                'event_type': safety_status['event_type'],
                'event_reason': safety_status['event_reason']
            }
            
            # 危險事件寫入CSV
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    file_name,
                    timestamp,
                    safety_status['event_type'],
                    safety_status['event_reason']
                ])
            
            print(f"危險影像 '{file_name}' 已記錄, 儲存時間：{timestamp}, 事件原因：{safety_status['event_reason']}。")
        else:
            print(f"一般影像 '{file_name}' 不記錄至CSV。")
    
    def display_all_images(self):
        """顯示所有記錄的危險圖像資訊"""
        print("所有危險影像資訊：")
        for file_name, details in self.images.items():
            print(f"影像名稱：{file_name}, 儲存時間：{details['timestamp']}, 事件原因：{details['event_reason']}")

    def display_all_records(self):
        """顯示所有安全記錄"""
        if os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            print(f"共有 {len(df)} 筆危險事件記錄")
            print(df)
        else:
            print("尚無安全記錄")
    
    def filter_by_date(self, date_str):
        """
        根據日期過濾安全記錄
        
        參數:
            date_str (str): 日期字串，格式為 YYYY-MM-DD
        """
        if os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            # 將時間戳記轉換為日期時間格式
            df['日期'] = pd.to_datetime(df['時間戳記']).dt.date
            filter_date = datetime.fromisoformat(date_str).date()
            
            # 過濾出指定日期之後的記錄
            filtered_df = df[df['日期'] >= filter_date]
            
            print(f"在 {date_str} 之後的危險事件記錄:")
            print(filtered_df)
        else:
            print("尚無安全記錄")
    
    def filter_by_reason(self, reason):
        """
        根據事件原因過濾安全記錄
        
        參數:
            reason (str): 事件原因
        """
        if os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            filtered_df = df[df['事件原因'] == reason]
            
            print(f"事件原因為 '{reason}' 的記錄:")
            print(filtered_df)
        else:
            print("尚無安全記錄")


if __name__ == "__main__":
    # 初始化安全圖像管理器
    manager = SafetyImageManager()
    
    # 模擬添加一些安全記錄
    manager.add_safety_record("image1.jpg", {
        'event_type': '危險',
        'event_reason': '未戴安全帽'
    })
    
    manager.add_safety_record("image2.jpg", {
        'event_type': '一般',
        'event_reason': ''
    })
    
    # 顯示所有危險圖像
    manager.display_all_images()
    
    # 顯示所有記錄
    manager.display_all_records()
    
    # 過濾記錄
    today = datetime.now().date().isoformat()
    manager.filter_by_date(today)
    manager.filter_by_reason('未戴安全帽')