import streamlit as st
import pandas as pd

# 讀取 CSV 檔案
df = pd.read_csv("pay2024.csv", encoding="utf-8")

st.title("藥品查詢介面")

# 使用者輸入主成分
keyword = st.text_input("請輸入主成分")

if keyword:
    # 篩選藥品名稱中包含主成分的項目
    result = df[df["藥品名稱"].str.contains(keyword, case=False, na=False)]

    # 將同藥品名稱的數量加總
    summary = result.groupby(["藥品代碼", "藥品名稱"], as_index=False)["數量"].sum()
    summary.rename(columns={"數量": "總量"}, inplace=True)

    st.write("查詢結果：")
    st.dataframe(summary)
