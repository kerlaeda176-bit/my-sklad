import streamlit as st
import json
import os

st.set_page_config(page_title="Склад Металла", page_icon="🏭", layout="centered")

# Отключаем всплывающую клавиатуру для списков на мобильных устройствах через скрытие поиска
st.markdown(
    """
    <style>
    div[data-baseweb="select"] input {
        inputmode: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏭 Мобильный Склад")
st.write("Учет остатков в рулонах, листах и квадратных метрах")

DB_FILE = "sklad_data.json"

START_DATA = {
    "RAL 7024 (Серый графит) Глянцевый": {"м2": 150.28, "тип": "рулон", "базовая_длина": 10},
    "RAL 8017 (Шоколад) Глянцевый": {"м2": 49.53, "тип": "рулон", "базовая_длина": 12},
    "RAL 9003 (Сигнально-белый) Глянцевый": {"м2": 7.17, "тип": "рулон", "базовая_длина": 12},
    "RR32 (Темно-бурый) Глянцевый": {"м2": 29.57, "тип": "рулон", "базовая_длина": 12},
    "Оцинкованная сталь (Цинк)": {"м2": 47.98, "тип": "рулон", "базовая_длина": 10},
    "RAL 8017 (Шоколад) Матовый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
    "RAL 6005 (Зеленый мох) Глянцевый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
    "RAL 7024 (Серый графит) Матовый": {"м2": 12.5, "тип": "рулон", "базовая_длина": 10},
    "RAL 9005 (Глубокий черный) Матовый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
    "RAL 9005 (Глубокий черный) Глянцевый": {"м2": 3.02, "тип": "рулон", "базовая_длина": 12},
    "Нержавеющая сталь (AISI 304)": {"м2": 0.16, "тип": "лист_2х1", "базовая_длина": 2},
    "Нержавеющая сталь (AISI 430)": {"м2": 4.9, "тип": "лист_2х1", "базовая_длина": 2},
    "RAL 8019 (Серо-коричневый) Глянцевый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
    "RAL 3005 (Винно-красный) Глянцевый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
    "RAL 3005 (Винно-красный) Матовый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
    "RR32 (Темно-бурый) Матовый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
    "ЗолДуб Глянцевый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12}
}

def save_to_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return START_DATA
    else:
        save_to_db(START_DATA)
        return START_DATA

sklad_data = load_from_db()

# РАЗДЕЛ 1: ТЕКУЩИЕ ОСТАТКИ С ФИЛЬТРОМ (Клавиатура отключена)
st.header("📊 Остатки в цеху")

color_options = ["🔍 Показать все цвета"] + list(sklad_data.keys())
selected_filter = st.selectbox("🎯 Фильтр по цвету металла:", color_options)

metals_to_show = sklad_data.keys() if selected_filter == "🔍 Показать все цвета" else [selected_filter]

for metal in metals_to_show:
    values = sklad_data[metal]
    st.subheader(f"• {metal}")
    col1, col2 = st.columns(2)
    col1.metric("Площадь, м²", f"{values['м2']:.2f} м²")
    
    if values.get("тип") == "лист_2х1":
        sheets_count = values["м2"] / 2.0
        col2.metric("В листах (2х1м)", f"{sheets_count:.1f} шт")
    else:
        roll_len = values["базовая_длина"]
        roll_area = roll_len * 1.25
        rolls_count = values["м2"] / roll_area
        col2.metric(f"В рулонах (по {roll_len}м)", f"{rolls_count:.1f} шт")
st.write("---")

# РАЗДЕЛ 2: ДОБАВЛЕНИЕ НОВОГО ЦВЕТА (Клавиатура РАЗРЕШЕНА для ввода текста)
st.header("➕ Добавить новый цвет в базу")
with st.form("new_color_form"):
    new_name = st.text_input("Введите название металла/цвета")
    mat_type = st.selectbox("Тип поставляемого материала:", ("Рулон со штрипсом 1.25м", "Штучный лист 2х1 метр"))
    new_len = st.selectbox("Базовая длина рулона, метров (только для рулонов):", (12, 10))
    start_m2 = st.number_input("Начальный остаток на складе, м²", min_value=0.0, step=0.1, value=0.0)
    
    submitted_new = st.form_submit_button("Создать новый материал")
    if submitted_new and new_name:
        if new_name not in sklad_data:
            t_type = "лист_2х1" if mat_type == "Штучный лист 2х1 метр" else "рулон"
            sklad_data[new_name] = {"м2": start_m2, "тип": t_type, "базовая_длина": new_len}
            save_to_db(sklad_data)
            st.success(f"Материал '{new_name}' успешно добавлен в базу склада!")
            st.rerun()
        else:
            st.error("Этот материал уже есть в базе данных!")
st.write("---")

# РАЗДЕЛ 3: ОФОРМЛЕНИЕ ПРИХОДА (Клавиатура отключена)
st.header("📥 Оформить Приход")
with st.form("income_form"):
    chosen_metal = st.selectbox("Выберите металл для прихода", list(sklad_data.keys()))
    is_sheet = sklad_data[chosen_metal].get("тип") == "лист_2х1"
    
    if is_sheet:
        sheets = st.number_input("Количество пришедших ЛИСТОВ (2х1м), шт", min_value=0.0, step=1.0, value=0.0)
    else:
        rolls = st.number_input("Количество рулонов, шт", min_value=0.0, step=1.0, value=0.0)
        length = st.selectbox("Длина пришедших рулонов, метров", (10, 12))
    
    submitted_in = st.form_submit_button("Добавить металл на склад")
    if submitted_in:
        if is_sheet and sheets > 0:
            added_m2 = sheets * 2.0
            sklad_data[chosen_metal]["м2"] += added_m2
            save_to_db(sklad_data)
            st.success(f"Добавлено {added_m2:.2f} м²!")
            st.rerun()
        elif not is_sheet and rolls > 0:
            added_m2 = rolls * length * 1.25
            sklad_data[chosen_metal]["м2"] += added_m2
            save_to_db(sklad_data)
            st.success(f"Добавлено {added_m2:.2f} м²!")
            st.rerun()
st.write("---")

# РАЗДЕЛ 4: РАСХОД ПО РАЗМЕРАМ ЗАГОТОВОК (Клавиатура отключена)
st.header("📤 Списать Расход")
with st.form("outcome_form"):
    chosen_metal_out = st.selectbox("Выберите металл для списания", list(sklad_data.keys()))
    shape_type = st.radio("Форма детали:", ("Прямоугольная", "Трапеция"))
    det_length = st.number_input("Чистая длина детали, мм", min_value=0, step=10, value=1000)
    
    if shape_type == "Прямоугольная":
        det_width = st.number_input("Ширина детали, мм", min_value=0, step=10, value=500, key="width_rect")
        calculated_m2_single = (det_length * det_width) / 1000000.0
    else:
        det_width_1 = st.number_input("Ширина НИЖНЯЯ (Основание 1), мм", min_value=0, step=10, value=600, key="width_trap1")
        det_width_2 = st.number_input("Ширина ВЕРХНЯЯ (Основание 2), мм", min_value=0, step=10, value=300, key="width_trap2")
        calculated_m2_single = (((det_width_1 + det_width_2) / 2.0) * det_length) / 1000000.0
        
    det_count = st.number_input("Количество деталей, шт", min_value=1, step=1, value=1)
    calculated_m2 = calculated_m2_single * det_count
    
    st.info(f"📐 Чистая расчетная площадь партии: {calculated_m2:.2f} м²")
    
    submitted_out = st.form_submit_button("Списать металл со склада")
    if submitted_out:
        if sklad_data[chosen_metal_out]["м2"] >= calculated_m2:
            sklad_data[chosen_metal_out]["м2"] -= calculated_m2
            save_to_db(sklad_data)
            st.success(f"Успешно списано {calculated_m2:.2f} м²!")
            st.rerun()
        else:
            st.error(f"Ошибка! На складе всего {sklad_data[chosen_metal_out]['м2']:.2f} м². Не хватает.")
