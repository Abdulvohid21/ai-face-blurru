st.set_page_config(page_title="AutoBlur AI", page_icon="🔍", layout="centered")

st.title("🕵️ AutoBlur AI: Защита конфиденциальности")
st.markdown("Загрузите фотографию, и наша модель компьютерного зрения автоматически обнаружит лица и анонимизирует их для защиты конфиденциальности.")

# --- Sidebar Configuration ---
st.sidebar.header("⚙️ Настройки")
method = st.sidebar.radio("Метод анонимизации", ("Blur", "Pixelate"))

if method == "Blur":
    strength = st.sidebar.slider("Сила размытия", min_value=5, max_value=99, value=45, step=2)
else:
    strength = st.sidebar.slider("Размер блока пикселизации", min_value=5, max_value=50, value=15)

st.sidebar.markdown("---")
st.sidebar.markdown("**✨ Уникальная функция:**\nПереключайтесь между плавным размытием и ретро-пикселизацией в реальном времени. ИИ автоматически определяет координаты лиц!")

# --- Main Content ---
uploaded_file = st.file_uploader("Выберите файл изображения...", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns(2)
with col1:
    st.subheader("Оригинал")

with col2:
    st.subheader("Анонимизированное изображение")

with st.spinner('Обнаружение лиц и применение ИИ-анонимизации...'):
    pass

st.success(f"✅ Успешно обнаружено и анонимизировано {face_count} лицо(лиц)!")
st.warning("Лица на изображении не обнаружены. Попробуйте другое!")
