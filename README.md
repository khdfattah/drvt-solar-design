# ☀️ DRVT Solar Cell Design & Optimization Simulator
### منصة تصميم وتحسين الخلايا الشمسية وفق نظرية الحجم الرنيني الديناميكي

[![Streamlit App](https://streamlit.io)](https://streamlit.app)
[![License](https://shields.io)](LICENSE)

---

## 📌 Overview | نظرة عامة

**English:**  
The **DRVT Solar Simulator** is an interactive engineering and economic decision-making platform built upon the **Dynamic Resonant Volume Theory (DRVT)**, formulated by **Dr. Khalid Abdel Fattah** (Merowe University of Technology, Sudan). The tool bridges theoretical quantum-electromagnetic resonance with practical photovoltaic (PV) manufacturing, enabling researchers and solar manufacturers to optimize light absorption, minimize raw material waste, and forecast industrial Return on Investment (ROI).

**العربية:**  
تُعد **منصة محاكاة الخلايا الشمسية (DRVT)** أداة هندسية واقتصادية تفاعلية مبنية على **نظرية الحجم الرنيني الديناميكي** للدكتور **خالد عبد الفتاح** (جامعة مروي للتكنولوجيا، السودان). تربط هذه المنصة بين الأسس الفيزيائية للرنين الكهرومغناطيسي والتطبيقات العملية لتصنيع الألواح الشمسية، مما يساعد الباحثين والمصنعين على تحسين امتصاص الضوء، وتقليل هدر المواد الخام، وحساب العائد المالي السنوي لخطوط الإنتاج.

---

## 🔬 Theoretical Framework | الإطار النظري للنظرية

**English:**  
Dynamic Resonant Volume Theory proposes that electromagnetic resonance is governed by a three-dimensional geometric interaction volume ($V_{res}$) rather than wavelength ($\lambda$) alone, maintaining equilibrium through a dynamic transverse resonant radius ($r_{res}$):

* **Equilibrium Resonant Volume:** $V_{eq} = \lambda \cdot \pi r_{res}^2 = 286.398\text{ nm}^3$
* **Dynamic Resonant Radius:** $r_{res} = \sqrt{\frac{286.398}{\pi \cdot \lambda}}$
* **Effective Interaction Area:** $A_{eff} = \pi r_{res}^2$
* **Resonant Energy Density Invariant:** $\frac{E}{r_{res}^2} = 13.606\text{ eV/nm}^2$

**العربية:**  
تفترض نظرية الحجم الرنيني الديناميكي أن الرنين الكهرومغناطيسي يُحكم بحجم تفاعل هندسي ثلاثي الأبعاد ($V_{res}$) يجمع بين الطول الموجي ($\lambda$) ونصف القطر الرنيني العرضي المكافئ ($r_{res}$)، مما يتيح تحديد المساحة الفعالة للتفاعل ($A_{eff}$) والطاقة الرنينية بدقة عبر مختلف نطاقات الطيف الشمسي.

---

## 🚀 Key Features | المميزات الرئيسية للمنصة

1. **Quantum & Spectral Analysis (التحليل الطيفي والرنيني):**  
   Calculates resonant radius ($r_{res}$), effective cross-sectional area ($A_{eff}$), photon energy ($E$), and spectral thermalization losses across wavelengths ($300\text{ nm} - 1200\text{ nm}$).
2. **Multi-Material Benchmarking (مقارنة المواد الشمسية):**  
   Supports Crystalline Silicon (c-Si), Standard & Wide-Bandgap Perovskites, Quantum Dots (CdSe), and Tandem Solar Cells.
3. **Material Thickness Optimization (تقليل استهلاك المواد الخام):**  
   Estimates optimal active-layer thickness to achieve full resonant coupling while reducing wafer and raw material costs.
4. **Industrial B2B Financial Forecasting (الجدوى الاقتصادية للمصانع):**  
   Translates efficiency gains and material savings into annual financial returns ($\text{USD/year}$) based on factory production capacity ($\text{MW/year}$).
5. **Executive Report Export (تصدير التقارير التنفيذية):**  
   Generates instant, downloadable technical and financial summaries for R&D teams, pitch decks, and feasibility studies.

---

## 🖥️ Live Demo | التشغيل المباشر

Access the live interactive web application directly via Streamlit Cloud:  
👉 **[Launch DRVT Solar Simulator](https://streamlit.app)**

---

## 🛠️ Local Installation | التشغيل المحلي على جهازك

To run the simulator locally using Python:

```bash
# 1. Clone the repository
git clone https://github.com
cd drvt-solar-design

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run drvt_solar_cell_design.py
```

---

## 📜 Citation & Intellectual Property | الاستشهاد العلمي والملكية الفكرية

* **Author:** Dr. Khalid Abdel Fattah — Merowe Institute of Technology, Merowe University of Technology, Sudan (`khdfattah@gmail.com`).
* **Software License:** The source code in this repository is licensed under the terms specified in the `LICENSE` file.
* **Scientific Theory:** Commercial or industrial deployment of the underlying physical framework (*Dynamic Resonant Volume Theory*) should acknowledge the original theoretical work and coordinate with the author.

