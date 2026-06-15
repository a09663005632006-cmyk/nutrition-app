import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 🏷️ 網站設定
# =========================
st.set_page_config(page_title="智慧 AI 營養系統", layout="centered")
st.title("🥗 智慧 AI 營養系統")

# =========================
# 🧠 使用者設定
# =========================
st.sidebar.header("使用者設定")

weight = st.sidebar.number_input("體重 (kg)", 40, 150, 60)
goal = st.sidebar.selectbox("目標", ["減脂", "增肌", "維持"])
mode = st.radio("模式選擇", ["食材模式", "營養素模式"])

# =========================
# 🍱 食材資料庫
# =========================
if "foods" not in st.session_state:
    st.session_state.foods = {
        "雞胸肉": {"protein": 31, "kcal": 165, "fat": 3.6, "carb": 0},
        "白飯": {"protein": 2.7, "kcal": 130, "fat": 0.3, "carb": 28},
        "花椰菜": {"protein": 2.8, "kcal": 34, "fat": 0.4, "carb": 7},
        "雞蛋": {"protein": 13, "kcal": 155, "fat": 11, "carb": 1.1},
        "牛肉": {"protein": 26, "kcal": 250, "fat": 20, "carb": 0},
        "鮭魚": {"protein": 20, "kcal": 208, "fat": 13, "carb": 0},
        "豆腐": {"protein": 8, "kcal": 76, "fat": 4.8, "carb": 2},
        "地瓜": {"protein": 1.6, "kcal": 86, "fat": 0.1, "carb": 20},
        "燕麥": {"protein": 13, "kcal": 389, "fat": 6.9, "carb": 66},
        "香蕉": {"protein": 1.1, "kcal": 89, "fat": 0.3, "carb": 23},
    }

foods = st.session_state.foods

# =========================
# ➕ 新增食材
# =========================
st.sidebar.header("➕ 新增食材")

new_name = st.sidebar.text_input("食材名稱")
new_p = st.sidebar.number_input("蛋白質 (每100g)", 0.0)
new_k = st.sidebar.number_input("熱量 (kcal)", 0.0)
new_f = st.sidebar.number_input("脂肪 (g)", 0.0)
new_c = st.sidebar.number_input("碳水 (g)", 0.0)

if st.sidebar.button("新增食材"):
    if new_name:
        foods[new_name] = {
            "protein": new_p,
            "kcal": new_k,
            "fat": new_f,
            "carb": new_c
        }
        st.sidebar.success(f"已新增：{new_name}")

# =========================
# 🧮 計算
# =========================
def calc(inputs):
    p = k = f = c = 0
    for food, g in inputs.items():
        p += g * foods[food]["protein"]
        k += g * foods[food]["kcal"]
        f += g * foods[food]["fat"]
        c += g * foods[food]["carb"]
    return p/100, k/100, f/100, c/100

def safe_div(a, b):
    return a / b if b else 1

# =========================
# 🎯 目標
# =========================
if goal == "減脂":
    target_p = weight * 2.0
    target_k = weight * 30
elif goal == "增肌":
    target_p = weight * 2.2
    target_k = weight * 35
else:
    target_p = weight * 1.8
    target_k = weight * 32

# =========================
# 🍱 食材模式（0g輸入）
# =========================
if mode == "食材模式":

    st.header("🍱 食材輸入 (g)")
    st.write("👉 沒吃 = 0g")
    st.caption("💡 例：雞胸肉100g / 白飯150g")

    inputs = {}

    for food in foods:
        inputs[food] = st.number_input(
            f"{food} (g)",
            min_value=0,
            max_value=1000,
            value=0,
            step=10
        )

    protein, kcal, fat, carb = calc(inputs)

# =========================
# 🧠 營養素模式
# =========================
else:
    st.header("🧠 營養素輸入")

    protein = st.number_input("蛋白質 (g)", 0.0)
    carb = st.number_input("碳水 (g)", 0.0)
    fat = st.number_input("脂肪 (g)", 0.0)

    kcal = protein * 4 + carb * 4 + fat * 9

# =========================
# 📊 顯示營養
# =========================
st.subheader("📊 目前營養")

col1, col2, col3, col4 = st.columns(4)
col1.metric("蛋白質", f"{protein:.1f} g")
col2.metric("熱量", f"{kcal:.0f} kcal")
col3.metric("脂肪", f"{fat:.1f} g")
col4.metric("碳水", f"{carb:.1f} g")

# =========================
# 📉 AI分析
# =========================
st.subheader("📉 AI分析")

st.write(f"蛋白質差距：{target_p - protein:.1f} g")
st.write(f"熱量差距：{target_k - kcal:.0f} kcal")

# =========================
# 🧠 AI建議
# =========================
st.subheader("🧠 AI建議")

if protein < target_p:
    st.warning("蛋白質不足 → 雞胸肉 / 雞蛋 / 豆腐")

if carb < 100:
    st.warning("碳水不足 → 白飯 / 地瓜 / 燕麥")

if fat < 25:
    st.warning("脂肪不足 → 鮭魚 / 堅果 / 酪梨")

# =========================
# 🔥 AI最佳化
# =========================
if st.button("🔥 AI自動生成最佳飲食方案"):

    scale_p = safe_div(target_p, protein)
    scale_k = safe_div(target_k, kcal)
    scale = (scale_p + scale_k) / 2

    if mode == "食材模式":
        optimized = {k: v * scale for k, v in inputs.items()}
        new_p, new_k, new_f, new_c = calc(optimized)
    else:
        new_p = protein * scale
        new_k = kcal * scale
        new_f = fat * scale
        new_c = carb * scale

    st.subheader("✨ AI最佳化結果")

    st.write(f"蛋白質：{new_p:.1f} g")
    st.write(f"熱量：{new_k:.0f} kcal")
    st.write(f"脂肪：{new_f:.1f} g")
    st.write(f"碳水：{new_c:.1f} g")

    fig, ax = plt.subplots()
    ax.pie([new_p, new_c, new_f],
           labels=["Protein", "Carbs", "Fat"],
           autopct="%1.1f%%")
    st.pyplot(fig)

    st.success("AI生成完成 🎉")

# =========================
# 🍱 食材模板
# =========================
meal_templates = {
    "減脂": {
        "早餐": ["雞蛋", "燕麥", "香蕉"],
        "午餐": ["雞胸肉", "白飯", "花椰菜"],
        "晚餐": ["豆腐", "鮭魚", "花椰菜"]
    },
    "增肌": {
        "早餐": ["雞蛋", "燕麥", "香蕉"],
        "午餐": ["牛肉", "白飯"],
        "晚餐": ["雞胸肉", "鮭魚", "地瓜"]
    },
    "維持": {
        "早餐": ["雞蛋", "香蕉"],
        "午餐": ["雞胸肉", "白飯", "花椰菜"],
        "晚餐": ["豆腐", "鮭魚"]
    }
}

# =========================
# 🍱 智能克數估算（核心升級）
# =========================
def estimate_grams(food_list, target_kcal=600):
    total = sum([foods[f]["kcal"] for f in food_list])
    if total == 0:
        return {f: 100 for f in food_list}
    scale = target_kcal / total
    return {f: round(100 * scale, 1) for f in food_list}

# =========================
# 🍱 AI 一日菜單（升級版）
# =========================
st.subheader("🍱 AI 一日菜單生成（智能克數版）")

if st.button("🤖 生成 AI 智能一日菜單"):

    plan = meal_templates[goal]

    total_p = total_k = total_f = total_c = 0

    for meal, foods_list in plan.items():
        st.markdown(f"## 🍽️ {meal}")

        grams_plan = estimate_grams(foods_list)

        meal_p = meal_k = meal_f = meal_c = 0

        for food, g in grams_plan.items():
            p = g * foods[food]["protein"] / 100
            k = g * foods[food]["kcal"] / 100
            f = g * foods[food]["fat"] / 100
            c = g * foods[food]["carb"] / 100

            meal_p += p
            meal_k += k
            meal_f += f
            meal_c += c

            st.write(f"🥗 {food}：{g} g")

        total_p += meal_p
        total_k += meal_k
        total_f += meal_f
        total_c += meal_c

        st.write(f"➡️ 蛋白質：{meal_p:.1f} g")
        st.write(f"➡️ 熱量：{meal_k:.0f} kcal")
        st.write(f"➡️ 脂肪：{meal_f:.1f} g")
        st.write(f"➡️ 碳水：{meal_c:.1f} g")

    st.markdown("---")
    st.subheader("📊 一日總計")

    st.write(f"總蛋白質：{total_p:.1f} g")
    st.write(f"總熱量：{total_k:.0f} kcal")
    st.write(f"總脂肪：{total_f:.1f} g")
    st.write(f"總碳水：{total_c:.1f} g")

    st.subheader("🎯 與目標比較")

    st.write(f"蛋白質差距：{target_p - total_p:.1f} g")
    st.write(f"熱量差距：{target_k - total_k:.0f} kcal")
