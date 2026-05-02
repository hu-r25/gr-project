import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(
    page_title=" Solver Graphical Method",
    page_icon="📱",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* إخفاء أزرار التحكم وحذف علامات البوينت */
    button.step-up, button.step-down { display: none !important; }
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    input[type=number] { -moz-appearance: textfield; }

    .stNumberInput div div input { 
        background-color: #161b22 !important; 
        color: #58a6ff !important; 
        border: 1px solid #30363d !important;
        font-size: 20px !important;
        height: 45px !important;
        text-align: center;
        border-radius: 8px !important;
    }
    
    .steps-container { 
        background-color: #010409; padding: 25px; border-radius: 12px; 
        border: 1px solid #30363d; font-family: 'Consolas', monospace; 
        color: #c9d1d9; line-height: 1.7; white-space: pre; overflow-x: auto;
    }

    .stButton>button {
        background: linear-gradient(90deg, #1f6feb 0%, #58a6ff 100%);
        color: white; font-weight: bold; height: 50px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك الرياضي ---
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
            res += f" (1) {int(a1)}X1 + {int(b1)}X2 = {int(r1)}\n"
            res += f" (2) {int(a2)}X1 + {int(b2)}X2 = {int(r2)}\n"
            res += f" => Result: Feasible Corner at ({x:.1f}, {y:.1f})\n\n"
            return (x, y), res
        return None, ""

# --- 3. واجهة الإدخال ---
st.title("Graphical Method \n by hussein")

with st.container():
    st.subheader("🎯 دالة الهدف")
    t_col, c1_col, c2_col = st.columns([1, 1, 1])
    with t_col: obj_type = st.selectbox("Type", ["Max", "Min"], label_visibility="collapsed")
    # القيمة البدائية صفر
    with c1_col: z1 = st.number_input("Z1", value=0, step=1, format="%d", label_visibility="collapsed")
    with c2_col: z2 = st.number_input("Z2", value=0, step=1, format="%d", label_visibility="collapsed")

st.write("---")

with st.container():
    st.subheader("📏 القيود")
    num_c = st.selectbox("عدد القيود:", [2, 3, 4], index=1)
    
    constraints_list = []
    for i in range(num_c):
        st.write(f"القيد L{i+1}:")
        v1_c, v2_c, op_c, rhs_c = st.columns([1, 1, 0.8, 1.2])
        # القيمة البدائية صفر وخطوة الزيادة 1 (بدون بوينتات)
        with v1_c: v1 = st.number_input(f"v1_{i}", value=0, step=1, format="%d", key=f"v1_{i}", label_visibility="collapsed")
        with v2_c: v2 = st.number_input(f"v2_{i}", value=0, step=1, format="%d", key=f"v2_{i}", label_visibility="collapsed")
        with op_c: op = st.selectbox(f"op_{i}", ["<=", ">=", "="], key=f"op_{i}", label_visibility="collapsed")
        with rhs_c: rhs = st.number_input(f"rhs_{i}", value=0, step=1, format="%d", key=f"rhs_{i}", label_visibility="collapsed")
        constraints_list.append(([v1, v2], op, rhs, i + 1))

run_btn = st.button("بدأ التحليل الرياضي")

if run_btn:
    try:
        report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
        report += "STEP 1: AXIS INTERCEPTS (SUBSTITUTION MATH)\n"
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints_list):
            corner_points.append((0,0))
            report += " - Origin Point Check: (0,0) is Feasible\n"

        for coeffs, op, rhs, idx in constraints_list:
            report += f"\nConstraint L{idx}: {int(coeffs[0])}X1 + {int(coeffs[1])}X2 = {int(rhs)}\n"
            if coeffs[0] != 0:
                p = (rhs/coeffs[0], 0)
                report += f" - Let X2 = 0: {int(coeffs[0])}X1 = {int(rhs)} -> X1 = {p[0]:.1f}\n"
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += "   [Status: Feasible Corner Point]\n"
                else: report += "   [Status: Discarded - Outside Area]\n"
            if coeffs[1] != 0:
                p = (0, rhs/coeffs[1])
                report += f" - Let X1 = 0: {int(coeffs[1])}X2 = {int(rhs)} -> X2 = {p[1]:.1f}\n"
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += "   [Status: Feasible Corner Point]\n"
                else: report += "   [Status: Discarded - Outside Area]\n"

        report += "\n" + "="*45 + "\nSTEP 2: LINE INTERSECTIONS (ELIMINATION)\n\n"
        for i in range(len(constraints_list)):
            for j in range(i+1, len(constraints_list)):
                pt, info = HusseinSolver.solve_with_report(constraints_list[i], constraints_list[j], constraints_list)
                if pt:
                    corner_points.append(pt)
                    report += info

        unique_corners = []
        seen = set()
        report += "="*45 + "\nSTEP 3: CORNER POINT Z-EVALUATION\n\n"
        for p in corner_points:
            rnd = (round(p[0], 4), round(p[1], 4))
            if rnd not in seen:
                seen.add(rnd)
                z_val = z1*p[0] + z2*p[1]
                unique_corners.append((p, z_val))
                report += f" Evaluating ({p[0]:.1f}, {p[1]:.1f}) -> Z = {z_val:.1f}\n"

        best = max(unique_corners, key=lambda x: x[1]) if obj_type == "Max" else min(unique_corners, key=lambda x: x[1])
        report += f"\n>>> FINAL OPTIMAL SOLUTION <<<\nZ = {best[1]:.1f} at X1={best[0][0]:.1f}, X2={best[0][1]:.1f}"

        # العرض
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#161b22')
        limit = max([p[0] for p in corner_points] + [p[1] for p in corner_points]) * 1.3 if corner_points else 10
        x_ax = np.linspace(0, limit, 400)
        for (coeffs, op, rhs, idx) in constraints_list:
            if coeffs[1] != 0: ax.plot(x_ax, (rhs - coeffs[0]*x_ax)/coeffs[1], lw=2)
            else: ax.axvline(x=rhs/coeffs[0], color="orange", lw=2)
        if len(unique_corners) >= 3:
            pts = np.array([u[0] for u in unique_corners])
            c = np.mean(pts, axis=0)
            a = np.arctan2(pts[:,1]-c[1], pts[:,0]-c[0])
            pts = pts[np.argsort(a)]
            ax.fill(pts[:,0], pts[:,1], color="#58a6ff", alpha=0.3)
        ax.scatter(best[0][0], best[0][1], color='red', s=150, zorder=5)
        ax.set_xlim(0, limit); ax.set_ylim(0, limit)
        ax.tick_params(colors='#8b949e'); ax.grid(color='#30363d', alpha=0.3)
        st.pyplot(fig)
        
        st.subheader("🏁 النتائج")
        m1, m2, m3 = st.columns(3)
        m1.metric("Optimal Z", f"{best[1]:.1f}")
        m2.metric("X1 Value", f"{best[0][0]:.1f}")
        m3.metric("X2 Value", f"{best[0][1]:.1f}")

        st.subheader("📄 التحليل الرياضي التفصيلي")
        st.markdown(f'<div class="steps-container">{report}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")
