from datetime import datetime, timedelta
import random

class ImageManager:
    def __init__(self):
        self.image= {}
    
    def add_image(self, file_name, event_type):
        timestamp = (datetime.now() - timedelta(hours=random.randint(0, 48))).isoformat()
        event_type = random.choice(["一般", "危險"])
        self.image[file_name] = {
            "timestamp":timestamp,
            "event_type":event_type
        }
        print(f"影像'{file_name}'已新增, 儲存時間：{timestamp}, 事件類型：{event_type}。")

    def display_all_images(self):
        print("所有影像資訊：")
        for file_name, details in self.image.items():
            print(f"影像名稱：{file_name}, 儲存時間：{details['timestamp']}, 事件類型：{details['event_type']}")

    def filter_by_date(self, date_str): 
        date_threshold = datetime.fromisoformat(date_str)
        print(f"儲存時間在 {date_threshold.date()} 之後的影像:")
        for file_name, details in self.image.items():
            image_time = datetime.fromisoformat(details["timestamp"])
            if image_time > date_threshold:
                print(f"影像名稱: {file_name}, 儲存時間: {details['timestamp']}, 事件類型: {details['event_type']}")

if __name__=="__main__": 
    manager = ImageManager()

manager.add_image("image1.jpg", "event_type")
manager.add_image("image2.jpg", "event_type")
manager.add_image("image3.jpg", "event_type")

manager.display_all_images()

date_input = input("請輸入篩選日期 (格式 YYYY-MM-DD): ")
manager.filter_by_date(date_input)
