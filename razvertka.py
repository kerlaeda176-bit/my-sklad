import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.set_page_config(page_title="Калькулятор Развертки", page_icon="📐", layout="centered")

st.title("📐 Мобильный Калькулятор Разверток")
st.write("Готовая карта раскроя со всеми числами для рулетки")

# БЛОК 1: Ввод размеров купола
st.write("<b>⚙️ Размеры купола (в мм):</b>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
A = c1.number_input("Длина основания (А), мм", min_value=0, value=880, step=10)
B = c2.number_input("Ширина основания (В), мм", min_value=0, value=760, step=10)
H = c1.number_input("Высота конька (Н), мм", min_value=0, value=240, step=10)
K = c2.number_input("Длина конька (К), мм", min_value=0, value=120, step=10)

# БЛОК 2: Ввод припусков
st.write("<b>🛠️ Технологические припуски (в мм):</b>", unsafe_allow_html=True)
c3, c4 = st.columns(2)
yubka = c3.number_input("Юбка, мм", min_value=0, value=40, step=5)
kapel = c4.number_input("Капельник, мм", min_value=0, value=20, step=5)
valc = c3.number_input("Вальцовка, мм", min_value=0, value=10, step=5)
klepki = c4.number_input("Припуск на клепки, мм", min_value=0, value=38, step=1)

# Математический расчет по Пифагору
single_pripusk = yubka + kapel + valc
half_base_trap = (A - K) / 2.0 if A > K else 1.0

h_trap = round(math.sqrt(H**2 + (B / 2.0)**2), 1) if B > 0 else 0
h_tri = round(math.sqrt(H**2 + half_base_trap**2), 1)

# Финальный размер отреза от рулона
final_L = round(K + 2 * h_tri + 2 * single_pripusk + 2 * klepki, 1)
final_W = round(2 * h_trap + 2 * single_pripusk, 1)

start_x = single_pripusk + klepki
start_y = single_pripusk

# Контрольные сантиметры для разметки рулеткой
mark_X1 = round(start_x / 10.0, 1)
mark_X2 = round(h_tri / 10.0, 1)
mark_K  = round(K / 10.0, 1)
mark_Y1 = round(start_y / 10.0, 1)
mark_H_side = round(h_trap / 10.0, 1)

# Вывод главного результата крупными буквами
st.success(f"📋 **ОТРЕЗАТЬ ОТ РУЛОНА: {round(final_L/10, 1)} см  х  {round(final_W/10, 1)} см**")

# Отрисовка чертежа
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')

# Красный пунктир отреза
ax.add_patch(patches.Rectangle((0, 0), final_L, final_W, linewidth=2, edgecolor='red', facecolor='none', linestyle='--'))
# Тело купола
ax.add_patch(patches.Rectangle((start_x, start_y), K + 2 * h_tri, 2 * h_trap, linewidth=1.5, edgecolor='black', facecolor='#f9f9f2'))
# Линия гиба юбки
ax.add_patch(patches.Rectangle((start_x - yubka, start_y - yubka), K + 2 * h_tri + 2 * yubka, 2 * h_trap + 2 * yubka, linewidth=1, edgecolor='black', facecolor='none', linestyle=':'))

# Конверт граней
ax.plot([start_x, start_x + h_tri], [start_y, final_W/2], color='black', linewidth=1.2)
ax.plot([start_x, start_x + h_tri], [start_y + 2 * h_trap, final_W/2], color='black', linewidth=1.2)
ax.plot([start_x + h_tri + K, final_L - start_x], [final_W/2, start_y], color='black', linewidth=1.2)
ax.plot([start_x + h_tri + K, final_L - start_x], [final_W/2, start_y + 2 * h_trap], color='black', linewidth=1.2)
ax.plot([start_x + h_tri, start_x + h_tri + K], [final_W/2, final_W/2], color='blue', linewidth=3)

# Зеленые линии разрезов ножницами
ax.plot([start_x, start_x], [0, start_y], color='green', linewidth=3)
ax.plot([start_x, start_x], [start_y + 2 * h_trap, final_W], color='green', linewidth=3)
ax.plot([final_L - start_x, final_L - start_x], [0, start_y], color='green', linewidth=3)
ax.plot([final_L - start_x, final_L - start_x], [start_y + 2 * h_trap, final_W], color='green', linewidth=3)
ax.plot([0, start_x], [start_y, start_y], color='green', linewidth=3)
ax.plot([0, start_x], [start_y + 2 * h_trap, start_y + 2 * h_trap], color='green', linewidth=3)
ax.plot([final_L - start_x, final_L], [start_y, start_y], color='green', linewidth=3)
ax.plot([final_L - start_x, final_L], [start_y + 2 * h_trap, start_y + 2 * h_trap], color='green', linewidth=3)

# Цепочка размеров для рулетки
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
st.pyplot(fig)
