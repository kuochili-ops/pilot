import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Step 1: 爬取健保署資料（支援分頁）
def get_drug_codes(keyword):
    base_url = "https://info.nhi.gov.tw/INAE3000/INAE3000S01"
    page = 1
    drug_codes = []

    while True:
        payload = {
            "ingredient": keyword,
            "page": page
        }
        response = requests.post(base_url, data=payload)
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select("table tr")
        if len(rows) <= 1:  # 沒有資料
            break

        for row in rows[1:]:
            cols = [col.text.strip() for col in row.find_all("td")]
            if len(cols) > 5:
                drug_code = cols[0]
                vendor = cols[4]
                if "中國化學" in vendor or "中化裕民" in vendor:
                    drug_codes.append(drug_code)

        page += 1

    return list(set(drug_codes))  # 去重

# Step 2: Streamlit UI
st.title("藥品代碼比對工具")

uploaded_file = st.file_uploader("請上傳 pay2024(UTF-8).csv 檔案", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.write("資料預覽：")
    st.dataframe(df)

    keyword = st.text_input("請輸入成分名稱：").strip()
    if keyword:
        st.write("正在搜尋健保署資料，請稍候...")
        drug_codes = get_drug_codes(keyword)
        st.write(f"找到 {len(drug_codes)} 個藥品代碼：", drug_codes)

        # Step 3: 比對 CSV
        result = df[df['藥品代碼'].isin(drug_codes)]

        # Step 4: 標示紅色
        def highlight_red(val):
            return 'color: red' if val in drug_codes else ''

        st.write(f"查詢結果（共 {len(result)} 筆）：")
        st.dataframe(result.style.applymap(highlight_red, subset=['藥品代碼']))

        # 提供下載結果
        csv = result.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="下載查詢結果 CSV",
            data=csv,
            file_name="query_result.csv",
            mime="text/csv"
        )
else:
    st.info("請先上傳 CSV 檔案。")
