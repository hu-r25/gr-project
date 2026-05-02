import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_page_config(
    page_title="import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_page_config(
    page_title="import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_page_config(
    page_title="Graphical Method",
    page_icon="📱",
    layout="wide"
)

# تصميم مخصص لمحاكاة واجهة التطبيقات الاحترافية وتنسيق تقرير الحل
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* إخفاء أزرار الزائد والناقص نهائياً لجعل الخانة صافية */
    button.step-up, button.step-down { display: none !important; }
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    input[type=number] { -moz-appearance: textfield; }

    /* تنسيق الخانات الرقمية */
    .stNumberInput div div input { 
        background-color: #161b22 !important; 
        color: #58a6ff !important; 
        border: 1px solid #30363d !important;
        font-size: 18px !important;
        height: 45px !important;
        text-align: center;
        border-radius: 8px !important;
    }
    
    /* تنسيق حاوية الحل المفصل لضمان ظهور الأسطر والترتيب العمودي */
    .steps-container { 
        background-color: #010409; 
        padding: 25px; 
        border-radius: 12px; 
        border: 1px solid #30363d; 
        font-family: 'Consolas', 'Monaco', monospace; 
        color: #c9d1d9; 
        line-height: 1.7;
        white-space: pre; /* للحفاظ على تنسيق الأسطر والمسافات */
        overflow-x: auto;
        font-size: 14px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #1f6feb 0%, #58a6ff 100%);
        color: white; font-weight: bold; border: none; width: 100%; 
        height: 50px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك الرياضي (المنطق البرمجي) ---
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
            res += f" (1) {a1}X1 + {b1}X2 = {r1}\n"
            res += f" (2) {a2}X1 + {b2}X2 = {r2}\n"
            res += f" => Result: Feasible Corner at ({x:.2f}, {y:.2f})\n\n"
            return (x, y), res
        return None, ""

# --- 3. واجهة الإدخال ---
st.title("🛡️ Hussein Solver Pro")
st.write("نظام التحليل الرياضي المفصل (بدون أزرار تحكم جانبية)")

with st.container():
    st.subheader("🎯 دالة الهدف")
    t_col, c1_col, c2_col = st.columns([1, 1, 1])
    with t_col: obj_type = st.selectbox("النوع", ["Max", "Min"], label_visibility="collapsed")
    with c1_col: z1 = st.number_input("Z1", value=3.0, label_visibility="collapsed")
    with c2_col: z2 = st.number_input("Z2", value=5.0, label_visibility="collapsed")

st.write("---")

with st.container():
    st.subheader("📏 القيود (Constraints)")
    num_c = st.selectbox("حدد عدد القيود:", [2, 3, 4], index=1)
    
    constraints_list = []
    for i in range(num_c):
        st.write(f"القيد L{i+1}:")
        v1_c, v2_c, op_c, rhs_c = st.columns([1, 1, 0.8, 1.2])
        with v1_c: v1 = st.number_input(f"v1_{i}", value=1.0, key=f"v1_{i}", label_visibility="collapsed")
        with v2_c: v2 = st.number_input(f"v2_{i}", value=1.0, key=f"v2_{i}", label_visibility="collapsed")
        with op_c: op = st.selectbox(f"op_{i}", ["<=", ">=", "="], key=f"op_{i}", label_visibility="collapsed")
        with rhs_c: rhs = st.number_input(f"rhs_{i}", value=10.0, key=f"rhs_{i}", label_visibility="collapsed")
        constraints_list.append(([v1, v2], op, rhs, i + 1))

run_btn = st.button("بدأ التحليل الرياضي الشامل")

if run_btn:
    try:
        # --- توليد تقرير الحل المفصل (تطابق كامل مع طلبك) ---
        report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
        report += "STEP 1: AXIS INTERCEPTS (SUBSTITUTION MATH)\n"
        
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints_list):
            corner_points.append((0,0))
            report += " - Origin Point Check: (0,0) is Feasible\n"

        for coeffs, op, rhs, idx in constraints_list:
            report += f"\nConstraint L{idx}: {coeffs[0]}X1 + {coeffs[1]}X2 = {rhs}\n"
            
            # Let X2 = 0
            if coeffs[0] != 0:
                p = (rhs/coeffs[0], 0)
                report += f" - Let X2 = 0: {coeffs[0]}X1 + {coeffs[1]}(0) = {rhs}\n"
                report += f"   => {coeffs[0]}X1 = {rhs} -> X1 = {p[0]:.2f}. Point: ({p[0]:.2f}, 0)\n"
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += "   [Status: Feasible Corner Point]\n"
                else:
                    report += "   [Status: Discarded - Outside Area]\n"
            
            # Let X1 = 0
            if coeffs[1] != 0:
                p = (0, rhs/coeffs[1])
                report += f" - Let X1 = 0: {coeffs[0]}(0) + {coeffs[1]}X2 = {rhs}\n"
                report += f"   => {coeffs[1]}X2 = {rhs} -> X2 = {p[1]:.2f}. Point: (0, {p[1]:.2f})\n"
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += "   [Status: Feasible Corner Point]\n"
                else:
                    report += "   [Status: Discarded - Outside Area]\n"

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
                report += f" Evaluating ({p[0]:.2f}, {p[1]:.2f}) -> Z = {z_val:.2f}\n"

        best = max(unique_corners, key=lambda x: x[1]) if obj_type == "Max" else min(unique_corners, key=lambda x: x[1])
        report += f"\n>>> FINAL OPTIMAL SOLUTION <<<\nZ = {best[1]:.2f} at X1={best[0][0]:.2f}, X2={best[0][1]:.2f}"

        # --- عرض الرسم البياني والنتائج ---
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#161b22')
        
        all_coords = [p[0] for p in corner_points] + [p[1] for p in corner_points]
        limit = max(all_coords) * 1.3 if all_coords else 10
        x_ax = np.linspace(0, limit, 400)
        
        for (coeffs, op, rhs, idx) in constraints_list:
            if coeffs[1] != 0: ax.plot(x_ax, (rhs - coeffs[0]*x_ax)/coeffs[1], label=f"L{idx}", lw=2)
            else: ax.axvline(x=rhs/coeffs[0], color="orange", lw=2, label=f"L{idx}")

        if len(unique_corners) >= 3:
            pts_array = np.array([u[0] for u in unique_corners])
            center = np.mean(pts_array, axis=0)
            angles = np.arctan2(pts_array[:,1]-center[1], pts_array[:,0]-center[0])
            pts_array = pts_array[np.argsort(angles)]
            ax.fill(pts_array[:,0], pts_array[:,1], color="#58a6ff", alpha=0.3)

        ax.scatter(best[0][0], best[0][1], color='red', s=150, zorder=5)
        ax.set_xlim(0, limit); ax.set_ylim(0, limit)
        ax.tick_params(colors='#8b949e'); ax.grid(color='#30363d', alpha=0.3)
        st.pyplot(fig)
        
        # عرض بطاقات النتائج
        st.write("---")
        m1, m2, m3 = st.columns(3)
        m1.metric(f"Optimal {obj_type}", f"{best[1]:.2f}")
        m2.metric("Value X1", f"{best[0][0]:.2f}")
        m3.metric("Value X2", f"{best[0][1]:.2f}")

        # عرض التقرير الرياضي المفصل (الذي طلبته)
        st.subheader("📄 تقرير التحليل الرياضي المفصل")
        st.markdown(f'<div class="steps-container">{report}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"حدث خطأ: {e}")",
    page_icon="📱",
    layout="wide"
)

# تصميم مخصص لمحاكاة واجهة التطبيقات الاحترافية وتنسيق تقرير الحل
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* إخفاء أزرار الزائد والناقص نهائياً لجعل الخانة صافية */
    button.step-up, button.step-down { display: none !important; }
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    input[type=number] { -moz-appearance: textfield; }

    /* تنسيق الخانات الرقمية */
    .stNumberInput div div input { 
        background-color: #161b22 !important; 
        color: #58a6ff !important; 
        border: 1px solid #30363d !important;
        font-size: 18px !important;
        height: 45px !important;
        text-align: center;
        border-radius: 8px !important;
    }
    
    /* تنسيق حاوية الحل المفصل لضمان ظهور الأسطر والترتيب العمودي */
    .steps-container { 
        background-color: #010409; 
        padding: 25px; 
        border-radius: 12px; 
        border: 1px solid #30363d; 
        font-family: 'Consolas', 'Monaco', monospace; 
        color: #c9d1d9; 
        line-height: 1.7;
        white-space: pre; /* للحفاظ على تنسيق الأسطر والمسافات */
        overflow-x: auto;
        font-size: 14px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #1f6feb 0%, #58a6ff 100%);
        color: white; font-weight: bold; border: none; width: 100%; 
        height: 50px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك الرياضي (المنطق البرمجي) ---
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
            res += f" (1) {a1}X1 + {b1}X2 = {r1}\n"
            res += f" (2) {a2}X1 + {b2}X2 = {r2}\n"
            res += f" => Result: Feasible Corner at ({x:.2f}, {y:.2f})\n\n"
            return (x, y), res
        return None, ""

# --- 3. واجهة الإدخال ---
st.title("Graphical")
st.write("by hussein")

with st.container():
    st.subheader("🎯 دالة الهدف")
    t_col, c1_col, c2_col = st.columns([1, 1, 1])
    with t_col: obj_type = st.selectbox("النوع", ["Max", "Min"], label_visibility="collapsed")
    with c1_col: z1 = st.number_input("Z1", value=3.0, label_visibility="collapsed")
    with c2_col: z2 = st.number_input("Z2", value=5.0, label_visibility="collapsed")

st.write("---")

with st.container():
    st.subheader("📏 القيود (Constraints)")
    num_c = st.selectbox("حدد عدد القيود:", [2, 3, 4], index=1)
    
    constraints_list = []
    for i in range(num_c):
        st.write(f"القيد L{i+1}:")
        v1_c, v2_c, op_c, rhs_c = st.columns([1, 1, 0.8, 1.2])
        with v1_c: v1 = st.number_input(f"v1_{i}", value=1.0, key=f"v1_{i}", label_visibility="collapsed")
        with v2_c: v2 = st.number_input(f"v2_{i}", value=1.0, key=f"v2_{i}", label_visibility="collapsed")
        with op_c: op = st.selectbox(f"op_{i}", ["<=", ">=", "="], key=f"op_{i}", label_visibility="collapsed")
        with rhs_c: rhs = st.number_input(f"rhs_{i}", value=10.0, key=f"rhs_{i}", label_visibility="collapsed")
        constraints_list.append(([v1, v2], op, rhs, i + 1))

run_btn = st.button("بدأ التحليل الرياضي الشامل")

if run_btn:
    try:
        # --- توليد تقرير الحل المفصل (تطابق كامل مع طلبك) ---
        report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
        report += "STEP 1: AXIS INTERCEPTS (SUBSTITUTION MATH)\n"
        
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints_list):
            corner_points.append((0,0))
            report += " - Origin Point Check: (0,0) is Feasible\n"

        for coeffs, op, rhs, idx in constraints_list:
            report += f"\nConstraint L{idx}: {coeffs[0]}X1 + {coeffs[1]}X2 = {rhs}\n"
            
            # Let X2 = 0
            if coeffs[0] != 0:
                p = (rhs/coeffs[0], 0)
                report += f" - Let X2 = 0: {coeffs[0]}X1 + {coeffs[1]}(0) = {rhs}\n"
                report += f"   => {coeffs[0]}X1 = {rhs} -> X1 = {p[0]:.2f}. Point: ({p[0]:.2f}, 0)\n"
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += "   [Status: Feasible Corner Point]\n"
                else:
                    report += "   [Status: Discarded - Outside Area]\n"
            
            # Let X1 = 0
            if coeffs[1] != 0:
                p = (0, rhs/coeffs[1])
                report += f" - Let X1 = 0: {coeffs[0]}(0) + {coeffs[1]}X2 = {rhs}\n"
                report += f"   => {coeffs[1]}X2 = {rhs} -> X2 = {p[1]:.2f}. Point: (0, {p[1]:.2f})\n"
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += "   [Status: Feasible Corner Point]\n"
                else:
                    report += "   [Status: Discarded - Outside Area]\n"

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
                report += f" Evaluating ({p[0]:.2f}, {p[1]:.2f}) -> Z = {z_val:.2f}\n"

        best = max(unique_corners, key=lambda x: x[1]) if obj_type == "Max" else min(unique_corners, key=lambda x: x[1])
        report += f"\n>>> FINAL OPTIMAL SOLUTION <<<\nZ = {best[1]:.2f} at X1={best[0][0]:.2f}, X2={best[0][1]:.2f}"

        # --- عرض الرسم البياني والنتائج ---
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#161b22')
        
        all_coords = [p[0] for p in corner_points] + [p[1] for p in corner_points]
        limit = max(all_coords) * 1.3 if all_coords else 10
        x_ax = np.linspace(0, limit, 400)
        
        for (coeffs, op, rhs, idx) in constraints_list:
            if coeffs[1] != 0: ax.plot(x_ax, (rhs - coeffs[0]*x_ax)/coeffs[1], label=f"L{idx}", lw=2)
            else: ax.axvline(x=rhs/coeffs[0], color="orange", lw=2, label=f"L{idx}")

        if len(unique_corners) >= 3:
            pts_array = np.array([u[0] for u in unique_corners])
            center = np.mean(pts_array, axis=0)
            angles = np.arctan2(pts_array[:,1]-center[1], pts_array[:,0]-center[0])
            pts_array = pts_array[np.argsort(angles)]
            ax.fill(pts_array[:,0], pts_array[:,1], color="#58a6ff", alpha=0.3)

        ax.scatter(best[0][0], best[0][1], color='red', s=150, zorder=5)
        ax.set_xlim(0, limit); ax.set_ylim(0, limit)
        ax.tick_params(colors='#8b949e'); ax.grid(color='#30363d', alpha=0.3)
        st.pyplot(fig)
        
        # عرض بطاقات النتائج
        st.write("---")
        m1, m2, m3 = st.columns(3)
        m1.metric(f"Optimal {obj_type}", f"{best[1]:.2f}")
        m2.metric("Value X1", f"{best[0][0]:.2f}")
        m3.metric("Value X2", f"{best[0][1]:.2f}")

        # عرض التقرير الرياضي المفصل (الذي طلبته)
        st.subheader("📄 تقرير التحليل الرياضي المفصل")
        st.markdown(f'<div class="steps-container">{report}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"حدث خطأ: {e}")r",
    page_icon="📱",
    layout="wide"
)

# تصميم مخصص لمحاكاة واجهة التطبيقات الاحترافية وتنسيق تقرير الحل
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* إخفاء أزرار الزائد والناقص نهائياً لجعل الخانة صافية */
    button.step-up, button.step-down { display: none !important; }
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    input[type=number] { -moz-appearance: textfield; }

    /* تنسيق الخانات الرقمية */
    .stNumberInput div div input { 
        background-color: #161b22 !important; 
        color: #58a6ff !important; 
        border: 1px solid #30363d !important;
        font-size: 18px !important;
        height: 45px !important;
        text-align: center;
        border-radius: 8px !important;
    }
    
    /* تنسيق حاوية الحل المفصل لضمان ظهور الأسطر والترتيب العمودي */
    .steps-container { 
        background-color: #010409; 
        padding: 25px; 
        border-radius: 12px; 
        border: 1px solid #30363d; 
        font-family: 'Consolas', 'Monaco', monospace; 
        color: #c9d1d9; 
        line-height: 1.7;
        white-space: pre; /* للحفاظ على تنسيق الأسطر والمسافات */
        overflow-x: auto;
        font-size: 14px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #1f6feb 0%, #58a6ff 100%);
        color: white; font-weight: bold; border: none; width: 100%; 
        height: 50px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك الرياضي (المنطق البرمجي) ---
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
            res += f" (1) {a1}X1 + {b1}X2 = {r1}\n"
            res += f" (2) {a2}X1 + {b2}X2 = {r2}\n"
            res += f" => Result: Feasible Corner at ({x:.2f}, {y:.2f})\n\n"
            return (x, y), res
        return None, ""

# --- 3. واجهة الإدخال ---
st.title(" Solver Pro")
st.write("by hussein")

with st.container():
    st.subheader("🎯 دالة الهدف")
    t_col, c1_col, c2_col = st.columns([1, 1, 1])
    with t_col: obj_type = st.selectbox("النوع", ["Max", "Min"], label_visibility="collapsed")
    with c1_col: z1 = st.number_input("Z1", value=3.0, label_visibility="collapsed")
    with c2_col: z2 = st.number_input("Z2", value=5.0, label_visibility="collapsed")

st.write("---")

with st.container():
    st.subheader("📏 القيود (Constraints)")
    num_c = st.selectbox("حدد عدد القيود:", [2, 3, 4], index=1)
    
    constraints_list = []
    for i in range(num_c):
        st.write(f"القيد L{i+1}:")
        v1_c, v2_c, op_c, rhs_c = st.columns([1, 1, 0.8, 1.2])
        with v1_c: v1 = st.number_input(f"v1_{i}", value=1.0, key=f"v1_{i}", label_visibility="collapsed")
        with v2_c: v2 = st.number_input(f"v2_{i}", value=1.0, key=f"v2_{i}", label_visibility="collapsed")
        with op_c: op = st.selectbox(f"op_{i}", ["<=", ">=", "="], key=f"op_{i}", label_visibility="collapsed")
        with rhs_c: rhs = st.number_input(f"rhs_{i}", value=10.0, key=f"rhs_{i}", label_visibility="collapsed")
        constraints_list.append(([v1, v2], op, rhs, i + 1))

run_btn = st.button("بدأ التحليل الرياضي الشامل")

if run_btn:
    try:
        # --- توليد تقرير الحل المفصل (تطابق كامل مع طلبك) ---
        report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
        report += "STEP 1: AXIS INTERCEPTS (SUBSTITUTION MATH)\n"
        
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints_list):
            corner_points.append((0,0))
            report += " - Origin Point Check: (0,0) is Feasible\n"

        for coeffs, op, rhs, idx in constraints_list:
            report += f"\nConstraint L{idx}: {coeffs[0]}X1 + {coeffs[1]}X2 = {rhs}\n"
            
            # Let X2 = 0
            if coeffs[0] != 0:
                p = (rhs/coeffs[0], 0)
                report += f" - Let X2 = 0: {coeffs[0]}X1 + {coeffs[1]}(0) = {rhs}\n"
                report += f"   => {coeffs[0]}X1 = {rhs} -> X1 = {p[0]:.2f}. Point: ({p[0]:.2f}, 0)\n"
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += "   [Status: Feasible Corner Point]\n"
                else:
                    report += "   [Status: Discarded - Outside Area]\n"
            
            # Let X1 = 0
            if coeffs[1] != 0:
                p = (0, rhs/coeffs[1])
                report += f" - Let X1 = 0: {coeffs[0]}(0) + {coeffs[1]}X2 = {rhs}\n"
                report += f"   => {coeffs[1]}X2 = {rhs} -> X2 = {p[1]:.2f}. Point: (0, {p[1]:.2f})\n"
                if HusseinSolver.is_feasible(p, constraints_list):
                    corner_points.append(p)
                    report += "   [Status: Feasible Corner Point]\n"
                else:
                    report += "   [Status: Discarded - Outside Area]\n"

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
                report += f" Evaluating ({p[0]:.2f}, {p[1]:.2f}) -> Z = {z_val:.2f}\n"

        best = max(unique_corners, key=lambda x: x[1]) if obj_type == "Max" else min(unique_corners, key=lambda x: x[1])
        report += f"\n>>> FINAL OPTIMAL SOLUTION <<<\nZ = {best[1]:.2f} at X1={best[0][0]:.2f}, X2={best[0][1]:.2f}"

        # --- عرض الرسم البياني والنتائج ---
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor('#0d1117'); ax.set_facecolor('#161b22')
        
        all_coords = [p[0] for p in corner_points] + [p[1] for p in corner_points]
        limit = max(all_coords) * 1.3 if all_coords else 10
        x_ax = np.linspace(0, limit, 400)
        
        for (coeffs, op, rhs, idx) in constraints_list:
            if coeffs[1] != 0: ax.plot(x_ax, (rhs - coeffs[0]*x_ax)/coeffs[1], label=f"L{idx}", lw=2)
            else: ax.axvline(x=rhs/coeffs[0], color="orange", lw=2, label=f"L{idx}")

        if len(unique_corners) >= 3:
            pts_array = np.array([u[0] for u in unique_corners])
            center = np.mean(pts_array, axis=0)
            angles = np.arctan2(pts_array[:,1]-center[1], pts_array[:,0]-center[0])
            pts_array = pts_array[np.argsort(angles)]
            ax.fill(pts_array[:,0], pts_array[:,1], color="#58a6ff", alpha=0.3)

        ax.scatter(best[0][0], best[0][1], color='red', s=150, zorder=5)
        ax.set_xlim(0, limit); ax.set_ylim(0, limit)
        ax.tick_params(colors='#8b949e'); ax.grid(color='#30363d', alpha=0.3)
        st.pyplot(fig)
        
        # عرض بطاقات النتائج
        st.write("---")
        m1, m2, m3 = st.columns(3)
        m1.metric(f"Optimal {obj_type}", f"{best[1]:.2f}")
        m2.metric("Value X1", f"{best[0][0]:.2f}")
        m3.metric("Value X2", f"{best[0][1]:.2f}")

        # عرض التقرير الرياضي المفصل (الذي طلبته)
        st.subheader("📄 تقرير التحليل الرياضي المفصل")
        st.markdown(f'<div class="steps-container">{report}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"حدث خطأ: {e}")
