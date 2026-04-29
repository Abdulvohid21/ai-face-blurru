import streamlit as st
import cv2
import numpy as np
from PIL import Image

def detect_and_blur_faces(image, method="Размытие", strength=15):
    """
    Detects faces in an image using OpenCV's Haar Cascades and applies
    either a blur or pixelate effect to anonymize them.
    """
    # Convert PIL image to OpenCV format (BGR)
    img_array = np.array(image.convert('RGB'))
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Load the pre-trained face detection model from OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Convert image to grayscale for face detection (makes it faster and more accurate)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) which is the face
        face_roi = img_cv[y:y+h, x:x+w]
        
        if method == "Размытие" or method == "Blur":
            # Apply Gaussian Blur (kernel size must be odd)
            k_size = strength if strength % 2 != 0 else strength + 1
            blurred_face = cv2.GaussianBlur(face_roi, (k_size, k_size), 0)
            img_cv[y:y+h, x:x+w] = blurred_face
            
        elif method == "Пикселизация" or method == "Pixelate":
            # Resize down and then back up to create a pixelated/mosaic effect
            # Ensure strength doesn't exceed width or height
            block_size = max(1, min(w, h, strength))
            temp = cv2.resize(face_roi, (w // block_size, h // block_size), interpolation=cv2.INTER_LINEAR)
            pixelated_face = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
            img_cv[y:y+h, x:x+w] = pixelated_face
            
    # Convert back to RGB for Streamlit rendering
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb), len(faces)

def main():
    st.set_page_config(page_title="AutoBlur AI", page_icon="🔍", layout="centered")
    
    st.title("🕵️ AutoBlur AI: Защитник приватности")
    st.markdown("Загрузите фото, и наша модель компьютерного зрения автоматически обнаружит лица и анонимизирует их для защиты приватности.")
    
    # --- Sidebar Configuration ---
    st.sidebar.header("⚙️ Настройки")
    method = st.sidebar.radio("Метод анонимизации", ("Размытие", "Пикселизация"))
    
    if method == "Размытие":
        strength = st.sidebar.slider("Интенсивность размытия", min_value=5, max_value=99, value=45, step=2)
    else:
        strength = st.sidebar.slider("Размер блока пикселизации", min_value=5, max_value=50, value=15)
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("**✨ Уникальная функция:**\nПереключайтесь между плавным размытием и ретро-пикселизацией на лету. ИИ автоматически обрабатывает координаты лиц!")
    
    # --- Main Content ---
    uploaded_file = st.file_uploader("Выберите файл изображения...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Оригинал")
            st.image(image, use_container_width=True)
            
        with st.spinner('Обнаружение лиц и применение ИИ-анонимизации...'):
            processed_image, face_count = detect_and_blur_faces(image, method=method, strength=strength)
            
        with col2:
            st.subheader("Анонимизированный результат")
            st.image(processed_image, use_container_width=True)
            
        if face_count > 0:
            st.success(f"✅ Успешно обнаружено и анонимизировано лиц: {face_count}!")
            st.snow() # Fun little visual reward
        else:
            st.warning("На этом изображении лица не обнаружены. Попробуйте другое!")
        
if __name__ == '__main__':
    main()
