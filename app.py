import streamlit as st

st.title("智慧營養規劃系統")

st.write("第一個 Streamlit 成功畫面 🎉")

name = st.text_input("請輸入姓名")

if st.button("送出"):
    st.write(f"你好，{name}！")