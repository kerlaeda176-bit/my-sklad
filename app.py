import streamlit as st

st.set_page_config(page_title="Склад Металла", page_icon="🏭", layout="centered")

st.title("🏭 Мобильный Склад")
st.write("Учет остатков в рулонах и квадратных метрах")

# Используем st.session_state, чтобы новые цвета не пропадали при обновлении страницы
if 'sklad' not in st.session_state:
    st.session_state.sklad = {
        "RAL 7024 (Серый графит) Глянцевый": {"м2": 150.28, "базовая_длина": 10},
        "RAL 8017 (Шоколад) Глянцевый": {"м2": 49.53, "базовая_длина": 12},
        "RAL 9003 (Сигнально-белый) Глянцевый": {"м2": 7.17, "базовая_длина": 12},
        "RR32 (Темно-бурый) Глянцевый": {"м2": 29.57, "базовая_длина": 12},
        "Оцинкованная сталь (Цинк)": {"м2": 47.98, "базовая_длина": 10},
        "RAL 8017 (Шоколад) Матовый": {"м2": 0.0, "базовая_длина": 12},
        "RAL 6005 (Зеленый мох) Глянцевый": {"м2": 0.0, "базовая_длина": 12},
        "RAL 7024 (Серый графит) Матовый": {"м2": 12.5, "базовая_длина": 10},
        "RAL 9005 (Глубокий черный) Матовый": {"м2": 0.0, "базовая_длина": 12},
        "RAL 9005 (Глубокий черный) Глянцевый": {"м2": 3.02, "базовая_длина": 12},
        "Нержавеющая сталь (AISI 304)": {"м2": 0.16, "базовая_длина": 12},
        "Нержавеющая сталь (AISI 430)": {"м2": 4.9, "базовая_длина": 12},
        "RAL 8019 (Серо-коричневый) Глянцевый": {"м2": 0.0, "базовая_длина": 12},
        "RAL 3005 (Винно-красный) Глянцевый": {"м2": 0.0, "базовая_длина": 12},
        "RAL 3005 (Винно-красный) Матовый": {"м2": 0.0, "базовая_длина": 12},
        "RR32 (Темно-бурый) Матовый": {"м2": 0.0, "базовая_длина": 12},
        "ЗолДуб Глянцевый": {"м2": 0.0, "базовая_длина": 12}
    }

# ЭКРАН 1: ТЕКУЩИЕ ОСТАТКИ
st.header("📊 Остатки в цеху")
for metal, values in st.session_state.sklad.items():
    st.subheader(f"• {metal}")
    col1, col2 = st.columns(2)
    col1.metric("Площадь, м²", f"{values['м2']:.2f} м²")
    
    roll_len = values["базовая_длина"]
    roll_area = roll_len * 1.25
    rolls_count = values["м2"] / roll_area
    col2.metric(f"В рулонах (по {roll_len}м)", f"{rolls_count:.1f} шт")
st.write("---")

# НОВЫЙ ЭКРАН: ДОБАВЛЕНИЕ НОВОГО ЦВЕТА/МАТЕРИАЛА
st.header("➕ Добавить новый цвет в базу")
with st.form("new_color_form"):
    new_name = st.text_input("Введите название металла/цвета (например: RAL 7016 Матовый)")
    new_len = st.selectbox("Базовая длина рулона для этого цвета, метров", (12, 10))
    start_m2 = st.number_input("Начальный остаток на складе, м²", min_value=0.0, step=0.1, value=0.0)
    
    submitted_new = st.form_submit_button("Создать новый цвет")
    if submitted_new and new_name:
        # Проверяем, нет ли уже такого цвета
        if new_name not in st.session_state.sklad:
            st.session_state.sklad[new_name] = {"м2": start_m2, "базовая_длина": new_len}
            st.success(f"Металл '{new_name}' успешно добавлен в базу склада!")
            st.rerun()
        else:
            st.error("Этот цвет уже есть в базе данных!")
st.write("---")

# ЭКРАН 3: ПРИХОД
st.header("📥 Оформить Приход")
with st.form("income_form"):
    chosen_metal = st.selectbox("Выберите металл для прихода", list(st.session_state.sklad.keys()))
    rolls = st.number_input("Количество рулонов, шт", min_value=0.0, step=1.0, value=0.0)
    length = st.selectbox("Длина пришедших рулонов, метров", (10, 12))
    
    submitted_in = st.form_submit_button("Добавить металл на склад")
    if submitted_in and rolls > 0:
        added_m2 = rolls * length * 1.25
        st.session_state.sklad[chosen_metal]["м2"] += added_m2
        st.success(f"Добавлено {added_m2:.2f} м² ({rolls} рул. по {length}м)!")
        st.rerun()

# ЭКРАН 4: РАСХОД ПО РАЗМЕРАМ ДЕТАЛЕЙ
st.header("📤 Списать Расход")
with st.form("outcome_form"):
    chosen_metal_out = st.selectbox("Выберите металл для списания", list(st.session_state.sklad.keys()))
    
    det_length = st.number_input("Длина детали, мм", min_value=0, step=10, value=1000)
    det_width = st.number_input("Ширина детали, мм", min_value=0, step=10, value=500)
    det_count = st.number_input("Количество деталей, шт", min_value=1, step=1, value=1)
    
    calculated_m2 = (det_length * det_width / 1000000.0) * det_count
    st.info(f"📐 Расчетная площадь: {calculated_m2:.2f} м²")
    
    submitted_out = st.form_submit_button("Списать металл со склада")
    if submitted_out:
        if st.session_state.sklad[chosen_metal_out]["м2"] >= calculated_m2:
            st.session_state.sklad[chosen_metal_out]["м2"] -= calculated_m2
            st.success(f"Успешно списано {calculated_m2:.2f} м² ({det_count} шт. {det_length}x{det_width}мм)!")
            st.rerun()
        else:
            st.error(f"Ошибка! На складе всего {st.session_state.sklad[chosen_metal_out]['м2']:.2f} м². Не хватает для списания.")
