import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="DRVT Solar Simulator", page_icon="☀️", layout="wide")

V_EQ = 286.398
INV_E = 13.606

LANG = st.sidebar.radio("🌐 Language / اللغة", ["English", "العربية"], horizontal=True)
IS_EN = (LANG == "English")

TXT = {
    "title": "☀️ DRVT Solar Cell Design & Optimization Simulator" if IS_EN else "☀️ منصة تصميم الخلايا الشمسية - نظرية الحجم الرنيني الديناميكي",
    "sub": "By Dr. Khalid Abdelfattah M. Osman| Quantum-Resonant & Economic Decision Tool for PV Manufacturers" if IS_EN else "د. خالد عبد الفتاح محمد عثمان | أداة محاكاة هندسية واقتصادية للمصنعين والمستثمرين",
    "side_hdr": "⚙️ Factory & Design Inputs" if IS_EN else "⚙️ إعدادات التصميم والمصنع",
    "mat_lbl": "Select Solar Cell Material:" if IS_EN else "اختر مادة الخلية الشمسية:",
    "wl_lbl": "Target Wavelength λ (nm):" if IS_EN else "الطول الموجي المستهدف λ (nm):",
    "mw_lbl": "Annual Line Capacity (MW/yr):" if IS_EN else "إنتاج المصنع السنوي (MW):",
    "irr_lbl": "Solar Irradiance (W/m²):" if IS_EN else "شدة الإشعاع الشمسي (W/m²):",
    "ff_lbl": "Fill Factor (FF):" if IS_EN else "معامل الملء (FF):",
    "area_lbl": "Standard Panel Area (m²):" if IS_EN else "مساحة اللوح القياسي (m²):",
    "m_r": "Resonant Radius (r_res)" if IS_EN else "نصف القطر الرنيني (r_res)",
    "m_a": "Effective Area (A_eff)" if IS_EN else "المساحة الفعالة (A_eff)",
    "m_e": "Photon Energy (E)" if IS_EN else "طاقة الفوتون (E)",
    "m_th": "Spectral Thermal Loss" if IS_EN else "الفقد الحراري الطيفي",
    "m_eff": "DRVT Efficiency" if IS_EN else "كفاءة تصميم DRVT",
    "m_pwr": "Single Panel Output" if IS_EN else "قدرة اللوح الواحد",
    "m_sav": "Material Thickness Saved" if IS_EN else "توفير سُمك المادة الخام",
    "m_usd": "Estimated Annual Gain" if IS_EN else "العائد المالي السنوي الإضافي",
    "c1_t": "Resonant Energy vs. Wavelength" if IS_EN else "الطاقة الرنينية مقابل الطول الموجي",
    "c2_t": "Standard vs. DRVT Performance" if IS_EN else "مقارنة الأداء (التقليدي مقابل DRVT)",
    "b_std": "Standard" if IS_EN else "التقليدي",
    "b_x": ["Efficiency (%)", "Power (x10 W)"] if IS_EN else ["الكفاءة (%)", "القدرة (x10 W)"],
    "rep_h": "📄 Executive Summary Report (For Investors & R&D)" if IS_EN else "📄 تصدير التقرير التنفيذي للمستثمرين والمصانع",
    "dl_b": "📥 Download Executive Report (TXT)" if IS_EN else "📥 تحميل التقرير التنفيذي (TXT)"
}

MATERIALS = {
    "Crystalline Silicon (c-Si)" if IS_EN else "السيليكون البلوري (c-Si)": {"Eg": 1.12, "thick": 180.0, "cost": 110.0, "eff": 21.5},
    "Standard Perovskite" if IS_EN else "البيروفسكايت القياسي (Perovskite)": {"Eg": 1.55, "thick": 0.6, "cost": 75.0, "eff": 23.0},
    "Wide-Bandgap Perovskite" if IS_EN else "البيروفسكايت واسع الفجوة": {"Eg": 2.25, "thick": 0.45, "cost": 85.0, "eff": 19.5},
    "Quantum Dots (CdSe QD)" if IS_EN else "النقاط الكمومية (CdSe QD)": {"Eg": 2.00, "thick": 0.35, "cost": 95.0, "eff": 18.0},
    "Perovskite / Silicon Tandem" if IS_EN else "خلية ترادفية (Tandem)": {"Eg": 1.75, "thick": 140.0, "cost": 130.0, "eff": 28.5}
}

with st.sidebar:
    st.title(TXT["side_hdr"])
    mat_name = st.selectbox(TXT["mat_lbl"], list(MATERIALS.keys()))
    mat = MATERIALS[mat_name]
    wl = st.slider(TXT["wl_lbl"], 300, 1200, 550, 10)
    prod_mw = st.number_input(TXT["mw_lbl"], 10, 5000, 500, 50)
    irr = st.slider(TXT["irr_lbl"], 200, 1200, 1000, 50)
    ff = st.slider(TXT["ff_lbl"], 0.65, 0.90, 0.82, 0.01)
    area = st.number_input(TXT["area_lbl"], 0.5, 5.0, 2.0, 0.1)

r_res = np.sqrt(V_EQ / (np.pi * wl))
a_eff = np.pi * (r_res ** 2)
e_ph = INV_E * (r_res ** 2)
eg = mat["Eg"]

if e_ph >= eg:
    th_loss = (1.0 - (eg / e_ph)) * 100.0
    boost = 1.0 + (0.14 * a_eff * (ff / 0.80))
    cap = 43.0 if "Tandem" in mat_name or "ترادفية" in mat_name else 33.7
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

st.title(TXT["title"])
st.caption(TXT["sub"])

c1, c2, c3, c4 = st.columns(4)
c1.metric(TXT["m_r"], f"{r_res:.4f} nm")
c2.metric(TXT["m_a"], f"{a_eff:.4f} nm²")
c3.metric(TXT["m_e"], f"{e_ph:.3f} eV", f"Eg: {eg} eV")
c4.metric(TXT["m_th"], f"{th_loss:.1f} %")

st.divider()

m1, m2, m3, m4 = st.columns(4)
m1.metric(TXT["m_eff"], f"{res_eff:.2f} %", f"+{res_eff - mat['eff']:.2f} %")
m2.metric(TXT["m_pwr"], f"{p_res:.1f} W", f"+{p_res - p_std:.1f} W")
m3.metric(TXT["m_sav"], f"{save_pct:.1f} %", f"{opt_thick:.2f} µm")
m4.metric(TXT["m_usd"], f"${tot_usd:,.0f}")

g1, g2 = st.columns(2)
with g1:
    ls = np.linspace(300, 1200, 150)
    es = INV_E * (V_EQ / (np.pi * ls))
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=ls, y=es, name="E (eV)"))
    fig1.add_hline(y=eg, line_dash="dash", line_color="red")
    fig1.add_vline(x=wl, line_dash="dot", line_color="green")
    fig1.update_layout(title=TXT["c1_t"], height=350)
    st.plotly_chart(fig1, use_container_width=True)

with g2:
    fig2 = go.Figure(data=[
        go.Bar(name=TXT["b_std"], x=TXT["b_x"], y=[mat["eff"], p_std/10]),
        go.Bar(name="DRVT", x=TXT["b_x"], y=[res_eff, p_res/10])
    ])
    fig2.update_layout(barmode="group", title=TXT["c2_t"], height=350)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader(TXT["rep_h"])

report = (
    f"DRVT SOLAR EXECUTIVE REPORT ({datetime.now().strftime('%Y-%m-%d')})\n"
    f"Author: Dr. Khalid Abdel Fattah (Merowe University of Technology)\n"
    f"Material: {mat_name} | Bandgap (Eg): {eg} eV | Wavelength: {wl} nm\n"
    f"r_res: {r_res:.4f} nm | A_eff: {a_eff:.4f} nm2 | Photon Energy: {e_ph:.3f} eV\n"
    f"Efficiency: {res_eff:.2f}% (vs {mat['eff']}% Std) | Panel Output: {p_res:.1f} W\n"
    f"Material Saved: {save_pct:.1f}% ({opt_thick:.2f} um vs {mat['thick']} um)\n"
    f"Estimated Annual Gain ({prod_mw} MW/yr): ${tot_usd:,.2f} USD"
)

st.text_area("", report, height=165)
st.download_button(TXT["dl_b"], data=report, file_name="DRVT_Executive_Report.txt")
