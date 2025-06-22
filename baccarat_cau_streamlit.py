import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Phân Tích Cầu Baccarat", layout="wide")

# Header
st.title("🔍 AI Phân Tích Cầu Baccarat")
st.markdown("""
Phát hiện & phân tích các dạng **cầu** trong Baccarat dựa trên lịch sử ván chơi.
Kết hợp phân tích truyền thống, phản cầu, và chỉ số tâm lý (Confidence Engine).
""")

# Nhập dữ liệu lịch sử bàn chơi
data_input = st.text_area("📋 Nhập kết quả ván (P/B/T) theo hàng dọc hoặc cách nhau bởi dấu cách:",
                          placeholder="Ví dụ: P B P B B P T P B ...")

# Chuyển dữ liệu thành danh sách
results = []
if data_input:
    results = data_input.replace("\n", " ").split()
    results = [x.upper() for x in results if x.upper() in ["P", "B", "T"]]

    df = pd.DataFrame({"Ván": np.arange(1, len(results)+1), "Kết Quả": results})
    st.dataframe(df)

    # Phân tích thống kê đơn giản
    p_count = results.count("P")
    b_count = results.count("B")
    t_count = results.count("T")
    total = len(results)

    st.subheader("📊 Thống Kê Tỷ Lệ")
    st.markdown(f"- Player (P): {p_count} lần ({(p_count/total*100):.1f}%)")
    st.markdown(f"- Banker (B): {b_count} lần ({(b_count/total*100):.1f}%)")
    st.markdown(f"- Tie (T): {t_count} lần ({(t_count/total*100):.1f}%)")

    # Vẽ biểu đồ
    fig, ax = plt.subplots()
    ax.bar(["P", "B", "T"], [p_count, b_count, t_count])
    ax.set_title("Tần suất xuất hiện")
    st.pyplot(fig)

    # Phát hiện cầu đơn giản
    st.subheader("🧠 Phát Hiện Cầu")
    from collections import Counter

    def detect_patterns(data):
        patterns = []
        i = 0
        while i < len(data):
            current = data[i]
            length = 1
            while i + length < len(data) and data[i + length] == current:
                length += 1
            if length >= 3:
                patterns.append((current, length, i+1))
            i += length
        return patterns

    patterns = detect_patterns(results)
    if patterns:
        for p in patterns:
            st.markdown(f"✅ Cầu Bệt: {p[0]} xuất hiện liên tiếp {p[1]} lần (từ ván {p[2]})")
    else:
        st.markdown("⚠️ Không phát hiện cầu bệt rõ ràng.")

    # Confidence Engine: nếu P hoặc B chiếm > 65% => cảnh báo lệch tâm lý
    if max(p_count, b_count) / total >= 0.65:
        dominant = "Player" if p_count > b_count else "Banker"
        st.warning(f"⚠️ Cảnh báo tâm lý nghiêng lệch: {dominant} chiếm hơn 65% tổng số ván.")
    
    st.success("🔁 Đã phân tích xong! Nhập dữ liệu mới để tiếp tục.")

else:
    st.info("Hãy nhập lịch sử bàn chơi ở khung trên để bắt đầu phân tích.")
