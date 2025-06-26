import streamlit as st
import os
import pandas as pd
from fpdf import FPDF
from PIL import Image

# ディレクトリ作成
UPLOAD_DIR = "uploaded_videos"
CSV_DIR = "uploaded_csvs"
IMAGE_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

st.title("フォーム分析ライト版アプリ")

page = st.sidebar.selectbox("ページ選択", ["動画アップロード", "CSVアップロード＆診断", "画像表示＆PDF出力"])

if page == "動画アップロード":
    st.header("① スマホで撮影した動画をアップロード")
    uploaded_file = st.file_uploader("動画ファイル（mp4, mov）を選択", type=["mp4", "mov"])
    if uploaded_file:
        path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"アップロード完了: {uploaded_file.name}")
        st.video(path)

elif page == "CSVアップロード＆診断":
    st.header("② ローカルで処理した角度データをアップロード")
    uploaded_csv = st.file_uploader("角度CSVファイルをアップロード", type=["csv"])
    if uploaded_csv:
        df = pd.read_csv(uploaded_csv)
        st.dataframe(df)

        st.subheader("ChatGPT風の診断コメント")
        if "左膝角度" in df.columns:
            avg_angle = df["左膝角度"].mean()
            if avg_angle < 150:
                st.info("膝の曲がりがやや浅い傾向があります。もう少し柔軟性を意識しましょう。")
            elif avg_angle > 170:
                st.info("膝が伸びすぎている可能性があります。着地時の衝撃に注意。")
            else:
                st.success("適切な膝角度を保てています！")

elif page == "画像表示＆PDF出力":
    st.header("③ キーフレーム画像表示とレポート出力")
    uploaded_images = st.file_uploader("フォーム画像をアップロード（複数可）", type=["jpg", "png"], accept_multiple_files=True)
    if uploaded_images:
        image_paths = []
        for img_file in uploaded_images:
            path = os.path.join(IMAGE_DIR, img_file.name)
            with open(path, "wb") as f:
                f.write(img_file.getbuffer())
            image_paths.append(path)
            st.image(path, caption=img_file.name, width=300)

        if st.button("PDFレポートを作成"):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            pdf.cell(200, 10, txt="フォーム比較レポート", ln=1)

            for img_path in image_paths:
                pdf.image(img_path, w=180)
            pdf_path = "フォームレポート.pdf"
            pdf.output(pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button("📄 レポートをダウンロード", f, file_name=pdf_path)
