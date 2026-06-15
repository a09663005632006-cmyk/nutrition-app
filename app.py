import streamlit as st

st.set_page_config(page_title="智慧營養系統 v4", layout="centered")

st.title("🥗 智慧營養食譜系統 v4")

# ===== 使用者設定 =====
st.sidebar.header("使用者設定")

weight = st.sidebar.number_input("體重 (kg)", value=60)

goal = st.sidebar.selectbox("目標", ["減脂", "增肌"])

# ===== 食材資料（每100g）=====
foods = {
    "雞胸肉": {"protein": 31, "kcal": 165, "fat": 3.6, "carb": 0},
    "白飯": {"protein": 2.7, "kcal": 130, "fat": 0.3, "carb": 28},
    "花椰菜": {"protein": 2.8, "kcal": 34, "fat": 0.4, "carb": 7}
}

st.header("食材輸入 (g)")

chicken = st.number_input("雞胸肉", value=100)
rice = st.number_input("白飯", value=150)
broccoli = st.number_input("花椰菜", value=100)

# ===== 營養計算 =====
def calc(chicken, rice, broccoli):
    protein = (
        chicken * foods["雞胸肉"]["protein"] +
        rice * foods["白飯"]["protein"] +
        broccoli * foods["花椰菜"]["protein"]
    ) / 100

    kcal = (
        chicken * foods["雞胸肉"]["kcal"] +
        rice * foods["白飯"]["kcal"] +
        broccoli * foods["花椰菜"]["kcal"]
    ) / 100

    fat = (
        chicken * foods["雞胸肉"]["fat"] +
        rice * foods["白飯"]["fat"] +
        broccoli * foods["花椰菜"]["fat"]
    ) / 100

    carb = (
        chicken * foods["雞胸肉"]["carb"] +
        rice * foods["白飯"]["carb"] +
        broccoli * foods["花椰菜"]["carb"]
    ) / 100

    return protein, kcal, fat, carb

protein, kcal, fat, carb = calc(chicken, rice, broccoli)

st.subheader("📊 目前營養")
st.write(f"蛋白質：{protein:.1f} g")
st.write(f"熱量：{kcal:.0f} kcal")
st.write(f"脂肪：{fat:.1f} g")
st.write(f"碳水：{carb:.1f} g")

# ===== 目標 =====
if goal == "減脂":
    target_protein = weight * 2.0
    target_kcal = weight * 30
else:
    target_protein = weight * 2.2
    target_kcal = weight * 35

st.subheader("🎯 目標")

st.write(f"蛋白質目標：{target_protein:.1f} g")
st.write(f"熱量目標：{target_kcal:.0f} kcal")

# ===== AI規則推薦 =====
st.subheader("🧠 AI營養建議")

if protein < target_protein:
    st.warning("蛋白質不足 → 建議增加雞胸肉 / 雞蛋 / 豆腐")

if fat < 30:
    st.warning("脂肪偏低 → 建議增加堅果 / 酪梨 / 橄欖油")

if carb < 100:
    st.warning("碳水偏低 → 建議增加白飯 / 地瓜")

# ===== 自動縮放 =====
if st.button("🔥 自動最佳化食譜"):

    scale = target_protein / protein

    new_chicken = chicken * scale
    new_rice = rice * scale
    new_broccoli = broccoli * scale

    new_protein, new_kcal, new_fat, new_carb = calc(
        new_chicken, new_rice, new_broccoli
    )

    st.subheader("✨ 最佳化結果")

    st.write(f"雞胸肉：{new_chicken:.0f} g")
    st.write(f"白飯：{new_rice:.0f} g")
    st.write(f"花椰菜：{new_broccoli:.0f} g")

    st.write("---")
    st.write(f"蛋白質：{new_protein:.1f} g")
    st.write(f"熱量：{new_kcal:.0f} kcal")
    st.write(f"脂肪：{new_fat:.1f} g")
    st.write(f"碳水：{new_carb:.1f} g")

    st.success("完成最佳化 🎉")