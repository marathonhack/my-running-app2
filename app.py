import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from PIL import Image
import os

st.set_page_config(page_title="Running Form Report", layout="centered")

st.title("🏃 Running Form PDF Report Generator")

# --- CSVアップロード ---
csv_file = st.file_uploader("📂 アップロードされた関節角度のCSVファイルを選んでください", type="csv")
if csv_file is not None:
    df = pd.read_csv(csv_file)
    st.success("✅ CSVファイルを読み込みました！")
    st.dataframe(df)

    # --- ChatGPT風のコメント ---
    avg_angle = df["knee_angle"].mean()
    if avg_angle < 160:
        comment = "Your knee angle seems slightly tight — consider focusing on flexibility."
    else:
        comment = "Your knee extension is good. Keep it up!"

    st.write("🧠 診断コメント:")
    st.info(comment)

    # --- グラフ生成 ---
    fig, ax = plt.subplots()
    ax.plot(df["frame"], df["knee_angle"], label="Knee Angle")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Angle (deg)")
    ax.set_title("Knee Angle over Time")
    ax.legend()
    graph_path = "knee_angle_plot.png"
    plt.savefig(graph_path)
    st.pyplot(fig)

    # --- PDF生成 ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Running Form Report", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"Average Knee Angle: {avg_angle:.2f} degrees\n\nComment:\n{comment}")
    pdf.image(graph_path, x=10, y=60, w=180)

    pdf_path = "report.pdf"
    pdf.output(pdf_path)
    st.success("📄 PDFレポートを生成しました")

    with open(pdf_path, "rb") as f:
        st.download_button(label="⬇️ レポートをダウンロード", data=f, file_name="running_report.pdf", mime="application/pdf")

# --- 画像アップロード（任意） ---
st.subheader("📷 フォーム画像の表示（オプション）")
img_file = st.file_uploader("フォーム画像ファイルを選択（PNGまたはJPEG）", type=["png", "jpg", "jpeg"])
if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Uploaded Form Image", use_column_width=True)
