import streamlit as st
import re
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Graphical Method Solver - Hussein", layout="wide")

# --- 2. تصميم الواجهة (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0f0f0f; color: #e0e0e0; }
    .stButton>button { width: 100%; background: #00d1ff; color: black; font-weight: bold; border-radius: 8px; }
    .report-box { background-color: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 5px solid #00d1ff; font-family: 'Courier New', monospace; }
    .metric-card { background: #252526; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. المحرك الرياضي وحل القيود ---
class HusseinSolver:
    @staticmethod
    def is_feasible(p, constraints):
        """التحقق مما إذا كانت النقطة تحقق جميع القيود"""
        x1, x2 = p
        if x1 < -1e-7 or x2 < -1e-7: return False
        for row, op, rhs, _ in constraints:
            val = row[0]*x1 + row[1]*x2
            if op == "<=" and val > rhs + 1e-7: return False
            if op == ">=" and val < rhs - 1e-7: return False
            if op == "=" and abs(val - rhs) > 1e-7: return False
        return True

    @staticmethod
    def solve_intersection(c1, c2, constraints):
        """حل معادلتين لإيجاد نقطة التقاطع"""
        a1, b1 = c1[0]; r1 = c1[2]
        a2, b2 = c2[0]; r2 = c2[2]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9: return None # الخطوط متوازية
        
        x = (r1 * b2 - r2 * b1) / det
        y = (a1 * r2 - a2 * r1) / det
        
        if HusseinSolver.is_feasible((x, y), constraints):
            return (x, y)
        return None

# --- 4. واجهة المستخدم ---
st.title("📊 Graphical Method Reasoning System")
st.markdown("Developed by **Hussein** | الحل الأمثل بطريقة الرسم البياني")

col_in, col_graph = st.columns([1, 1.2], gap="large")

with col_in:
    st.subheader("📥 مدخلات المسألة")
    input_text = st.text_area("أدخل دالة الهدف والقيود:", 
                             value="Max Z = 3X1 + 5X2\n2X1 + 1X2 <= 8\n1X1 + 2X2 <= 10\n1X1 + 0X2 <= 3", 
                             height=200)
    analyze_btn = st.button("بدأ التحليل الرياضي")

if analyze_btn:
    try:
        # --- تحليل النص (Parsing) ---
        raw = input_text.strip().lower().replace(" ", "")
        lines = [l for l in raw.split('\n') if l]
        mode = "max" if "max" in lines[0] else "min"
        
        # استخراج دالة الهدف
        obj_m = re.findall(r'([-+]?\d*\.?\d*)x(\d+)', lines[0])
        obj_c = [0.0, 0.0]
        for v, i in obj_m:
            idx = int(i)-1
            if idx < 2: obj_c[idx] = float(v) if v not in ["", "+", "-"] else float(v + "1")
        
        # استخراج القيود
        constraints = []
        steps_log = ""
        for idx, l in enumerate(lines[1:]):
            op = "<=" if "<=" in l else (">=" if ">=" in l else "=")
            lhs, rhs = l.split(op)
            m = re.findall(r'([-+]?\d*\.?\d*)x(\d+)', lhs)
            row = [0.0, 0.0]
            for v, i in m:
                c_idx = int(i)-1
                if c_idx < 2: row[c_idx] = float(v) if v not in ["", "+", "-"] else float(v + "1")
            constraints.append((row, op, float(rhs), idx + 1))

        # --- إيجاد النقاط الركنية (Corner Points) ---
        corner_points = []
        steps_log += "1. Checking intercepts with axes...\n"
        
        # نقطة الأصل
        if HusseinSolver.is_feasible((0,0), constraints):
            corner_points.append((0,0))

        # تقاطع القيود مع المحاور
        for r, o, rhs, idx in constraints:
            if r[0] != 0: # التقاطع مع X1
                p = (rhs/r[0], 0)
                if HusseinSolver.is_feasible(p, constraints): corner_points.append(p)
            if r[1] != 0: # التقاطع مع X2
                p = (0, rhs/r[1])
                if HusseinSolver.is_feasible(p, constraints): corner_points.append(p)

        # تقاطع القيود مع بعضها البعض
        steps_log += "2. Solving intersections between constraints...\n"
        for i in range(len(constraints)):
            for j in range(i+1, len(constraints)):
                pt = HusseinSolver.solve_intersection(constraints[i], constraints[j], constraints)
                if pt:
                    corner_points.append(pt)
                    steps_log += f"   - Intersection found between L{constraints[i][3]} & L{constraints[j][3]}\n"

        # تصفية النقاط المكررة وحساب Z
        unique_results = []
        seen = set()
        for p in corner_points:
            p_rnd = (round(p[0], 4), round(p[1], 4))
            if p_rnd not in seen:
                seen.add(p_rnd)
                z_val = obj_c[0]*p[0] + obj_c[1]*p[1]
                unique_results.append((p, z_val))

        # الحل الأمثل
        best = max(unique_results, key=lambda x: x[1]) if mode == "max" else min(unique_results, key=lambda x: x[1])

        # --- الرسم البياني ---
        with col_graph:
            st.subheader("📊 الرسم البياني ومنطقة الحل")
            fig, ax = plt.subplots(figsize=(8, 8))
            fig.patch.set_facecolor('#0f0f0f')
            ax.set_facecolor('#1a1a1a')
            
            # تحديد حدود الرسم
            all_coords = [p[0] for p in corner_points] + [p[1] for p in corner_points]
            limit = max(all_coords) * 1.3 if all_coords else 10
            x_vals = np.linspace(0, limit, 400)
            
            # رسم الخطوط
            for r, o, rhs, idx in constraints:
                if r[1] != 0:
                    ax.plot(x_vals, (rhs - r[0]*x_vals)/r[1], label=f"L{idx}", lw=2)
                else:
                    ax.axvline(x=rhs/r[0], label=f"L{idx}", color="orange", lw=2)

            # تظليل منطقة الحل (Feasible Region)
            if len(unique_results) >= 3:
                poly_pts = np.array([r[0] for r in unique_results])
                center = np.mean(poly_pts, axis=0)
                angles = np.arctan2(poly_pts[:,1]-center[1], poly_pts[:,0]-center[0])
                poly_pts = poly_pts[np.argsort(angles)]
                ax.fill(poly_pts[:,0], poly_pts[:,1], color="#00d1ff", alpha=0.3, label="Feasible Region")

            ax.scatter(best[0][0], best[0][1], color='red', s=200, zorder=5, label="Optimal Point")
            ax.set_xlim(0, limit); ax.set_ylim(0, limit)
            ax.tick_params(colors='white')
            ax.grid(color='#333', alpha=0.5)
            ax.legend()
            st.pyplot(fig)

        # --- النتائج النهائية ---
        st.markdown("---")
        st.subheader("🏁 النتائج النهائية")
        r1, r2, r3 = st.columns(3)
        r1.markdown(f'<div class="metric-card"><h4>Optimal Z</h4><h2>{best[1]:.2f}</h2></div>', unsafe_allow_html=True)
        r2.markdown(f'<div class="metric-card"><h4>X1 Value</h4><h2>{best[0][0]:.2f}</h2></div>', unsafe_allow_html=True)
        r3.markdown(f'<div class="metric-card"><h4>X2 Value</h4><h2>{best[0][1]:.2f}</h2></div>', unsafe_allow_html=True)

        with st.expander("Show Mathematical Reasoning Steps"):
            st.markdown(f'<div class="report-box">{steps_log}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"خطأ في إدخال البيانات: تأكد من كتابة المسألة بشكل صحيح. التفاصيل: {e}")
