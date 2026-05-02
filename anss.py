import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_page_config(page_title="Hussein Optimization System", layout="wide")

st.markdown("""
    <style>
    /* تنسيق الخلفية العامة */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* تنسيق الحاويات (Containers) */
    .stNumberInput div div input { 
        background-color: #262730 !important; 
        color: #00ff00 !important; 
        border: 1px solid #444 !important;
        font-size: 18px !important;
    }
    
    /* تنسيق العناوين */
    h1, h2, h3 { color: #00d1ff !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تنسيق منطقة التحليل الرياضي */
    .steps-card { 
        background-color: #161b22; 
        padding: 30px; 
        border-radius: 15px; 
        border: 1px solid #30363d; 
        font-family: 'Consolas', monospace; 
        color: #c9d1d9;
        line-height: 1.6;
    }
    
    /* تنسيق الأزرار */
    .stButton>button {
        background: linear-gradient(90deg, #00d1ff 0%, #0072ff 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.6rem 2rem;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); color: black; }
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
    def solve_intersection(c1, c2, constraints):
        a1, b1 = c1[0]; r1 = c1[2]
        a2, b2 = c2[0]; r2 = c2[2]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9: return None, ""
        x = (r1 * b2 - r2 * b1) / det
        y = (a1 * r2 - a2 * r1) / det
        if HusseinSolver.is_feasible((x, y), constraints):
            report = f"INTERSECTION L{c1[3]} & L{c2[3]} (Elimination):\n"
            report += f" (1) {a1}X1 + {b1}X2 = {r1}\n"
            report += f" (2) {a2}X1 + {b2}X2 = {r2}\n"
            report += f" => Result: Corner at ({x:.2f}, {y:.2f})\n\n"
            return (x, y), report
        return None, ""

# --- 3. واجهة المستخدم المنظمة ---
st.title("🛡️ Hussein Graphical Reasoning System")
st.write("نظام التحليل الرياضي المتطور - واجهة الإدخال المباشر")
st.markdown("---")

# تقسيم الصفحة إلى قسمين: المدخلات والنتائج
col_input, col_display = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("⚙️ إعدادات المسألة")
    
    # دالة الهدف بتصميم نظيف
    with st.expander("🎯 دالة الهدف (Objective Function)", expanded=True):
        m1, m2, m3 = st.columns(3)
        with m1: obj_type = st.selectbox("النوع", ["Max", "Min"])
        with m2: c1 = st.number_input("معامل X1", value=3.0)
        with m3: c2 = st.number_input("معامل X2", value=5.0)

    # التحكم بالقيود
    num_constraints = st.slider("عدد القيود المطلوبة", 1, 10, 3)
    
    constraints_list = []
    st.write("📝 **قيم القيود:**")
    for i in range(num_constraints):
        with st.container():
            r1, r2, r3, r4 = st.columns([1, 1, 1, 1.2])
            with r1: v1 = st.number_input(f"X1 (L{i+1})", value=1.0, key=f"v1_{i}")
            with r2: v2 = st.number_input(f"X2 (L{i+1})", value=1.0, key=f"v2_{i}")
            with r3: op = st.selectbox("الرمز", ["<=", ">=", "="], key=f"op_{i}")
            with r4: rhs = st.number_input(f"الناتج", value=10.0, key=f"rhs_{i}")
            constraints_list.append(([v1, v2], op, rhs, i + 1))
    
    st.write("")
    run_btn = st.button("تحليل المسألة ورسم الحل")

if run_btn:
    try:
        # --- التحليل الرياضي ---
        report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
        report += "STEP 1: AXIS INTERCEPTS\n"
        
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints_list):
            corner_points.append((0,0))
            report += " - (0,0) Checked: Feasible\n"

        for coeffs, op, rhs, idx in constraints_list:
            report += f"\n[Constraint L{idx}: {coeffs[0]}X1 + {coeffs[1]}X2 {op} {rhs}]\n"
            if coeffs[0] != 0:
                p = (rhs/coeffs[0], 0)
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += f" - Let X2=0 => X1={p[0]:.2f}. (Feasible)\n"
                else: report += f" - Let X2=0 => X1={rhs/coeffs[0]:.2f}. (Outside)\n"
            
            if coeffs[1] != 0:
                p = (0, rhs/coeffs[1])
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += f" - Let X1=0 => X2={p[1]:.2f}. (Feasible)\n"
                else: report += f" - Let X1=0 => X2={rhs/coeffs[1]:.2f}. (Outside)\n"

        report += "\n" + "="*45 + "\nSTEP 2: LINE INTERSECTIONS\n"
        for i in range(len(constraints_list)):
            for j in range(i+1, len(constraints_list)):
                pt, info = HusseinSolver.solve_intersection(constraints_list[i], constraints_list[j], constraints_list)
                if pt:
                    corner_points.append(pt)
                    report += info

        unique_corners = []
        seen = set()
        report += "="*45 + "\nSTEP 3: EVALUATING CORNERS\n"
        for p in corner_points:
            rnd = (round(p[0], 4), round(p[1], 4))
            if rnd not in seen:
                seen.add(rnd)
                z = c1*p[0] + c2*p[1]
                unique_corners.append((p, z))
                report += f" Pt({p[0]:.2f}, {p[1]:.2f}) -> Z = {z:.2f}\n"

        best = max(unique_corners, key=lambda x: x[1]) if obj_type == "Max" else min(unique_corners, key=lambda x: x[1])
        report += f"\n>>> FINAL OPTIMAL SOLUTION <<<\nZ = {best[1]:.2f} at X1={best[0][0]:.2f}, X2={best[0][1]:.2f}"

        # --- العرض في القسم الثاني ---
        with col_display:
            st.subheader("📊 المخرجات البيانية")
            fig, ax = plt.subplots(figsize=(8, 7))
            fig.patch.set_facecolor('#0e1117'); ax.set_facecolor('#161b22')
            
            # حساب الحدود
            all_vals = [p[0] for p in corner_points] + [p[1] for p in corner_points]
            lim = max(all_vals) * 1.3 if all_vals else 10
            x_ax = np.linspace(0, lim, 400)
            
            for (coeffs, op, rhs, idx) in constraints_list:
                if coeffs[1] != 0:
                    ax.plot(x_ax, (rhs - coeffs[0]*x_ax)/coeffs[1], label=f"L{idx}", lw=2)
                else:
                    ax.axvline(x=rhs/coeffs[0], label=f"L{idx}", color="orange", lw=2)

            if len(unique_corners) >= 3:
                pts = np.array([u[0] for u in unique_corners])
                center = np.mean(pts, axis=0)
                angles = np.arctan2(pts[:,1]-center[1], pts[:,0]-center[0])
                pts = pts[np.argsort(angles)]
                ax.fill(pts[:,0], pts[:,1], color="#00d1ff", alpha=0.3, label="Feasible Area")

            ax.scatter(best[0][0], best[0][1], color='#ff0055', s=250, zorder=5, edgecolors='white')
            ax.set_xlim(0, lim); ax.set_ylim(0, lim)
            ax.tick_params(colors='white'); ax.grid(color='#30363d')
            ax.legend(facecolor='#161b22', labelcolor='white')
            st.pyplot(fig)

            # بطاقات النتائج
            st.write("---")
            r1, r2, r3 = st.columns(3)
            r1.metric("Optimal Z", f"{best[1]:.2f}")
            r2.metric("Value X1", f"{best[0][0]:.2f}")
            r3.metric("Value X2", f"{best[0][1]:.2f}")

        # التقرير في الأسفل
        st.subheader("📄 التحليل الرياضي المفصل")
        st.markdown(f'<div class="steps-card">{report}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"خطأ في الحسابات: {e}")
