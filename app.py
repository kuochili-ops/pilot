import streamlit as st
import pandas as pd

st.title("健保藥品查詢系統")

# 上傳 CSV 檔案
uploaded_file = st.file_uploader("請上傳 pay2024 (UTF-8).csv 檔案", type="csv")

if uploaded_file is not None:
    # 讀取 CSV
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.write("資料預覽：")
    st.dataframe(df)

    # 多關鍵字輸入
    keywords_input = st.text_input("請輸入多個關鍵字（用逗號分隔）：").strip()
    search_mode = st.radio("搜尋模式", ["AND", "OR"])

    # 價格篩選
    if '價格' in df.columns:
        min_price = st.number_input("最低價", value=0)
        max_price = st.number_input("最高價", value=100000)
    else:
        min_price, max_price = None, None

    if keywords_input:
        keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]

        if search_mode == "AND":
            mask = df['藥品名稱'].apply(lambda x: all(kw.lower() in str(x).lower() for kw in keywords))
        else:
            mask = df['藥品名稱'].apply(lambda x: any(kw.lower() in str(x).lower() for kw in keywords))

        # 價格篩選
        if '價格' in df.columns:
            price_mask = (df['價格'] >= min_price) & (df['價格'] <= max_price)
            result = df[mask & price_mask]
        else:
            result = df[mask]

        st.write(f"查詢結果（共 {len(result)} 筆）：")
        st.dataframe(result)

        # 統計分析
        if '價格' in result.columns and not result.empty:
            st.subheader("統計分析")
            st.write(f"平均價：{result['價格'].mean():.2f}")
            st.write(f"最高價：{result['價格'].max():.2f}")
            st.write(f"最低價：{result['價格'].min():.2f}")

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

