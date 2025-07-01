import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image

st.set_page_config(page_title="Running Report Lite")

st.title("📄 Running Report (Simple Version)")

# CSV読み込み
csv_file = st.file_uploader("📂 Upload knee angle CSV", type="csv")
if csv_file:
    df = pd.read_csv(csv_file)
    avg_angle = df["knee_angle"].mean()
    st.success("✅ CSV loaded.")
    st.write(f"**Average Knee Angle:** {avg_angle:.2f} degrees")

    comment = "Good form!" if avg_angle > 160 else "Consider improving flexibility."
    st.info(f"💬 Comment: {comment}")

    # PDF作成
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Running Report", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Average Knee Angle: {avg_angle:.2f}\nComment: {comment}")
    pdf_path = "report_simple.pdf"
    pdf.output(pdf_path)

    with open(pdf_path, "rb") as f:
        st.download_button("⬇️ Download PDF", f, "report_simple.pdf", mime="application/pdf")

# 画像表示
img_file = st.file_uploader("🖼️ Optional: Upload image", type=["jpg", "jpeg", "png"])
if img_file:
    img = Image.open(img_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

