import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة والتصميم الفاخر ---
st.set_page_config(page_title="Graphical Method", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e6edf3; }
    
    /* إخفاء أزرار التحكم تماماً */
    button.step-up, button.step-down { display: none !important; }
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    
    /* تنسيق الحقول الرقمية */
    .stNumberInput div div input { 
        background-color: #161b22 !important; 
        color: #58a6ff !important; 
        border: 1px solid #30363d !important;
        font-size: 20px !important;
        height: 50px !important;
        text-align: center;
        border-radius: 12px !important;
    }

    /* صناديق النتائج النهائية */
    .result-card {
        background: linear-gradient(135deg, #1f6feb 0%, #111 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }

    /* حاوية التقرير الرياضي */
    .steps-container { 
        background-color: #0d1117; 
        padding: 30px; 
        border-radius: 15px; 
        border: 1px solid #30363d; 
        font-family: 'Consolas', monospace; 
        color: #8b949e; 
        line-height: 1.8; 
        white-space: pre; 
        overflow-x: auto;
        box-shadow: inset 0 0 10px #000;
    }

    .stButton>button {
        background: #238636;
        color: white; font-weight: bold; height: 55px; border-radius: 12px;
        font-size: 1.2rem; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background: #2ea043; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك الرياضي الذكي ---
class HusseinSolver:
    @staticmethod
    def is_feasible(p, constraints):
        x1, x2 = p
        if x1 < -1e-7 or x2 < -1e-7: return False
        for coeffs, op, rhs, _ in constraints:
            val = coeffs[0]*x1 + coeffs[1]*x2
            if op == "<=" and val > rhs + 1e-7: return False
            if op == ">=" and val < rhs - 1e-7: return False
            if op == "=" and abs(val - rhs) > 1e-7: return False
        return True

    @staticmethod
    def solve_with_report(c1, c2, constraints):
        a1, b1, r1 = c1[0][0], c1[0][1], c1[2]
        a2, b2, r2 = c2[0][0], c2[0][1], c2[2]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9: return None, ""
        x = (r1 * b2 - r2 * b1) / det
        y = (a1 * r2 - a2 * r1) / det
        if HusseinSolver.is_feasible((x, y), constraints):
            res = f"INTERSECTION L{c1[3]} & L{c2[3]} (Elimination):\n"
            res += f"  Eq1: {int(a1)}X1 + {int(b1)}X2 = {int(r1)}\n"
            res += f"  Eq2: {int(a2)}X1 + {int(b2)}X2 = {int(r2)}\n"
            res += f"  => Result: Corner at ({x:.1f}, {y:.1f})\n\n"
            return (x, y), res
        return None, ""

# --- 3. بناء الواجهة ---
st.markdown("<h1>Graphical Method ></h1>", unsafe_allow_html=True)
st.markdown("<h3>Graphical Method ></h3>", unsafe_allow_html=True)
with st.container():
    st.subheader("🎯 دالة الهدف (Objective Function)")
    c_type, c_z1, c_z2 = st.columns([1, 1, 1])
    with c_type: obj_type = st.selectbox("Type", ["Max", "Min"], label_visibility="collapsed")
    with c_z1: z1 = st.number_input("Z1", value=0, step=1, format="%d", label_visibility="collapsed")
    with c_z2: z2 = st.number_input("Z2", value=0, step=1, format="%d", label_visibility="collapsed")
    st.markdown(f"<p style='text-align:center; color:#58a6ff;'>Objective: {obj_type} Z = {z1}X1 + {z2}X2</p>", unsafe_allow_html=True)

st.write("---")

with st.container():
    st.subheader("📏 القيود (Constraints)")
    num_c = st.selectbox("عدد القيود المتاحة:", [2, 3, 4], index=1)
    
    constraints_list = []
    for i in range(num_c):
        st.markdown(f"**القيد {i+1}**")
        v1, v2, op_s, rh_v = st.columns([1, 1, 0.8, 1.2])
        with v1: val1 = st.number_input(f"v1_{i}", value=0, step=1, format="%d", key=f"v1_{i}", label_visibility="collapsed")
        with v2: val2 = st.number_input(f"v2_{i}", value=0, step=1, format="%d", key=f"v2_{i}", label_visibility="collapsed")
        with op_s: op = st.selectbox(f"op_{i}", ["<=", ">=", "="], key=f"op_{i}", label_visibility="collapsed")
        with rh_v: rhs = st.number_input(f"rhs_{i}", value=0, step=1, format="%d", key=f"rhs_{i}", label_visibility="collapsed")
        constraints_list.append(([val1, val2], op, rhs, i + 1))

st.write("")
if st.button("🚀 بدأ التحليل الرياضي الآن"):
    try:
        # --- التقرير والنتائج ---
        report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
        report += "STEP 1: AXIS INTERCEPTS (Substitution)\n"
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints_list):
            corner_points.append((0,0))
            report += " - Origin Point (0,0) is Feasible\n"

        for coeffs, op, rhs, idx in constraints_list:
            report += f"\nConstraint L{idx}: {int(coeffs[0])}X1 + {int(coeffs[1])}X2 = {int(rhs)}\n"
            if coeffs[0] != 0:
                p = (rhs/coeffs[0], 0)
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += f" - Let X2=0: {int(coeffs[0])}X1={int(rhs)} -> X1={p[0]:.1f} [Feasible]\n"
                else: report += f" - Let X2=0: X1={rhs/coeffs[0]:.1f} [Discarded]\n"
            if coeffs[1] != 0:
                p = (0, rhs/coeffs[1])
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += f" - Let X1=0: {int(coeffs[1])}X2={int(rhs)} -> X2={p[1]:.1f} [Feasible]\n"
                else: report += f" - Let X1=0: X2={rhs/coeffs[1]:.1f} [Discarded]\n"

        report += "\n" + "="*45 + "\nSTEP 2: LINE INTERSECTIONS (Elimination)\n\n"
        for i in range(len(constraints_list)):
            for j in range(i+1, len(constraints_list)):
                pt, info = HusseinSolver.solve_with_report(constraints_list[i], constraints_list[j], constraints_list)
                if pt:
                    corner_points.append(pt)
                    report += info

        unique_corners = []
        seen = set()
        report += "="*45 + "\nSTEP 3: EVALUATING CORNER POINTS\n\n"
        for p in corner_points:
            rnd = (round(p[0], 4), round(p[1], 4))
            if rnd not in seen:
                seen.add(rnd)
                z_val = z1*p[0] + z2*p[1]
                unique_corners.append((p, z_val))
                report += f" Evaluating ({p[0]:.1f}, {p[1]:.1f}) -> Z = {z_val:.1f}\n"

        # اختيار الحل الأمثل (تجاهل الصفر في الـ Min)
        if obj_type == "Max":
            best = max(unique_corners, key=lambda x: x[1])
        else:
            non_zero = [c for c in unique_corners if c[1] > 1e-7]
            best = min(non_zero, key=lambda x: x[1]) if non_zero else (unique_corners[0])

        report += f"\n>>> FINAL OPTIMAL SOLUTION <<<\nTarget: {obj_type}\nBest Z = {best[1]:.1f} at X1={best[0][0]:.1f}, X2={best[0][1]:.1f}"

        # عرض النتائج في كروت جميلة
        st.markdown(f"""
            <div class="result-card">
                <h2 style='margin:0; color:#58a6ff;'>Optimal Value: Z = {best[1]:.1f}</h2>
                <p style='margin:0; font-size:1.2rem;'>at X1 = {best[0][0]:.1f}, X2 = {best[0][1]:.1f}</p>
            </div>
        """, unsafe_allow_html=True)

        # الرسم البياني
        fig, ax = plt.subplots(figsize=(7, 6))
        fig.patch.set_facecolor('#0e1117'); ax.set_facecolor('#161b22')
        all_x = [p[0] for p in corner_points]; all_y = [p[1] for p in corner_points]
        lim = max(all_x + all_y) * 1.3 if corner_points else 10
        x_space = np.linspace(0, lim, 400)
        for (coeffs, op, rhs, idx) in constraints_list:
            if coeffs[1] != 0: ax.plot(x_space, (rhs - coeffs[0]*x_space)/coeffs[1], lw=2.5, label=f"L{idx}")
            else: ax.axvline(x=rhs/coeffs[0], color="orange", lw=2.5, label=f"L{idx}")
        if len(unique_corners) >= 3:
            pts = np.array([u[0] for u in unique_corners])
            c = np.mean(pts, axis=0); a = np.arctan2(pts[:,1]-c[1], pts[:,0]-c[0]); pts = pts[np.argsort(a)]
            ax.fill(pts[:,0], pts[:,1], color="#58a6ff", alpha=0.3)
        ax.scatter(best[0][0], best[0][1], color='#f85149', s=200, zorder=10, edgecolors='white')
        ax.set_xlim(0, lim); ax.set_ylim(0, lim); ax.tick_params(colors='#8b949e'); ax.grid(alpha=0.2)
        ax.legend(facecolor='#0d1117', labelcolor='white')
        st.pyplot(fig)

        st.markdown("### 📄 التحليل الرياضي التفصيلي")
        st.markdown(f'<div class="steps-container">{report}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"يرجى إدخال قيم صحيحة. خطأ: {e}")
