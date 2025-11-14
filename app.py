import streamlit as st
import pandas as pd

# 讀取 CSV 檔案
df = pd.read_csv("pay2024 (UTF-8).csv", encoding="utf-8")

st.title("2024 健保申報藥品數量查詢介面（測試 A 版）")

# 使用者輸入主成分
keyword = st.text_input("請輸入主成分")

def get_online_codes(keyword):
    url = f"https://www.nhi.gov.tw/QueryN/Query3.aspx?KeyWord={keyword}"
    tables = pd.read_html(url)
    codes = set()
    for table in tables:
        if "藥品代碼" in table.columns and "藥商名稱" in table.columns:
            filtered = table[table["藥商名稱"].isin(["中國化學", "中化裕民"])]
            codes.update(filtered["藥品代碼"].astype(str))
    return codes

if keyword:
    # 取得網站藥品代碼
    online_codes = get_online_codes(keyword)

    # 篩選藥品名稱中包含主成分的項目
    result = df[df["藥品名稱"].str.contains(keyword, case=False, na=False)]

    # 將同藥品名稱的數量加總
    summary = result.groupby(["藥品代碼", "藥品名稱"], as_index=False)["數量"].sum()
    summary.rename(columns={"數量": "總量"}, inplace=True)

    # 標示藥品代碼（紅色）
    def highlight_code(row):
        color = "background-color: red" if str(row["藥品代碼"]) in online_codes else ""
        return [color, "", ""]

    st.write("查詢結果：")
    st.dataframe(summary.style.apply(highlight_code, axis=1))
