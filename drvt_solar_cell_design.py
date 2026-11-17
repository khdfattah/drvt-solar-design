import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="DRVT Solar Simulator", page_icon="☀️", layout="wide")

V_EQ = 286.398
LAMBDA_R = 91.127
LAMBDA_B = 32550.0
INV_E = 13.606

MATERIALS = {
    "السيليكون البلوري (c-Si)": {"Eg": 1.12, "thick": 180.0, "cost": 110.0, "eff": 21.5},
    "البيروفسكايت القياسي (Perovskite)": {"Eg": 1.55, "thick": 0.6, "cost": 75.0, "eff": 23.0},
    "البيروفسكايت واسع الفجوة": {"Eg": 2.25, "thick": 0.45, "cost": 85.0, "eff": 19.5},
    "النقاط الكمومية (CdSe QD)": {"Eg": 2.00, "thick": 0.35, "cost": 95.0, "eff": 18.0},
    "خلية ترادفية (Tandem)": {"Eg": 1.75, "thick": 140.0, "cost": 130.0, "eff": 28.5}
}

with st.sidebar:
    st.title("⚙️ إعدادات المصنع")
    mat_name = st.selectbox("المادة:", list(MATERIALS.keys()))
    mat = MATERIALS[mat_name]
    wl = st.slider("الطول الموجي λ (nm):", 300, 1200, 550, 10)
    prod_mw = st.number_input("إنتاج المصنع السنوي (MW):", 10, 5000, 500, 50)
    irr = st.slider("الإشعاع الشمسي (W/m²):", 200, 1200, 1000, 50)
    ff = st.slider("معامل الملء (FF):", 0.65, 0.90, 0.82, 0.01)
    area = st.number_input("مساحة اللوح (m²):", 0.5, 5.0, 2.0, 0.1)

r_res = np.sqrt(V_EQ / (np.pi * wl))
a_eff = np.pi * (r_res ** 2)
e_ph = INV_E * (r_res ** 2)
eg = mat["Eg"]

if e_ph >= eg:
    th_loss = (1.0 - (eg / e_ph)) * 100.0
    boost = 1.0 + (0.14 * a_eff * (ff / 0.80))
    cap = 43.0 if "Tandem" in mat_name else 33.7
    res_eff = min(mat["eff"] * boost, cap)
else:
    th_loss = 100.0
    res_eff = 0.0

p_std = irr * area * (mat["eff"] / 100.0)
p_res = irr * area * (res_eff / 100.0)
save_pct = min(18.0 + (a_eff * 12.0), 38.0) if res_eff > 0 else 0.0
opt_thick = mat["thick"] * (1.0 - save_pct / 100.0)

kw = prod_mw * 1000.0
mat_usd = kw * mat["cost"] * (save_pct / 100.0) * 0.45
eff_usd = kw * ((res_eff - mat["eff"]) / max(mat["eff"], 1.0)) * 180.0
tot_usd = max(0.0, mat_usd + eff_usd)

st.title("☀️ منصة تصميم الخلايا الشمسية - نظرية الحجم الرنيني الديناميكي (DRVT)")
st.caption("د. خالد عبد الفتاح | أداة محاكاة هندسية واقتصادية للمصنعين والمستثمرين")

c1, c2, c3, c4 = st.columns(4)
c1.metric("نصف القطر الرنيني (r_res)", f"{r_res:.4f} nm")
c2.metric("المساحة الفعالة (A_eff)", f"{a_eff:.4f} nm²")
c3.metric("طاقة الفوتون (E)", f"{e_ph:.3f} eV", f"فجوة المادة: {eg} eV")
c4.metric("الفقد الحراري", f"{th_loss:.1f} %")

st.divider()

m1, m2, m3, m4 = st.columns(4)
m1.metric("كفاءة DRVT", f"{res_eff:.2f} %", f"+{res_eff - mat['eff']:.2f} %")
m2.metric("قدرة اللوح", f"{p_res:.1f} W", f"+{p_res - p_std:.1f} W")
m3.metric("توفير السُمك", f"{save_pct:.1f} %", f"{opt_thick:.2f} µm")
m4.metric("العائد السنوي الإضافي", f"${tot_usd:,.0f}")

g1, g2 = st.columns(2)
with g1:
    ls = np.linspace(300, 1200, 150)
    es = INV_E * (V_EQ / (np.pi * ls))
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=ls, y=es, name="طاقة الفوتون (eV)"))
    fig1.add_hline(y=eg, line_dash="dash", line_color="red")
    fig1.add_vline(x=wl, line_dash="dot", line_color="green")
    fig1.update_layout(title="الطاقة الرنينية مقابل الطول الموجي", height=350)
    st.plotly_chart(fig1, use_container_width=True)

with g2:
    fig2 = go.Figure(data=[
        go.Bar(name="تقليدي", x=["الكفاءة %", "القدرة (x10 W)"], y=[mat["eff"], p_std/10]),
        go.Bar(name="DRVT", x=["الكفاءة %", "القدرة (x10 W)"], y=[res_eff, p_res/10])
    ])
    fig2.update_layout(barmode="group", title="مقارنة الأداء", height=350)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("📄 تصدير التقرير التنفيذي (Executive Summary)")

report = (
    f"DRVT SOLAR EXECUTIVE REPORT ({datetime.now().strftime('%Y-%m-%d')})\n"
    f"Material: {mat_name} | Eg: {eg} eV | Wavelength: {wl} nm\n"
    f"r_res: {r_res:.4f} nm | A_eff: {a_eff:.4f} nm2 | Photon Energy: {e_ph:.3f} eV\n"
    f"Efficiency: {res_eff:.2f}% (vs {mat['eff']}% Std) | Panel Output: {p_res:.1f} W\n"
    f"Material Saved: {save_pct:.1f}% ({opt_thick:.2f} um vs {mat['thick']} um)\n"
    f"Estimated Annual Gain ({prod_mw} MW/yr): ${tot_usd:,.2f} USD"
)

st.text_area("ملخص التقرير:", report, height=160)
st.download_button("📥 تحميل التقرير (TXT)", data=report, file_name="DRVT_Report.txt")
