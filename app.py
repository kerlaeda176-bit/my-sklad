import streamlit as st

st.set_page_config(page_title="Склад Металла", page_icon="🏭", layout="centered")

st.title("🏭 Мобильный Склад")
st.write("Учет остатков в рулонах, листах и квадратных метрах")

# База данных склада в памяти смартфона (Обе нержавейки переведены в листы 2х1м)
if 'sklad' not in st.session_state:
    st.session_state.sklad = {
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
        "Нержавеющая сталь (AISI 430)": {"м2": 4.9, "тип": "лист_2х1", "базовая_длина": 2}, # Переведено в листы
        "RAL 8019 (Серо-коричневый) Глянцевый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
        "RAL 3005 (Винно-красный) Глянцевый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
        "RAL 3005 (Винно-красный) Матовый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
        "RR32 (Темно-бурый) Матовый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12},
        "ЗолДуб Глянцевый": {"м2": 0.0, "тип": "рулон", "базовая_длина": 12}
    }

# РАЗДЕЛ 1: ТЕКУЩИЕ ОСТАТКИ С ФИЛЬТРОМ
st.header("📊 Остатки в цеху")

color_options = ["🔍 Показать все цвета"] + list(st.session_state.sklad.keys())
selected_filter = st.selectbox("🎯 Фильтр по цвету металла:", color_options)

metals_to_show = st.session_state.sklad.keys() if selected_filter == "🔍 Показать все цвета" else [selected_filter]

for metal in metals_to_show:
    values = st.session_state.sklad[metal]
    st.subheader(f"• {metal}")
    col1, col2 = st.columns(2)
    col1.metric("Площадь, м²", f"{values['м2']:.2f} м²")
    
    # Автоматическое разделение логики отображения штучных листов и рулонов
    if values.get("тип") == "лист_2х1":
        sheets_count = values["м2"] / 2.0  # 1 лист 2х1м = 2 м²
        col2.metric("В листах (2х1м)", f"{sheets_count:.1f} шт")
    else:
        roll_len = values["базовая_длина"]
        roll_area = roll_len * 1.25
        rolls_count = values["м2"] / roll_area
        col2.metric(f"В рулонах (по {roll_len}м)", f"{rolls_count:.1f} шт")
st.write("---")

# РАЗДЕЛ 2: ДОБАВЛЕНИЕ НОВОГО ЦВЕТА/МАТЕРИАЛА
st.header("➕ Добавить новый цвет в базу")
with st.form("new_color_form"):
    new_name = st.text_input("Введите название металла/цвета")
    mat_type = st.selectbox("Тип поставляемого материала:", ("Рулон со штрипсом 1.25м", "Штучный лист 2х1 метр"))
    new_len = st.selectbox("Базовая длина рулона, метров (только для рулонов):", (12, 10))
    start_m2 = st.number_input("Начальный остаток на складе, м²", min_value=0.0, step=0.1, value=0.0)
    
    submitted_new = st.form_submit_button("Создать новый материал")
    if submitted_new and new_name:
        if new_name not in st.session_state.sklad:
            t_type = "лист_2х1" if mat_type == "Штучный лист 2х1 метр" else "рулон"
            st.session_state.sklad[new_name] = {"м2": start_m2, "тип": t_type, "базовая_длина": new_len}
            st.success(f"Материал '{new_name}' успешно добавлен в базу склада!")
            st.rerun()
        else:
            st.error("Этот материал уже есть в базе данных!")
st.write("---")

# РАЗДЕЛ 3: ОФОРМЛЕНИЕ ПРИХОДА
st.header("📥 Оформить Приход")
with st.form("income_form"):
    chosen_metal = st.selectbox("Выберите металл для прихода", list(st.session_state.sklad.keys()))
    
    # Проверка типа материала для подстройки интерфейса прихода
    is_sheet = st.session_state.sklad[chosen_metal].get("тип") == "лист_2х1"
    
    if is_sheet:
        sheets = st.number_input("Количество пришедших ЛИСТОВ (2х1м), шт", min_value=0.0, step=1.0, value=0.0)
    else:
        rolls = st.number_input("Количество рулонов, шт", min_value=0.0, step=1.0, value=0.0)
        length = st.selectbox("Длина пришедших рулонов, метров", (10, 12))
    
    submitted_in = st.form_submit_button("Добавить металл на склад")
    if submitted_in:
        if is_sheet and sheets > 0:
            added_m2 = sheets * 2.0  # Каждый штучный лист дает 2 кв. метра площади
            st.session_state.sklad[chosen_metal]["м2"] += added_m2
            st.success(f"Добавлено {added_m2:.2f} м² ({sheets:.0f} листов 2х1м)!")
            st.rerun()
        elif not is_sheet and rolls > 0:
            added_m2 = rolls * length * 1.25
            st.session_state.sklad[chosen_metal]["м2"] += added_m2
            st.success(f"Добавлено {added_m2:.2f} м² ({rolls:.0f} рул. по {length}м)!")
            st.rerun()
st.write("---")

# РАЗДЕЛ 4: РАСХОД ПО РАЗМЕРАМ ЗАГОТОВОК
st.header("📤 Списать Расход")
with st.form("outcome_form"):
    chosen_metal_out = st.selectbox("Выберите металл для списания", list(st.session_state.sklad.keys()))
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
        if st.session_state.sklad[chosen_metal_out]["м2"] >= calculated_m2:
            st.session_state.sklad[chosen_metal_out]["м2"] -= calculated_m2
            st.success(f"Успешно списано {calculated_m2:.2f} м²!")
            st.rerun()
        else:
            st.error(f"Ошибка! На складе всего {st.session_state.sklad[chosen_metal_out]['м2']:.2f} м². Не хватает.")
