import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتنسيق الاحترافي
# ==========================================
st.set_page_config(
    page_title="DRVT Solar R&D Simulator",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الثوابت الفيزيائية لنظرية الحجم الرنيني الديناميكي
# ==========================================
V_EQ = 286.398          # حجم الاتزان الرنيني (nm^3)
LAMBDA_R = 91.127       # الطول الموجي المرجعي (nm)
LAMBDA_B = 32550.0      # حد أفق بوهر (nm) = 32.55 ميكرومتر
INVARIANT_E_R2 = 13.606 # ثابت كثافة الطاقة الرنينية (eV/nm^2)
K_SURFACE = 13.0 / 3.0  # معامل كثافة الطاقة السطحية (eV/nm^2)

MATERIALS = {
    "السيليكون البلوري (c-Si)": {"Eg": 1.12, "std_thickness": 180.0, "cost_per_kw": 110.0, "std_eff": 21.5},
    "البيروفسكايت القياسي (Perovskite)": {"Eg": 1.55, "std_thickness": 0.6, "cost_per_kw": 75.0, "std_eff": 23.0},
    "البيروفسكايت واسع الفجوة (Wide-Bandgap)": {"Eg": 2.25, "std_thickness": 0.45, "cost_per_kw": 85.0, "std_eff": 19.5},
    "النقاط الكمومية (CdSe Quantum Dots)": {"Eg": 2.00, "std_thickness": 0.35, "cost_per_kw": 95.0, "std_eff": 18.0},
    "خلية ترادفية (Perovskite / Silicon Tandem)": {"Eg": 1.75, "std_thickness": 140.0, "cost_per_kw": 130.0, "std_eff": 28.5}
}

# ==========================================
# 3. الدوال الحسابية للنظرية والمحاكاة الصناعية
# ==========================================
def calculate_drvt_metrics(wavelength_nm):
    r_res = np.sqrt(V_EQ / (np.pi * wavelength_nm))
    a_eff = np.pi * (r_res ** 2)
    e_photon = INVARIANT_E_R2 * (r_res ** 2)
    
    if wavelength_nm < 0.002426:
        regime = "Pre-Resonant Domain (نطاق ما قبل الرنين)"
    elif wavelength_nm < LAMBDA_R:
        regime = "Above-Reference Resonance (فوق المرجعي)"
    elif np.isclose(wavelength_nm, LAMBDA_R, atol=0.5):
        regime = "Reference Resonance (الرنين المرجعي)"
    elif wavelength_nm < LAMBDA_B:
        regime = "Below-Reference Resonance (دون المرجعي - الطيف الشمسي)"
    else:
        regime = "Post-Atomic Resonance (ما بعد الذري - فونونات/حرارة)"
        
    return r_res, a_eff, e_photon, regime

# ==========================================
# 4. القائمة الجانبية (مدخلات المصنع والمهندس)
# ==========================================
with st.sidebar:
    st.title("⚙️ إعدادات التصميم والمصنع")
    
    selected_mat_name = st.selectbox("اختر مادة الخلية الشمسية:", list(MATERIALS.keys()))
    mat = MATERIALS[selected_mat_name]
    
    wavelength = st.slider("الطول الموجي المستهدف λ (نانومتر):", min_value=300, max_value=1200, value=550, step=10)
    
    st.markdown("---")
    st.subheader("🏭 معايير خط الإنتاج (B2B)")
    production_mw = st.number_input("الطاقة الإنتاجية السنوية للمصنع (MW/year):", min_value=10, max_value=5000, value=500, step=50)
    solar_irradiance = st.slider("شدة الإشعاع الشمسي القياسية (W/m²):", min_value=200, max_value=1200, value=1000, step=50)
    fill_factor = st.slider("معامل الملء (Fill Factor):", min_value=0.65, max_value=0.90, value=0.82, step=0.01)
    cell_area = st.number_input("مساحة اللوح القياسي (m²):", min_value=0.5, max_value=5.0, value=2.0, step=0.1)

# ==========================================
# 5. تنفيذ الحسابات
# ==========================================
r_res, a_eff, e_photon, regime = calculate_drvt_metrics(wavelength)
eg = mat["Eg"]

if e_photon >= eg:
    spectral_utilization = eg / e_photon
    thermal_loss_pct = (1.0 - spectral_utilization) * 100.0
    resonant_boost_factor = 1.0 + (0.14 * (a_eff / 1.0)) * (fill_factor / 0.80)
    max_cap = 43.0 if "Tandem" in selected_mat_name else 33.7
    resonant_eff = min(mat["std_eff"] * resonant_boost_factor, max_cap)
else:
    spectral_utilization = 0.0
    thermal_loss_pct = 100.0
    resonant_eff = 0.0

p_out_std = solar_irradiance * cell_area * (mat["std_eff"] / 100.0)
p_out_res = solar_irradiance * cell_area * (resonant_eff / 100.0)

thickness_reduction_pct = min(18.0 + (a_eff * 12.0), 38.0) if resonant_eff > 0 else 0.0
optimized_thickness = mat["std_thickness"] * (1.0 - thickness_reduction_pct / 100.0)

annual_kw = production_mw * 1000.0
material_savings_usd = annual_kw * mat["cost_per_kw"] * (thickness_reduction_pct / 100.0) * 0.45
efficiency_premium_usd = annual_kw * ((resonant_eff - mat["std_eff"]) / max(mat["std_eff"], 1.0)) * 180.0
total_annual_benefit_usd = max(0.0, material_savings_usd + efficiency_premium_usd)

# ==========================================
# 6. واجهة العرض الرئيسية (Dashboard)
# ==========================================
st.markdown('<div class="main-header">☀️ منصة تصميم الخلايا الشمسية بنظرية الحجم الرنيني الديناميكي (DRVT)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">أداة هندسية واقتصادية لتحسين امتصاص الطيف الشمسي، خفض استهلاك المواد الخام، وتعظيم عائد خطوط الإنتاج</div>', unsafe_allow_html=True)

st.subheader("1️⃣ المخرجات الفيزيائية للرنين (DRVT Core Parameters)")
c1, c2, c3, c4 = st.columns(4)
c1.metric("نصف القطر الرنيني (r_res)", f"{r_res:.4f} nm")
c2.metric("المساحة الفعالة (A_eff)", f"{a_eff:.4f} nm²")
c3.metric("طاقة الفوتون الرنينية (E)", f"{e_photon:.3f} eV", f"فجوة المادة: {eg} eV")
c4.metric("الفقد الحراري الطيفي", f"{thermal_loss_pct:.1f} %", delta="-تحسين حراري" if thermal_loss_pct < 45 else "فقد مرتفع", delta_color="inverse")

st.info(f"**تصنيف النطاق الطيفي:** {regime} | **حجم الاتزان الرنيني المرجعي:** Veq = 286.398 nm³")

st.markdown("---")

st.subheader("2️⃣ الجدوى الصناعية والاقتصادية للمصنع (Standard vs. DRVT Design)")
m1, m2, m3, m4 = st.columns(4)
m1.metric("كفاءة التحويل (تصميم DRVT)", f"{resonant_eff:.2f} %", f"+{resonant_eff - mat['std_eff']:.2f} % عن التقليدي")
m2.metric("قدرة اللوح الواحد (Output)", f"{p_out_res:.1f} W", f"+{p_out_res - p_out_std:.1f} W")
m3.metric("توفير سُمك المادة الخام", f"{thickness_reduction_pct:.1f} %", f"{optimized_thickness:.2f} µm بدلاً من {mat['std_thickness']} µm")
m4.metric("العائد المالي السنوي الإضافي", f"${total_annual_benefit_usd:,.0f}", f"لخط إنتاج {production_mw} MW")

# ==========================================
# 7. الرسوم البيانية التفاعلية
# ==========================================
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    lambdas = np.linspace(300, 1200, 200)
    r_vals = np.sqrt(V_EQ / (np.pi * lambdas))
    e_vals = INVARIANT_E_R2 * (r_vals ** 2)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=lambdas, y=e_vals, mode='lines', name='طاقة الفوتون الرنينية (eV)', line=dict(color='#2563EB', width=3)))
    fig1.add_hline(y=eg, line_dash="dash", line_color="#DC2626", annotation_text=f"فجوة الطاقة ({eg} eV)")
    fig1.add_vline(x=wavelength, line_dash="dot", line_color="#059669", annotation_text=f"الطول المختار ({wavelength} nm)")
    fig1.update_layout(title="منحنى الطاقة الرنينية مقابل الطول الموجي", xaxis_title="الطول الموجي λ (nm)", yaxis_title="الطاقة (eV)", height=380)
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    categories = ['التصميم التجاري التقليدي', 'التصميم الرنيني (DRVT)']
    fig2 = go.Figure(data=[
        go.Bar(name='كفاءة الخلية (%)', x=categories, y=[mat['std_eff'], resonant_eff], marker_color=['#94A3B8', '#10B981']),
        go.Bar(name='قدرة اللوح (مقسومة على 10 W)', x=categories, y=[p_out_std/10.0, p_out_res/10.0], marker_color=['#CBD5E1', '#3B82F6'])
    ])
    fig2.update_layout(barmode='group', title="مقارنة الأداء الفعلي للوح الشمسي", height=380)
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# 8. توليد وتصدير التقرير التنفيذي (Executive Summary)
# ==========================================
st.markdown("---")
st.subheader("3️⃣ تصدير التقرير الفني والمالي للمستثمرين والمصانع (Executive Summary)")

report_date = datetime.now().strftime("%Y-%m-%d %H:%M")
eff_gain = resonant_eff - mat['std_eff']
power_gain = p_out_res - p_out_std

report_lines = [
    "====================================================================",
    "EXECUTIVE TECHNICAL & FINANCIAL REPORT (DRVT SOLAR OPTIMIZER)",
    "Based on Dynamic Resonant Volume Theory (Dr. Khalid Abdel Fattah)",
    f"Generated on: {report_date}",
    "====================================================================",
    "",
    "1. SELECTED MATERIAL & OPERATING SPECS:",
    f"   - Solar Cell Technology : {selected_mat_name}",
    f"   - Bandgap Energy (Eg)   : {eg} eV",
    f"   - Target Wavelength (λ) : {wavelength} nm",
    f"   - Standard Panel Area   : {cell_area} m2",
    f"   - Solar Irradiance      : {solar_irradiance} W/m2",
    "",
    "2. DRVT QUANTUM & RESONANT PARAMETERS:",
    f"   - Equilibrium Volume (Veq) : {V_EQ} nm3",
    f"   - Resonant Radius (r_res)  : {r_res:.4f} nm",
    f"   - Effective Area (A_eff)   : {a_eff:.4f} nm2",
    f"   - Photon Energy (E)        : {e_photon:.3f} eV",
    f"   - Spectral Thermal Loss    : {thermal_loss_pct:.1f} %",
    f"   - Physical Regime          : {regime}",
    "",
    "3. MANUFACTURING & PERFORMANCE BENCHMARK (STANDARD vs. DRVT):",
    f"   - Conversion Efficiency    : {resonant_eff:.2f}% (vs. {mat['std_eff']}% Standard) -> +{eff_gain:.2f}% Gain",
    f"   - Single Panel Output      : {p_out_res:.1f} W (vs. {p_out_std:.1f} W Standard) -> +{power_gain:.1f} W Gain",
    f"   - Active Layer Thickness   : {optimized_thickness:.2f} um (vs. {mat['std_thickness']} um Standard) -> {thickness_reduction_pct:.1f}% Material Saved",
    "",
    f"4. INDUSTRIAL FINANCIAL IMPACT (LINE CAPACITY: {production_mw} MW/YEAR):",
    f"   - Annual Raw Material Savings : ${material_savings_usd:,.2f} USD",
