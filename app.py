import streamlit as st
import pandas as pd

# 讀取 CSV 檔案
df = pd.read_csv("20025 mount.csv", sep="\t")

st.title("藥品查詢介面")
st.write("輸入主成分，顯示藥品代碼、藥品名稱、數量加總")

# 使用者輸入主成分
ingredient = st.text_input("請輸入主成分")

if ingredient:
    # 篩選含有主成分的資料
    filtered = df[df['藥品名稱'].str.contains(ingredient, case=False, na=False)]
    
    # 依藥品代碼與名稱加總數量
    result = filtered.groupby(['藥品代碼', '藥品名稱'], as_index=False)['數量'].sum()
    
    # 顯示結果表格
    st.dataframe(result)
    
    # 顯示總數量
    total = result['數量'].sum()
    st.write(f"👉 主成分 **{ingredient}** 的總數量：{total}")
