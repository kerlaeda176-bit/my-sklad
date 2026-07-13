import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.set_page_config(page_title="Калькулятор Развертки", page_icon="📐", layout="centered")

st.title("📐 Мобильный Калькулятор Разверток")
st.write("Раскрой колпака на 3 части: «Бабочка» + 2 Торцевых треугольника")

# БЛОК 1: Выбор детали для отображения
st.write("<b>✂️ Выберите деталь для разметки:</b>", unsafe_allow_html=True)
part_type = st.radio("Какую деталь размечаем?", ("🦋 Центр — «Бабочка»", "🔺 Торец — Треугольник (нужно 2 шт)"))

# БЛОК 2: Ввод размеров купола (в мм)
st.write("<b>⚙️ Размеры купола (в мм):</b>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
A = c1.number_input("Длина основания (А), мм", min_value=0, value=880, step=10)
B = c2.number_input("Ширина основания (В), мм", min_value=0, value=760, step=10)
H = c1.number_input("Высота конька (Н), мм", min_value=0, value=240, step=10)
K = c2.number_input("Длина конька (К), мм", min_value=0, value=120, step=10)

# БЛОК 3: Ввод припусков (в мм)
st.write("<b>🛠️ Технологические припуски (в мм):</b>", unsafe_allow_html=True)
c3, c4 = st.columns(2)
yubka = c3.number_input("Юбка, мм", min_value=0, value=40, step=5)
kapel = c4.number_input("Капельник, мм", min_value=0, value=20, step=5)
valc = c3.number_input("Вальцовка, мм", min_value=0, value=10, step=5)
klepki = c4.number_input("Припуск на клепки (шов), мм", min_value=0, value=38, step=1)

# --- МАТЕМАТИЧЕСКИЙ РАСЧЕТ ГЕОМЕТРИИ (Пифагор) ---
single_pripusk = yubka + kapel + valc
half_base_trap = (A - K) / 2.0 if A > K else 1.0

# Высоты скатов (чистые)
h_trap = round(math.sqrt(H**2 + (B / 2.0)**2), 1) if B > 0 else 0
h_tri = round(math.sqrt(H**2 + half_base_trap**2), 1)

# Сантиметры для рулетки
mark_Y1 = round(single_pripusk / 10.0, 1)
mark_H_side = round(h_trap / 10.0, 1)
mark_H_tri = round(h_tri / 10.0, 1)
mark_K = round(K / 10.0, 1)
mark_A = round(A / 10.0, 1)
mark_B = round(B / 10.0, 1)
mark_klepki = round(klepki / 10.0, 1)

# Отрисовка чертежа в зависимости от выбранной детали
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')

if part_type == "🦋 Центр — «Бабочка»":
    # Расчет габаритов заготовки для Бабочки
    # Длина заготовки = Длина основания (А) + 2 припуска под клепки
    final_L = round(A + 2 * klepki, 1)
    # Ширина заготовки = 2 высоты боковых скатов + 2 припуска низа
    final_W = round(2 * h_trap + 2 * single_pripusk, 1)
    
    st.success(f"📋 **РАЗМЕР ЛИСТА ДЛЯ «БАБОЧКИ»: {round(final_L/10, 1)} см х {round(final_W/10, 1)} см**")
    
    # Красный контур заготовки
    ax.add_patch(patches.Rectangle((0, 0), final_L, final_W, linewidth=2, edgecolor='red', facecolor='none', linestyle='--'))
    
    # Линии гиба конька по центру
    ax.plot([klepki + half_base_trap, klepki + half_base_trap + K], [final_W/2, final_W/2], color='blue', linewidth=3, label='Конек')
    
    # Контур двух трапеций (вверх и вниз от конька)
    # Нижняя трапеция
    ax.plot([klepki, final_L - klepki], [single_pripusk, start_y := single_pripusk], color='black', linewidth=1.5)
    ax.plot([klepki, klepki + half_base_trap], [single_pripusk, final_W/2], color='black', linewidth=1.2)
    ax.plot([final_L - klepki, final_L - klepki - half_base_trap], [single_pripusk, final_W/2], color='black', linewidth=1.2)
    # Верхняя трапеция
    ax.plot([klepki, final_L - klepki], [final_W - single_pripusk, final_W - single_pripusk], color='black', linewidth=1.5)
    ax.plot([klepki, klepki + half_base_trap], [final_W - single_pripusk, final_W/2], color='black', linewidth=1.2)
    ax.plot([final_L - klepki, final_L - klepki - half_base_trap], [final_W - single_pripusk, final_W/2], color='black', linewidth=1.2)
    
    # Пунктирные линии юбки
    ax.plot([klepki, final_L - klepki], [single_pripusk + yubka, single_pripusk + yubka], color='black', linestyle=':', linewidth=1)
    ax.plot([klepki, final_L - klepki], [final_W - single_pripusk - yubka, final_W - single_pripusk - yubka], color='black', linestyle=':', linewidth=1)
    
    # Синие линии нахлеста шва под заклепки (боковые ушки)
    ax.fill([0, klepki, klepki + half_base_trap, half_base_trap], [single_pripusk, single_pripusk, final_W/2, final_W/2], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')
    ax.fill([final_L, final_L - klepki, final_L - klepki - half_base_trap, final_L - half_base_trap], [single_pripusk, single_pripusk, final_W/2, final_W/2], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')
    ax.fill([0, klepki, klepki + half_base_trap, half_base_trap], [final_W - single_pripusk, final_W - single_pripusk, final_W/2, final_W/2], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')
    ax.fill([final_L, final_L - klepki, final_L - klepki - half_base_trap, final_L - half_base_trap], [final_W - single_pripusk, final_W - single_pripusk, final_W/2, final_W/2], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')

    # Разрезы ножницами (зеленые линии)
    ax.plot([klepki, klepki], [0, single_pripusk], color='green', linewidth=3)
    ax.plot([final_L - klepki, final_L - klepki], [0, single_pripusk], color='green', linewidth=3)
    ax.plot([klepki, klepki], [final_W - single_pripusk, final_W], color='green', linewidth=3)
    ax.plot([final_L - klepki, final_L - klepki], [final_W - single_pripusk, final_W], color='green', linewidth=3)

    # Нанесение размеров для Бабочки
    t_y = final_W - single_pripusk / 2.0
    ax.text(klepki / 2.0, t_y, f"{mark_klepki}", ha='center', va='center', color='green', weight='bold', size=11)
    ax.text(klepki + half_base_trap / 2.0, t_y, f"{mark_X2}", ha='center', va='center', color='black', weight='bold', size=11)
    ax.text(klepki + half_base_trap + K / 2.0, t_y, f"{mark_K}", ha='center', va='center', color='blue', weight='bold', size=12)
    
    t_x = klepki + 20
    ax.text(t_x, single_pripusk / 2.0, f"{mark_Y1}", ha='center', va='center', color='green', weight='bold', size=11)
    ax.text(t_x, single_pripusk + h_trap / 2.0, f"{mark_H_side}", ha='center', va='center', color='black', weight='bold', size=11)

    ax.text(final_L/2.0, final_W + 35, f"ДЛИНА БАБОЧКИ: {round(final_L/10, 1)} см", ha='center', color='red', weight='bold', size=12)
    ax.text(-35, final_W/2.0, f"ШИРИНА БАБОЧКИ:\n{round(final_W/10, 1)} см", ha='right', va='center', color='red', weight='bold', size=12)
    plt.xlim(-150, final_L + 150)
    plt.ylim(-100, final_W + 120)

else:
    # РАСЧЕТ И ОТРИСОВКА ОТДЕЛЬНОГО ТОРЦЕВОГО ТРЕУГОЛЬНИКА
    # Длина заготовки под треугольник = Ширина основания (В)
    final_L = round(B, 1)
    # Ширина заготовки под треугольник = Высота торцевого ската + 1 припуск низа
    final_W = round(h_tri + single_pripusk, 1)
    
    st.success(f"📋 **РАЗМЕР ЛИСТА ДЛЯ ОДНОГО ТРЕУГОЛЬНИКА: {round(final_L/10, 1)} см х {round(final_W/10, 1)} см**")
    
    # Красный контур заготовки
    ax.add_patch(patches.Rectangle((0, 0), final_L, final_W, linewidth=2, edgecolor='red', facecolor='none', linestyle='--'))
    
    # Прорисовка самого треугольника ската
    ax.plot([0, final_L], [single_pripusk, single_pripusk], color='black', linewidth=1.5)
    ax.plot([0, final_L/2.0], [single_pripusk, final_W], color='black', linewidth=1.5)
    ax.plot([final_L, final_L/2.0], [single_pripusk, final_W], color='black', linewidth=1.5)
    
    # Линия гиба юбки низа
    ax.plot([0, final_L], [single_pripusk + yubka, single_pripusk + yubka], color='black', linestyle=':', linewidth=1)
    
    # Нанесение размеров для треугольника
    ax.text(final_L / 4.0, final_W - 30, f"{round(mark_B/2, 1)}", ha='center', color='black', weight='bold', size=11)
    ax.text(final_L / 2.0, single_pripusk + h_tri / 2.0, f"{mark_H_tri}", ha='center', color='black', weight='bold', size=11)
    ax.text(final_L / 2.0, single_pripusk / 2.0, f"{mark_Y1}", ha='center', color='green', weight='bold', size=11)
    
    ax.text(final_L/2.0, final_W + 35, f"ОСНОВАНИЕ ТРЕУГОЛЬНИКА: {round(final_L/10, 1)} см", ha='center', color='red', weight='bold', size=12)
    ax.text(-35, final_W/2.0, f"ВЫСОТА ЗАГОТОВКИ:\n{round(final_W/10, 1)} см", ha='right', va='center', color='red', weight='bold', size=12)
    plt.xlim(-120, final_L + 120)
    plt.ylim(-100, final_W + 120)

plt.axis('off')
st.pyplot(fig)
