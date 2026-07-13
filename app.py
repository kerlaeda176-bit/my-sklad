import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.set_page_config(page_title="Склад и Развертка", page_icon="🏭", layout="centered")

# Отключаем всплывающую клавиатуру для списков выбора
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

st.title("🏭 Мобильный Комплекс: Склад и Развертка")

# Создаем две удобные вкладки на экране телефона
tab1, tab2 = st.tabs(["📊 Учет Склада", "📐 Калькулятор Развертки"])

# ==========================================
# ВКЛАДКА 1: ЧИСТЫЙ ОНЛАЙН СКЛАД
# ==========================================
with tab1:
    st.header("📦 Текущие Остатки")
    # (Здесь используется базовая копия склада в памяти, пока вы не привяжете вашу Google Таблицу)
    if 'sklad' not in st.session_state:
        st.session_state.sklad = {
            "RAL 7024 (Серый графит) Глянцевый": {"м2": 150.28, "тип": "рулон", "базовая_длина": 10},
            "RAL 8017 (Шоколад) Глянцевый": {"м2": 49.53, "тип": "рулон", "базовая_длина": 12},
            "RAL 9003 (Сигнально-белый) Глянцевый": {"м2": 7.17, "тип": "рулон", "базовая_длина": 12},
            "Оцинкованная сталь (Цинк)": {"м2": 47.98, "тип": "рулон", "базовая_длина": 10},
            "Нержавеющая сталь (AISI 304)": {"м2": 0.16, "тип": "лист_2х1", "базовая_длина": 2}
        }
    
    color_options = ["🔍 Показать все цвета"] + list(st.session_state.sklad.keys())
    selected_filter = st.selectbox("🎯 Выберите цвет:", color_options)
    metals_to_show = st.session_state.sklad.keys() if selected_filter == "🔍 Показать все цвета" else [selected_filter]
    
    for metal in metals_to_show:
        values = st.session_state.sklad[metal]
        st.subheader(f"• {metal}")
        col1, col2 = st.columns(2)
        col1.metric("Площадь", f"{values['м2']:.2f} м²")
        if "лист" in values.get("тип", ""):
            col2.metric("Листы (2х1м)", f"{values['м2']/2.0:.1f} шт")
        else:
            col2.metric("Рулоны", f"{values['м2']/(values['базовая_длина']*1.25):.1f} шт")

# ==========================================
# ВКЛАДКА 2: ЧУДО-КАЛЬКУЛЯТОР ДЛЯ СМАРТФОНА
# ==========================================
with tab2:
    st.header("📐 Расчет чертежа заготовки")
    
    st.write("<b>⚙️ Размеры купола (в мм):</b>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    A = c1.number_input("Длина основания (А), мм", min_value=0, value=1180, step=10)
    B = c2.number_input("Ширина основания (В), мм", min_value=0, value=780, step=10)
    H = c1.number_input("Высота конька (Н), мм", min_value=0, value=240, step=10)
    K = c2.number_input("Длина конька (К), мм", min_value=0, value=400, step=10)
    
    st.write("<b>🛠️ Припуски (в мм):</b>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    yubka = c3.number_input("Юбка, мм", min_value=0, value=40, step=5)
    kapel = c4.number_input("Капельник, мм", min_value=0, value=20, step=5)
    valc = c3.number_input("Вальцовка, мм", min_value=0, value=10, step=5)
    klepki = c4.number_input("Припуск на клепки, мм", min_value=0, value=38, step=1)
    
    # Математика Пифагора
    single_pripusk = yubka + kapel + valc
    half_base_trap = (A - K) / 2.0 if A > K else 1.0
    h_trap = round(math.sqrt(H**2 + (B / 2.0)**2), 1) if B > 0 else 0
    h_tri = round(math.sqrt(H**2 + half_base_trap**2), 1)
    
    final_L = round(K + 2 * h_tri + 2 * single_pripusk + 2 * klepki, 1)
    final_W = round(2 * h_trap + 2 * single_pripusk, 1)
    
    start_x = single_pripusk + klepki
    start_y = single_pripusk
    
    # Сантиметры для разметки рулеткой
    mark_X1 = round(start_x / 10.0, 1)
    mark_X2 = round(h_tri / 10.0, 1)
    mark_K  = round(K / 10.0, 1)
    mark_Y1 = round(start_y / 10.0, 1)
    mark_H_side = round(h_trap / 10.0, 1)
    
    st.success(f"📋 **ОТРЕЗАТЬ ОТ РУЛОНА: {round(final_L/10, 1)} см  х  {round(final_W/10, 1)} см**")
    
    # Строим график разметки прямо на экране смартфона
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    
    ax.add_patch(patches.Rectangle((0, 0), final_L, final_W, linewidth=2, edgecolor='red', facecolor='none', linestyle='--'))
    ax.add_patch(patches.Rectangle((start_x, start_y), K + 2 * h_tri, 2 * h_trap, linewidth=1.5, edgecolor='black', facecolor='#f9f9f2'))
    ax.add_patch(patches.Rectangle((start_x - yubka, start_y - yubka), K + 2 * h_tri + 2 * yubka, 2 * h_trap + 2 * yubka, linewidth=1, edgecolor='black', facecolor='none', linestyle=':'))
    
    # Конверт гиба
    ax.plot([start_x, start_x + h_tri], [start_y, final_W/2], color='black', linewidth=1.2)
    ax.plot([start_x, start_x + h_tri], [start_y + 2 * h_trap, final_W/2], color='black', linewidth=1.2)
    ax.plot([start_x + h_tri + K, final_L - start_x], [final_W/2, start_y], color='black', linewidth=1.2)
    ax.plot([start_x + h_tri + K, final_L - start_x], [final_W/2, start_y + 2 * h_trap], color='black', linewidth=1.2)
    ax.plot([start_x + h_tri, start_x + h_tri + K], [final_W/2, final_W/2], color='blue', linewidth=3)
    
    # Зеленые резы
    ax.plot([start_x, start_x], [0, start_y], color='green', linewidth=3)
    ax.plot([start_x, start_x], [start_y + 2 * h_trap, final_W], color='green', linewidth=3)
    ax.plot([final_L - start_x, final_L - start_x], [0, start_y], color='green', linewidth=3)
    ax.plot([final_L - start_x, final_L - start_x], [start_y + 2 * h_trap, final_W], color='green', linewidth=3)
    ax.plot([0, start_x], [start_y, start_y], color='green', linewidth=3)
    ax.plot([0, start_x], [start_y + 2 * h_trap, start_y + 2 * h_trap], color='green', linewidth=3)
    ax.plot([final_L - start_x, final_L], [start_y, start_y], color='green', linewidth=3)
    ax.plot([final_L - start_x, final_L], [start_y + 2 * h_trap, start_y + 2 * h_trap], color='green', linewidth=3)
    
    # Наносим числа цепочки размеров
    text_y_pos = final_W - start_y / 2.0
    ax.text(start_x / 2.0, text_y_pos, f"{mark_X1}\nсм", ha='center', va='center', color='green', weight='bold', size=11)
    ax.text(start_x + h_tri / 2.0, text_y_pos, f"{mark_X2}\nсм", ha='center', va='center', color='black', weight='bold', size=11)
    ax.text(start_x + h_tri + K / 2.0, text_y_pos, f"{mark_K}\nсм", ha='center', va='center', color='blue', weight='bold', size=11)
    ax.text(start_x + h_tri + K + h_tri / 2.0, text_y_pos, f"{mark_X2}\nсм", ha='center', va='center', color='black', weight='bold', size=11)
    ax.text(final_L - start_x / 2.0, text_y_pos, f"{mark_X1}\nсм", ha='center', va='center', color='green', weight='bold', size=11)
    
    text_x_pos = start_x / 2.0
    ax.text(text_x_pos, start_y / 2.0, f"{mark_Y1} см", ha='center', va='center', color='green', weight='bold', size=11)
    ax.text(text_x_pos, start_y + h_trap / 2.0, f"{mark_H_side} см", ha='center', va='center', color='black', weight='bold', size=11)
    ax.text(text_x_pos, start_y + h_trap + h_trap / 2.0, f"{mark_H_side} см", ha='center', va='center', color='black', weight='bold', size=11)
    ax.text(text_x_pos, final_W - start_y / 2.0, f"{mark_Y1} см", ha='center', va='center', color='green', weight='bold', size=11)
    
    plt.xlim(-180, final_L + 180)
    plt.ylim(-120, final_W + 120)
    plt.axis('off')
    st.pyplot(fig) # Выводим чертеж на экран телефона
