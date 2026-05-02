import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة والتنسيق ---
st.set_page_config(page_title="Hussein Optimization Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    /* تنسيق خانات الإدخال لتكون واضحة وبدون رموز جانبية */
    .stNumberInput div div input { 
        background-color: #161b22 !important; 
        color: #00ff00 !important; 
        border: 1px solid #30363d !important;
        font-size: 18px !important;
        text-align: center;
    }
    .label-text { font-size: 1.2rem; font-weight: bold; color: #00d1ff; margin-top: 10px; }
    .steps-card { 
        background-color: #0d1117; padding: 25px; border-radius: 15px; 
        border: 1px solid #30363d; font-family: 'Consolas', monospace; 
        color: #c9d1d9; line-height: 1.6; overflow-x: auto;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d1ff 0%, #0072ff 100%);
        color: white; font-weight: bold; border: none; width: 100%; height: 3em;
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
    def solve_with_steps(c1, c2, constraints):
        a1, b1, r1 = c1[0][0], c1[0][1], c1[2]
        a2, b2, r2 = c2[0][0], c2[0][1], c2[2]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9: return None, ""
        x = (r1 * b2 - r2 * b1) / det
        y = (a1 * r2 - a2 * r1) / det
        if HusseinSolver.is_feasible((x, y), constraints):
            report = f"--- Intersection L{c1[3]} & L{c2[3]} ---\n"
            report += f" Elimination Method Applied:\n"
            report += f"  Eq1: ({a1})X1 + ({b1})X2 = {r1}\n"
            report += f"  Eq2: ({a2})X1 + ({b2})X2 = {r2}\n"
            report += f" Result: Feasible corner at X1={x:.2f}, X2={y:.2f}\n\n"
            return (x, y), report
        return None, ""

# --- 3. واجهة المستخدم ---
st.title("🛡️ Hussein Graphical Solver - Clean Input")
st.markdown("---")

col_in, col_res = st.columns([1, 1.2], gap="large")

with col_in:
    st.subheader("⚙️ إدخال المعاملات الرقمية")
    
    # دالة الهدف
    st.markdown('<p class="label-text">🎯 دالة الهدف (Z)</p>', unsafe_allow_html=True)
    obj_type = st.selectbox("نوع الدالة", ["Max", "Min"], label_visibility="collapsed")
    
    z_col1, z_txt, z_col2 = st.columns([1, 0.2, 1])
    with z_col1: z1 = st.number_input("Coeff X1", value=3.0, label_visibility="collapsed")
    with z_txt: st.markdown("<div style='text-align:center; padding-top:10px;'>X1</div>", unsafe_allow_html=True)
    with z_col2: z2 = st.number_input("Coeff X2", value=5.0, label_visibility="collapsed")
    
    st.write("---")
    
    # القيود
    st.markdown('<p class="label-text">📏 القيود (Constraints)</p>', unsafe_allow_html=True)
    num_c = st.slider("عدد القيود", 1, 10, 3)
    
    constraints_list = []
    for i in range(num_c):
        st.markdown(f"**القيد {i+1}**")
        c1, t1, c2, t2, cop, crhs = st.columns([1, 0.2, 1, 0.2, 1, 1.2])
        with c1: v1 = st.number_input(f"v1_{i}", value=1.0, key=f"v1_{i}", label_visibility="collapsed")
        with t1: st.write("X1")
        with c2: v2 = st.number_input(f"v2_{i}", value=1.0, key=f"v2_{i}", label_visibility="collapsed")
        with t2: st.write("X2")
        with cop: op = st.selectbox(f"op_{i}", ["<=", ">=", "="], key=f"op_{i}", label_visibility="collapsed")
        with crhs: rhs = st.number_input(f"rhs_{i}", value=10.0, key=f"rhs_{i}", label_visibility="collapsed")
        constraints_list.append(([v1, v2], op, rhs, i + 1))

    st.write("")
    run_btn = st.button("تحليل المسألة")

if run_btn:
    try:
        report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
        report += "STEP 1: AXIS INTERCEPTS (Substitution)\n"
        
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints_list):
            corner_points.append((0,0))
            report += " - (0,0) Checked: Feasible\n"
        else:
            report += " - (0,0) Checked: Outside Area\n"

        for coeffs, op, rhs, idx in constraints_list:
            report += f"\n[Constraint L{idx}: {coeffs[0]}X1 + {coeffs[1]}X2 {op} {rhs}]\n"
            if coeffs[0] != 0:
                p = (rhs/coeffs[0], 0)
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += f" - Let X2=0: X1 = {rhs}/{coeffs[0]} = {p[0]:.2f} (Feasible)\n"
            if coeffs[1] != 0:
                p = (0, rhs/coeffs[1])
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += f" - Let X1=0: X2 = {rhs}/{coeffs[1]} = {p[1]:.2f} (Feasible)\n"

        report += "\n" + "="*45 + "\nSTEP 2: FINDING INTERSECTIONS (Elimination)\n"
        for i in range(len(constraints_list)):
            for j in range(i+1, len(constraints_list)):
                pt, info = HusseinSolver.solve_with_steps(constraints_list[i], constraints_list[j], constraints_list)
                if pt:
                    corner_points.append(pt)
                    report += info

        unique_corners = []
        seen = set()
        report += "="*45 + "\nSTEP 3: OPTIMALITY EVALUATION\n"
        for p in corner_points:
            rnd = (round(p[0], 4), round(p[1], 4))
            if rnd not in seen:
                seen.add(rnd)
                z_val = z1*p[0] + z2*p[1]
                unique_corners.append((p, z_val))
                report += f" Pt({p[0]:.2f}, {p[1]:.2f}) -> Z = {z_val:.2f}\n"

        if not unique_corners:
            st.error("Infeasible Region!")
        else:
            # المنطق الصحيح لاختيار الحل (Max أو Min)
            best = max(unique_corners, key=lambda x: x[1]) if obj_type == "Max" else min(unique_corners, key=lambda x: x[1])
            report += f"\n>>> FINAL OPTIMAL SOLUTION <<<\nTarget: {obj_type}\nBest Z = {best[1]:.2f} at X1={best[0][0]:.2f}, X2={best[0][1]:.2f}"

            with col_res:
                st.subheader("📊 الرسم البياني")
                fig, ax = plt.subplots(figsize=(8, 7))
                fig.patch.set_facecolor('#0e1117'); ax.set_facecolor('#161b22')
                
                # حساب أبعاد الرسم
                limit = max([p[0] for p in corner_points] + [p[1] for p in corner_points]) * 1.3
                x_ax = np.linspace(0, limit, 400)
                
                for (coeffs, op, rhs, idx) in constraints_list:
                    if coeffs[1] != 0:
                        ax.plot(x_ax, (rhs - coeffs[0]*x_ax)/coeffs[1], label=f"L{idx}")
                    else:
                        ax.axvline(x=rhs/coeffs[0], label=f"L{idx}", color="orange")

                if len(unique_corners) >= 3:
                    pts = np.array([u[0] for u in unique_corners])
                    c = np.mean(pts, axis=0)
                    a = np.arctan2(pts[:,1]-c[1], pts[:,0]-c[0])
                    pts = pts[np.argsort(a)]
                    ax.fill(pts[:,0], pts[:,1], color="#00d1ff", alpha=0.3, label="Feasible Area")

                ax.scatter(best[0][0], best[0][1], color='red', s=200, edgecolors='white', zorder=5)
                ax.set_xlim(0, limit); ax.set_ylim(0, limit)
                ax.tick_params(colors='white'); ax.grid(color='#30363d')
                ax.legend(facecolor='#161b22', labelcolor='white')
                st.pyplot(fig)
                
                st.write("---")
                st.subheader("🏁 النتائج")
                m1, m2, m3 = st.columns(3)
                m1.metric("Optimal Z", f"{best[1]:.2f}")
                m2.metric("X1", f"{best[0][0]:.2f}")
                m3.metric("X2", f"{best[0][1]:.2f}")

        st.subheader("📄 التحليل الرياضي التفصيلي")
        st.markdown(f'<div class="steps-card">{report}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
