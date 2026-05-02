import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة والتصميم المتجاوب للجوال ---
st.set_page_config(
    page_title="Hussein Optima App",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تصميم محاكي لتطبيقات الجوال الاحترافية
st.markdown("""
    <style>
    /* تحسين الخلفية العامة */
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* إخفاء أزرار التحكم الجانبية نهائياً */
    button.step-up, button.step-down { display: none !important; }
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    input[type=number] { -moz-appearance: textfield; }

    /* تنسيق خانات الإدخال لتكون سهلة اللمس على الجوال */
    .stNumberInput div div input { 
        background-color: #161b22 !important; 
        color: #58a6ff !important; 
        border: 2px solid #30363d !important;
        font-size: 18px !important;
        height: 45px !important;
        text-align: center;
        border-radius: 10px !important;
    }
    
    /* تنسيق العناوين */
    h1 { font-size: 1.8rem !important; color: #58a6ff !important; text-align: center; }
    h3 { font-size: 1.2rem !important; color: #00d1ff !important; }

    /* حاوية التحليل الرياضي */
    .steps-card { 
        background-color: #010409; padding: 20px; border-radius: 12px; 
        border: 1px solid #30363d; font-family: 'Consolas', monospace; 
        color: #8b949e; line-height: 1.5; font-size: 0.9rem;
        overflow-x: auto;
    }

    /* زر التشغيل (التصميم العائم) */
    .stButton>button {
        background: linear-gradient(90deg, #1f6feb 0%, #58a6ff 100%);
        color: white; font-weight: bold; border: none; width: 100%; 
        height: 50px; border-radius: 12px; font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(31, 111, 235, 0.3);
    }
    
    /* تحسين عرض الأعمدة على الشاشات الصغيرة */
    [data-testid="column"] { min-width: 45% !important; }
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
            report = f"• Intersection L{c1[3]} & L{c2[3]}: ({x:.2f}, {y:.2f})\n"
            return (x, y), report
        return None, ""

# --- 3. واجهة التطبيق ---
st.title("📱 Hussein Solver App")
st.markdown("<p style='text-align: center; color: #8b949e;'>نظام التحليل الرياضي الذكي للموبايل</p>", unsafe_allow_html=True)

# القسم الأول: المدخلات
with st.container():
    st.subheader("🎯 دالة الهدف")
    t_col, c1_col, c2_col = st.columns([1, 1, 1])
    with t_col: obj_type = st.selectbox("النوع", ["Max", "Min"], label_visibility="collapsed")
    with c1_col: z1 = st.number_input("Z-X1", value=3.0, label_visibility="collapsed")
    with c2_col: z2 = st.number_input("Z-X2", value=5.0, label_visibility="collapsed")
    st.markdown("<div style='text-align: center; font-size: 0.8rem; color: #58a6ff;'>Z = (X1) + (X2)</div>", unsafe_allow_html=True)

st.write("---")

with st.container():
    st.subheader("📏 القيود")
    num_c = st.selectbox("عدد القيود المتاحة:", [2, 3, 4], index=1)
    
    constraints_list = []
    for i in range(num_c):
        st.markdown(f"**القيد {i+1}**")
        v1_c, v2_c, op_c, rhs_c = st.columns([1, 1, 0.8, 1.2])
        with v1_c: v1 = st.number_input(f"v1_{i}", value=1.0, key=f"v1_{i}", label_visibility="collapsed")
        with v2_c: v2 = st.number_input(f"v2_{i}", value=1.0, key=f"v2_{i}", label_visibility="collapsed")
        with op_c: op = st.selectbox(f"op_{i}", ["<=", ">=", "="], key=f"op_{i}", label_visibility="collapsed")
        with rhs_c: rhs = st.number_input(f"rhs_{i}", value=10.0, key=f"rhs_{i}", label_visibility="collapsed")
        constraints_list.append(([v1, v2], op, rhs, i + 1))

st.write("")
run_btn = st.button("تحليل المسألة")

if run_btn:
    try:
        report = "--- التحليل الرياضي المفصل ---\n\n"
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints_list):
            corner_points.append((0,0))

        # حساب التقاطعات
        for coeffs, op, rhs, idx in constraints_list:
            if coeffs[0] != 0:
                p = (rhs/coeffs[0], 0)
                if HusseinSolver.is_feasible(p, constraints_list): corner_points.append(p)
            if coeffs[1] != 0:
                p = (0, rhs/coeffs[1])
                if HusseinSolver.is_feasible(p, constraints_list): corner_points.append(p)

        report += "STEP: Calculating Intersections...\n"
        for i in range(len(constraints_list)):
            for j in range(i+1, len(constraints_list)):
                pt, info = HusseinSolver.solve_with_steps(constraints_list[i], constraints_list[j], constraints_list)
                if pt:
                    corner_points.append(pt)
                    report += info

        unique_corners = []
        seen = set()
        for p in corner_points:
            rnd = (round(p[0], 4), round(p[1], 4))
            if rnd not in seen:
                seen.add(rnd)
                z_val = z1*p[0] + z2*p[1]
                unique_corners.append((p, z_val))

        if not unique_corners:
            st.error("Infeasible Region!")
        else:
            best = max(unique_corners, key=lambda x: x[1]) if obj_type == "Max" else min(unique_corners, key=lambda x: x[1])

            # العرض البياني
            fig, ax = plt.subplots(figsize=(6, 5))
            fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#161b22')
            
            limit = max([p[0] for p in corner_points] + [p[1] for p in corner_points]) * 1.3
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

            ax.scatter(best[0][0], best[0][1], color='#ff0055', s=150, zorder=5)
            ax.set_xlim(0, limit); ax.set_ylim(0, limit)
            ax.tick_params(colors='#8b949e', labelsize=8); ax.grid(color='#30363d', alpha=0.3)
            st.pyplot(fig)
            
            # عرض المتركس (Cards)
            st.write("---")
            st.subheader("🏁 النتيجة")
            m1, m2, m3 = st.columns(3)
            m1.metric("Optimal Z", f"{best[1]:.2f}")
            m2.metric("Value X1", f"{best[0][0]:.2f}")
            m3.metric("Value X2", f"{best[0][1]:.2f}")

        st.subheader("📄 الخطوات الرياضية")
        st.markdown(f'<div class="steps-card">{report}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
