import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image
import os

st.set_page_config(page_title="Running Report (Lite)", layout="centered")

st.title("🏃 Running Form PDF Report Generator")

# --- CSVアップロード ---
csv_file = st.file_uploader("📂 Upload CSV file of knee angles", type="csv")
if csv_file is not None:
    df = pd.read_csv(csv_file)
    st.success("✅ CSV loaded successfully!")
    st.dataframe(df)

    # --- 平均値とコメント ---
    if "knee_angle" in df.columns:
        avg_angle = df["knee_angle"].mean()
        comment = (
            "Your knee extension is good. Keep it up!"
            if avg_angle >= 160
            else "Your knee angle seems slightly tight — consider focusing on flexibility."
        )

        st.write("🧠 Diagnosis Comment:")
        st.info(comment)

        # --- PDF生成 ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Running Form Report", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(
            0,
            10,
            txt=f"Average Knee Angle: {avg_angle:.2f} degrees\n\nComment:\n{comment}",
        )

        pdf_path = "report.pdf"
        pdf.output(pdf_path)
        st.success("📄 PDF report generated!")

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Report PDF",
                data=f,
                file_name="running_report.pdf",
                mime="application/pdf",
            )
    else:
        st.error("❌ 'knee_angle' column not found in the CSV.")

# --- 画像アップロード ---
st.subheader("📷 Optional: Display Uploaded Image")
img_file = st.file_uploader("Upload form image (PNG or JPEG)", type=["png", "jpg", "jpeg"])
if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Uploaded Form Image", use_column_width=True)


