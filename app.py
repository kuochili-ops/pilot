import streamlit as st
import pandas as pd

# 上傳 CSV 檔案
uploaded_file = st.file_uploader("請上傳 pay2024(UTF-8).csv 檔案", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("資料預覽：")
    st.dataframe(df)

    # 讓使用者輸入主成分關鍵字查詢
    keyword = st.text_input("請輸入主成分關鍵字查詢：")
    if keyword:
        result = df[df['藥品名稱'].str.contains(keyword, na=False)]
        st.write(f"查詢結果（共 {len(result)} 筆）：")
        st.dataframe(result)
else:
    st.info("請先上傳 CSV 檔案。")
