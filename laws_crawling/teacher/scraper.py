from selenium.webdriver.chrome.service import Service
from shutil import which

from db_utils import insert_laws, drop_and_create_db, show_laws_data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_laws():
    # 設定 Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 初始化 WebDriver
    # driver = webdriver.Chrome(options=chrome_options)
    chrome_service = Service(executable_path=which("chromedriver"))
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    print("Accessing website...")

    try:
        driver.get("https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0060014")

        # 等待頁面載入
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "law-article"))
        )
        print("Page loaded successfully")

        laws_data = []
        current_chapter = ""
        rows = driver.find_elements(By.CLASS_NAME, "row")
        print(f"Found {len(rows)} rows")

        for index, row in enumerate(rows, 1):
            try:
                # 檢查是否為章節標題
                chapter_elements = row.find_elements(By.CLASS_NAME, "h3")
                if chapter_elements:
                    current_chapter = chapter_elements[0].text.strip()
                    print(f"\nNew chapter: {current_chapter}")
                    continue

                # 檢查是否有條號
                col_no_elements = row.find_elements(By.CLASS_NAME, "col-no")
                if not col_no_elements:
                    continue

                article_number = col_no_elements[0].text.strip()
                article_link = col_no_elements[0].find_element(By.TAG_NAME, "a").text.strip()

                # 取得條文內容
                content_element = row.find_element(By.CLASS_NAME, "law-article")
                content = content_element.text.strip()

                # 儲存資料
                law_item = {
                    'chapter': current_chapter,
                    'article_number': article_number,
                    'article_link': article_link,
                    'content': content
                }

                laws_data.append(law_item)
                print(f"Processed: {article_number}")

            except Exception as e:
                print(f"\nError processing row {index}: {str(e)}")
                continue

        print("\n\nSample of scraped data (last 5 entries):")
        for item in laws_data[-5:]:
            print("\n" + "="*50)
            print(f"Chapter: {item['chapter']}")
            print(f"Article Number: {item['article_number']}")
            print(f"Article Link: {item['article_link']}")
            print(f"Content: {item['content']}")

        insert_laws(laws_data)
        show_laws_data()
        return laws_data

    finally:
        driver.quit()
        print("\nBrowser closed")

if __name__ == "__main__":
    print("Starting web scraper...")
    drop_and_create_db()
    laws_data = scrape_laws()

    # 統計資訊
    print("\n" + "="*50)
    print(f"Total articles scraped: {len(laws_data)}")

    # 印出所有章節
    chapters = set(item['chapter'] for item in laws_data if item['chapter'])
    print("\nChapters found:")
    for chapter in sorted(chapters):
        print(f"- {chapter}")dd