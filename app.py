import streamlit as st
import pandas as pd

# 上傳 CSV 檔案
uploaded_file = st.file_uploader("請上傳 pay2024(UTF-8).csv 檔案", type="csv")

if uploaded_file is not None:
    # 讀取 CSV
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.write("資料預覽：")
    st.dataframe(df)

    # 多關鍵字輸入
    keywords_input = st.text_input("請輸入多個關鍵字（用逗號分隔）：").strip()
    search_mode = st.radio("搜尋模式", ["AND", "OR"])

    if keywords_input:
        keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]

        if search_mode == "AND":
            # AND 條件：每個關鍵字都必須出現在藥品名稱中
            mask = df['藥品名稱'].apply(lambda x: all(kw.lower() in str(x).lower() for kw in keywords))
        else:
            # OR 條件：只要有一個關鍵字出現在藥品名稱中
            mask = df['藥品名稱'].apply(lambda x: any(kw.lower() in str(x).lower() for kw in keywords))

        result = df[mask]
        st.write(f"查詢結果（共 {len(result)} 筆）：")
        st.dataframe(result)

        # 提供下載結果功能
        csv = result.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="下載查詢結果 CSV",
            data=csv,
            file_name="query_result.csv",
            mime="text/csv"
        )
else:
    st.info("請先上傳 CSV 檔案。")
