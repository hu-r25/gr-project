import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Hussein Graphical Solver", layout="wide")

# --- تنسيق واجهة المستخدم CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0f0f0f; color: #e0e0e0; }
    .stNumberInput>div>div>input { background-color: #222; color: #00ff00; font-weight: bold; }
    .steps-container { 
        background-color: #1a1a1a; padding: 25px; border-radius: 10px; 
        border: 1px solid #333; font-family: 'Consolas', monospace; 
        white-space: pre-wrap; color: #f0f0f0;
    }
    .stButton>button { width: 100%; background: #00d1ff; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

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
    def solve_intersection(c1, c2, constraints):
        a1, b1 = c1[0]; r1 = c1[2]
        a2, b2 = c2[0]; r2 = c2[2]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9: return None, ""
        x = (r1 * b2 - r2 * b1) / det
        y = (a1 * r2 - a2 * r1) / det
        if HusseinSolver.is_feasible((x, y), constraints):
            report = f"INTERSECTION L{c1[3]} & L{c2[3]} (Substitution):\n"
            report += f" (1) {a1}X1 + {b1}X2 = {r1}\n"
            report += f" (2) {a2}X1 + {b2}X2 = {r2}\n"
            report += f" => Result: Feasible Corner at ({x:.2f}, {y:.2f})\n\n"
            return (x, y), report
        return None, ""

st.title("📊 Graphical Method Solver - Numeric Input")
st.write("Developed by **Hussein**")

# --- إدخال دالة الهدف ---
st.subheader("1. دالة الهدف (Objective Function)")
obj_col1, obj_col2, obj_col3 = st.columns([1, 1, 1])
with obj_col1:
    mode = st.selectbox("النوع (Mode):", ["Max", "Min"])
with obj_col2:
    z_x1 = st.number_input("معامل X1 (Z):", value=3.0)
with obj_col3:
    z_x2 = st.number_input("معامل X2 (Z):", value=5.0)

# --- التحكم في عدد القيود ---
st.subheader("2. القيود (Constraints)")
num_constraints = st.number_input("حدد عدد القيود:", min_value=1, max_value=10, value=3)

constraints_data = []
for i in range(int(num_constraints)):
    st.markdown(f"**القيد رقم {i+1}:**")
    c_col1, c_col2, c_col3, c_col4 = st.columns([1, 1, 1, 1.5])
    with c_col1:
        x1_val = st.number_input(f"X1 (L{i+1})", value=1.0, key=f"x1_{i}")
    with c_col2:
        x2_val = st.number_input(f"X2 (L{i+1})", value=1.0, key=f"x2_{i}")
    with c_col3:
        op = st.selectbox("الرمز", ["<=", ">=", "="], key=f"op_{i}")
    with c_col4:
        rhs_val = st.number_input(f"الناتج (RHS {i+1})", value=10.0, key=f"rhs_{i}")
    constraints_data.append(([x1_val, x2_val], op, rhs_val, i + 1))

analyze_btn = st.button("بدأ التحليل الرياضي الشامل")

if analyze_btn:
    try:
        report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
        report += "STEP 1: AXIS INTERCEPTS (SUBSTITUTION MATH)\n"
        
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints_data):
            corner_points.append((0,0))
            report += " - Origin Point Check: (0,0) is Feasible\n"

        for coeffs, op, rhs, idx in constraints_data:
            report += f"\nConstraint L{idx}: {coeffs[0]}X1 + {coeffs[1]}X2 {op} {rhs}\n"
            # Let X2 = 0
            if coeffs[0] != 0:
                val = rhs / coeffs[0]
                report += f" - Let X2 = 0: {coeffs[0]}X1 + {coeffs[1]}(0) = {rhs}\n"
                report += f"   => {coeffs[0]}X1 = {rhs} -> X1 = {val:.2f}. Point: ({val:.2f}, 0)\n"
                if HusseinSolver.is_feasible((val, 0), constraints_data):
                    corner_points.append((val, 0))
                    report += "   [Status: Feasible Corner Point]\n"
                else: report += "   [Status: Discarded - Outside Area]\n"
            
            # Let X1 = 0
            if coeffs[1] != 0:
                val = rhs / coeffs[1]
                report += f" - Let X1 = 0: {coeffs[0]}(0) + {coeffs[1]}X2 = {rhs}\n"
                report += f"   => {coeffs[1]}X2 = {rhs} -> X2 = {val:.2f}. Point: (0, {val:.2f})\n"
                if HusseinSolver.is_feasible((0, val), constraints_data):
                    corner_points.append((0, val))
                    report += "   [Status: Feasible Corner Point]\n"
                else: report += "   [Status: Discarded - Outside Area]\n"

        report += "\n" + "="*45 + "\nSTEP 2: LINE INTERSECTIONS (ELIMINATION)\n"
        for i in range(len(constraints_data)):
            for j in range(i+1, len(constraints_data)):
                pt, info = HusseinSolver.solve_intersection(constraints_data[i], constraints_data[j], constraints_data)
                if pt:
                    corner_points.append(pt)
                    report += info

        unique_corners = []
        seen = set()
        report += "="*45 + "\nSTEP 3: CORNER POINT Z-EVALUATION\n"
        for p in corner_points:
            rnd = (round(p[0], 4), round(p[1], 4))
            if rnd not in seen:
                seen.add(rnd)
                z = z_x1*p[0] + z_x2*p[1]
                unique_corners.append((p, z))
                report += f" Evaluating ({p[0]:.2f}, {p[1]:.2f}) -> Z = {z:.2f}\n"

        best = max(unique_corners, key=lambda x: x[1]) if mode == "Max" else min(unique_corners, key=lambda x: x[1])
        report += f"\n>>> OPTIMAL SOLUTION <<<\nZ = {best[1]:.2f} at X1={best[0][0]:.2f}, X2={best[0][1]:.2f}"

        # --- الرسم البياني ---
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#0f0f0f'); ax.set_facecolor('#1a1a1a')
        
        all_intercepts = []
        for c, o, r, _ in constraints_data:
            if c[0] != 0: all_intercepts.append(r/c[0])
            if c[1] != 0: all_intercepts.append(r/c[1])
        
        limit = max(all_intercepts) * 1.3 if all_intercepts else 10
        x = np.linspace(0, limit, 400)
        
        for c, o, r, idx in constraints_data:
            if c[1] != 0: ax.plot(x, (r - c[0]*x)/c[1], label=f"L{idx}")
            else: ax.axvline(x=r/c[0], label=f"L{idx}", color="orange")

        if len(unique_corners) >= 3:
            pts = np.array([u[0] for u in unique_corners])
            center = np.mean(pts, axis=0)
            angles = np.arctan2(pts[:,1]-center[1], pts[:,0]-center[0])
            pts = pts[np.argsort(angles)]
            ax.fill(pts[:,0], pts[:,1], color="#00d1ff", alpha=0.3)

        ax.scatter(best[0][0], best[0][1], color='red', s=200, zorder=5)
        ax.set_xlim(0, limit); ax.set_ylim(0, limit)
        ax.tick_params(colors='white'); ax.grid(alpha=0.2)
        ax.legend(); st.pyplot(fig)

        # عرض التقرير والنتائج
        st.success(f"### النتيجة النهائية: Z = {best[1]:.2f} عند X1={best[0][0]:.2f}, X2={best[0][1]:.2f}")
        st.markdown("### 📝 Detailed Mathematical Analysis")
        st.markdown(f'<div class="steps-container">{report}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"حدث خطأ: {e}")
