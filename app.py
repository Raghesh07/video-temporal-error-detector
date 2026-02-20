import streamlit as st
import cv2

st.title("Video Temporal Error Detector")
uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.write("Processing for temporal errors...")
    # Call your logic here: result = detector.process(uploaded_file)