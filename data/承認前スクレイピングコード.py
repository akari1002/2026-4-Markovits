from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def clean_text(text):
    return text.replace('\n', ' ').replace('\r', ' ').strip()

# ブラウザの起動
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# ログイン（手動）
driver.get('https://crowdworks.jp/')
input("ログインが完了したらEnterを押してください：")

max_page = 15
data = []

for page in range(1, max_page + 1):
    if page == 1:
        url = "https://crowdworks.jp/r/job_offers/13043865/task_works?filter=waiting_accept"
    else:
        url = f"https://crowdworks.jp/r/job_offers/13043865/task_works?filter=waiting_accept&page={page}"

    print(f"取得中: {url}")
    driver.get(url)

    try:
        # tableが表示されるまで待つ
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )

        # 行が出るまで待つ
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
        )

        rows = driver.find_elements(By.CSS_SELECTOR, "table tr")[1:]  # ヘッダー除外
        print("行数:", len(rows))

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 4:
                continue

            data.append({
                "ステータス": clean_text(cols[1].text),
                "ワーカー": clean_text(cols[2].text),
                "完了日時": clean_text(cols[3].text),
                "ID": clean_text(cols[4].text),
            })

    except Exception as e:
        print("エラー or データなし:", e)

driver.quit()

# 保存
df = pd.DataFrame(data)
df.to_csv("/Users/sato/Desktop/output.csv", index=False, encoding='utf-8-sig')
print(df)