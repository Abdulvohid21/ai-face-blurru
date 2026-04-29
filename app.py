import streamlit as st
import cv2
import numpy as np
from PIL import Image

# ⚠️ FAqat 1 marta va tepada bo‘lishi kerak
st.set_page_config(page_title="AutoBlur AI", page_icon="🔍", layout="centered")


def detect_and_blur_faces(image, method="Размытие", strength=15):
    # Convert PIL image to OpenCV format
    img_array = np.array(image.convert('RGB'))
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # Face detection model
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        face_roi = img_cv[y:y+h, x:x+w]

        if method == "Размытие":
            k_size = strength if strength % 2 != 0 else strength + 1
            blurred_face = cv2.GaussianBlur(face_roi, (k_size, k_size), 0)
            img_cv[y:y+h, x:x+w] = blurred_face

        elif method == "Пикселизация":
            block_size = max(1, min(w, h, strength))
            temp = cv2.resize(
                face_roi,
                (w // block_size, h // block_size),
                interpolation=cv2.INTER_LINEAR
            )
            pixelated_face = cv2.resize(
                temp,
                (w, h),
                interpolation=cv2.INTER_NEAREST
            )
            img_cv[y:y+h, x:x+w] = pixelated_face

    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb), len(faces)


def main():
    st.title("🔍 AutoBlur AI: Защитник приватности")
    st.markdown(
        "Загрузите фото, и модель обнаружит лица и скроет их."
    )

    # Sidebar
    st.sidebar.header("⚙️ Настройки")

    method = st.sidebar.radio(
        "Метод анонимизации",
        ("Размытие", "Пикселизация")
    )

    if method == "Размытие":
        strength = st.sidebar.slider(
            "Интенсивность размытия",
            5, 99, 45, step=2
        )
    else:
        strength = st.sidebar.slider(
            "Размер пикселей",
            5, 50, 15
        )

    # Upload
    uploaded_file = st.file_uploader(
        "Выберите изображение",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Оригинал")
            st.image(image, use_container_width=True)

        with st.spinner("Обработка..."):
            processed_image, face_count = detect_and_blur_faces(
                image, method, strength
            )

        with col2:
            st.subheader("Результат")
            st.image(processed_image, use_container_width=True)

        if face_count > 0:
            st.success(f"Обнаружено лиц: {face_count}")
        else:
            st.warning("Лица не найдены")


if __name__ == "__main__":
    main()
