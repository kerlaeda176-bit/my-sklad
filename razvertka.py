import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.set_page_config(page_title="Развёртка", layout="centered")
st.title("📐 Мобильный Раскрой: Бабочка + 2 Торца")

# ОСТАВЛЯЕМ ДВА ПОНЯТНЫХ ЦЕХОВЫХ РЕЖИМА БЕЗ ПУТАНИЦЫ
part_type = st.radio("Что размечаем?", ("🦋 Центр — «Бабочка»", "🔺 Торец — Треугольник (нужно 2 шт)"))

# БЛОК ВВОДА РАЗМЕРОВ
c1, c2 = st.columns(2)
A = c1.number_input("Длина основания (А), мм", min_value=0, value=880, step=10)
B = c2.number_input("Ширина основания (В), мм", min_value=0, value=760, step=10)
H = c1.number_input("Высота конька (Н), мм", min_value=0, value=240, step=10)
K = c2.number_input("Длина конька (К), мм", min_value=0, value=120, step=10)

yubka = c1.number_input("Юбка, мм", min_value=0, value=40, step=5)
kapel = c2.number_input("Капельник, мм", min_value=0, value=20, step=5)
valc = c1.number_input("Вальцовка, мм", min_value=0, value=10, step=5)
klepki = c2.number_input("Шов клепок, мм", min_value=0, value=38, step=1)

# Математика Пифагора
single_pripusk = yubka + kapel + valc
half_base_trap = (A - K) / 2.0 if A > K else 1.0
h_trap = round(math.sqrt(H**2 + (B / 2.0)**2), 1) if B > 0 else 0
h_tri = round(math.sqrt(H**2 + half_base_trap**2), 1)

# Перевод в сантиметры для рулетки
mark_Y1 = round(single_pripusk / 10.0, 1)
mark_H_side = round(h_trap / 10.0, 1)
mark_H_tri = round(h_tri / 10.0, 1)
mark_K = round(K / 10.0, 1)
mark_B = round(B / 10.0, 1)
mark_klepki = round(klepki / 10.0, 1)

final_L = round(A + 2 * klepki, 1)
final_W = round(2 * h_trap + 2 * single_pripusk, 1)

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
st.success(f"📦 **ОБЩИЙ ОТРЕЗ ОТ РУЛОНА ДЛЯ ВСЕХ ДЕТАЛЕЙ: {round(final_L/10, 1)} см х {round(final_W/10, 1)} см**")
st.info("💡 Отрежьте этот лист. Разметьте Бабочку по схеме ниже, а 2 торцевых треугольника вырежьте из пустых боковых углов!")

if part_type == "🦋 Центр — «Бабочка»":
    ax.add_patch(patches.Rectangle((0, 0), final_L, final_W, linewidth=2, edgecolor='red', facecolor='none', linestyle='--'))
    ax.plot([klepki + half_base_trap, klepki + half_base_trap + K], [final_W/2, final_W/2], color='blue', linewidth=3)
    
    ax.plot([klepki, final_L - klepki], [single_pripusk, single_pripusk], color='black', linewidth=1.5)
    ax.plot([klepki, klepki + half_base_trap], [single_pripusk, final_W/2], color='black', linewidth=1.2)
    ax.plot([final_L - klepki, final_L - klepki - half_base_trap], [single_pripusk, final_W/2], color='black', linewidth=1.2)
    ax.plot([klepki, final_L - klepki], [final_W - single_pripusk, final_W - single_pripusk], color='black', linewidth=1.5)
    ax.plot([klepki, klepki + half_base_trap], [final_W - single_pripusk, final_W/2], color='black', linewidth=1.2)
    ax.plot([final_L - klepki, final_L - klepki - half_base_trap], [final_W - single_pripusk, final_W/2], color='black', linewidth=1.2)
    
    ax.fill([0, klepki, klepki + half_base_trap, half_base_trap], [single_pripusk, single_pripusk, final_W/2, final_W/2], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')
    ax.fill([final_L, final_L - klepki, final_L - klepki - half_base_trap, final_L - half_base_trap], [single_pripusk, single_pripusk, final_W/2, final_W/2], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')
    ax.fill([0, klepki, klepki + half_base_trap, half_base_trap], [final_W - single_pripusk, final_W - single_pripusk, final_W/2, final_W/2], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')
    ax.fill([final_L, final_L - klepki, final_L - klepki - half_base_trap, final_L - half_base_trap], [final_W - single_pripusk, final_W - single_pripusk, final_W/2, final_W/2], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')

    ax.plot([klepki, klepki], [0, single_pripusk], color='green', linewidth=3)
    ax.plot([final_L - klepki, final_L - klepki], [0, single_pripusk], color='green', linewidth=3)
    ax.plot([klepki, klepki], [final_W - single_pripusk, final_W], color='green', linewidth=3)
    ax.plot([final_L - klepki, final_L - klepki], [final_W - single_pripusk, final_W], color='green', linewidth=3)

    half_base_cm = round(half_base_trap / 10.0, 1)
    text_y = final_W - single_pripusk / 2.0
    ax.text(klepki / 2.0, text_y, f"{mark_klepki}", ha='center', va='center', color='green', weight='bold', size=12)
    ax.text(klepki + half_base_trap / 2.0, text_y, f"{half_base_cm}", ha='center', va='center', color='black', weight='bold', size=12)
    ax.text(klepki + half_base_trap + K / 2.0, text_y, f"{mark_K}", ha='center', va='center', color='blue', weight='bold', size=13)
    ax.text(klepki + half_base_trap + K + half_base_trap / 2.0, text_y, f"{half_base_cm}", ha='center', va='center', color='black', weight='bold', size=12)
    ax.text(final_L - klepki / 2.0, text_y, f"{mark_klepki}", ha='center', va='center', color='green', weight='bold', size=12)
    
    text_x = klepki / 2.0
    ax.text(text_x, single_pripusk / 2.0, f"{mark_Y1}", ha='center', va='center', color='green', weight='bold', size=12)
    ax.text(text_x, single_pripusk + h_trap / 2.0, f"{mark_H_side}", ha='center', va='center', color='black', weight='bold', size=12)
    ax.text(text_x, single_pripusk + h_trap + h_trap / 2.0, f"{mark_H_side}", ha='center', va='center', color='black', weight='bold', size=12)
    ax.text(text_x, final_W - single_pripusk / 2.0, f"{mark_Y1}", ha='center', va='center', color='green', weight='bold', size=12)

    ax.text(final_L/2.0, final_W + 25, f"ДЛИНА БАБОЧКИ: {round(final_L/10, 1)} см", ha='center', color='red', weight='bold', size=11)
    ax.text(final_L/2.0, 15, f"ШИРИНА БАБОЧКИ: {round(final_W/10, 1)} см", ha='center', color='red', weight='bold', size=11)
    plt.xlim(-50, final_L + 50)
    plt.ylim(-20, final_W + 60)

else:
    # ИСПРАВЛЕННЫЙ ТОРЦЕВОЙ ТРЕУГОЛЬНИК С БОКОВЫМИ ПРИПУСКАМИ ЮБКИ
    # Габарит заготовки увеличивается на ширину двух боковых ушек клепок (по 38 мм с каждой стороны)
    tri_L = round(B + 2 * klepki, 1)
    tri_W = round(h_tri + single_pripusk, 1)
    
    st.success(f"📋 **ЛИСТ ТРЕУГОЛЬНИКА С УШКАМИ: {round(tri_L/10, 1)} см х {round(tri_W/10, 1)} см**")
    ax.add_patch(patches.Rectangle((0, 0), tri_L, tri_W, linewidth=2, edgecolor='red', facecolor='none', linestyle='--'))
    
    # Сдвигаем чистый треугольник на ширину ушка клепок вправо
    ax.plot([klepki, tri_L - klepki], [single_pripusk, single_pripusk], color='black', linewidth=1.5)
    ax.plot([klepki, tri_L/2.0], [single_pripusk, tri_W], color='black', linewidth=1.5)
    ax.plot([tri_L - klepki, tri_L/2.0], [single_pripusk, tri_W], color='black', linewidth=1.5)
    ax.plot([klepki, tri_L - klepki], [single_pripusk + yubka, single_pripusk + yubka], color='black', linestyle=':', linewidth=1)
    
    # 🌟 Синие боковые ушки шва под заклепки в зоне юбки (справа и слева от 7.0 см)
    ax.fill([0, klepki, klepki, 0], [0, 0, single_pripusk, single_pripusk], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')
    ax.fill([tri_L, tri_L - klepki, tri_L - klepki, tri_L], [0, 0, single_pripusk, single_pripusk], color='#d9e1f2', alpha=0.5, edgecolor='blue', linestyle='--')
    
    # Зеленые линии отреза ушек
    ax.plot([klepki, klepki], [0, single_pripusk], color='green', linewidth=3)
    ax.plot([tri_L - klepki, tri_L - klepki], [0, single_pripusk], color='green', linewidth=3)
    
    # Нанесение размеров
    text_y = tri_W - 20
    ax.text(klepki / 2.0, single_pripusk / 2.0, f"{mark_klepki}", ha='center', va='center', color='blue', weight='bold', size=11)
    ax.text(tri_L / 2.0, single_pripusk - 20, f"{round(mark_B/2, 1)}", ha='center', color='black', weight='bold', size=12)
    ax.text(tri_L / 2.0, single_pripusk + h_tri / 2.0, f"{mark_H_tri}", ha='center', color='black', weight='bold', size=12)
    ax.text(tri_L / 2.0, single_pripusk / 2.0, f"{mark_Y1}", ha='center', color='green', weight='bold', size=12)
    ax.text(tri_L - klepki / 2.0, single_pripusk / 2.0, f"{mark_klepki}", ha='center', va='center', color='blue', weight='bold', size=11)
    
    ax.text(tri_L/2.0, tri_W + 20, f"ШИРИНА ЗАГОТОВКИ: {round(tri_L/10, 1)} см", ha='center', color='red', weight='bold', size=11)
    ax.text(tri_L/2.0, 15, f"ВЫСОТА ЗАГОТОВКИ: {round(tri_W/10, 1)} см", ha='center', color='red', weight='bold', size=11)
    plt.xlim(-50, tri_L + 50)
    plt.ylim(-20, tri_W + 60)

plt.axis('off')
st.pyplot(fig)
