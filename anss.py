import streamlit as st
import re
import matplotlib.pyplot as plt
import numpy as np

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Graphical Method Solver - Hussein", layout="wide")

# --- تنسيق CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0f0f0f; color: #e0e0e0; }
    .stButton>button { width: 100%; background: #00d1ff; color: black; font-weight: bold; border-radius: 8px; }
    .steps-container { 
        background-color: #1a1a1a; 
        padding: 25px; 
        border-radius: 10px; 
        border: 1px solid #333; 
        font-family: 'Consolas', 'Courier New', monospace; 
        white-space: pre-wrap;
        line-height: 1.5;
        color: #f0f0f0;
    }
    .metric-card { background: #252526; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; }
    h4 { color: #00d1ff !important; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

class HusseinSolver:
    @staticmethod
    def is_feasible(p, constraints):
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

st.title("📊 Graphical Method Reasoning System")
st.write("Developed by **Hussein**")

col_in, col_graph = st.columns([1, 1.2], gap="large")

with col_in:
    st.subheader("📥 مدخلات المسألة")
    input_text = st.text_area("Objective & Constraints:", 
                             value="Max Z = 3X1 + 5X2\n2X1 + 1X2 <= 8\n1X1 + 2X2 <= 10\n1X1 + 0X2 <= 3", 
                             height=200)
    analyze_btn = st.button("START MATHEMATICAL ANALYSIS")

if analyze_btn:
    try:
        raw = input_text.strip().lower().replace(" ", "")
        lines = [l for l in raw.split('\n') if l]
        mode = "max" if "max" in lines[0] else "min"
        obj_m = re.findall(r'([-+]?\d*\.?\d*)x(\d+)', lines[0])
        obj_c = [0.0, 0.0]
        for v, i in obj_m:
            idx = int(i)-1
            if idx < 2: obj_c[idx] = float(v) if v not in ["", "+", "-"] else float(v + "1")
        
        constraints = []
        for idx, l in enumerate(lines[1:]):
            op = "<=" if "<=" in l else (">=" if ">=" in l else "=")
            lhs, rhs = l.split(op)
            m = re.findall(r'([-+]?\d*\.?\d*)x(\d+)', lhs)
            row = [0.0, 0.0]
            for v, i in m:
                c_idx = int(i)-1
                if c_idx < 2: row[c_idx] = float(v) if v not in ["", "+", "-"] else float(v + "1")
            constraints.append((row, op, float(rhs), idx + 1))

        # --- توليد تقرير الخطوات (مثل الصورة تماماً) ---
        report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
        report += "STEP 1: AXIS INTERCEPTS (SUBSTITUTION MATH)\n"
        
        corner_points = []
        if HusseinSolver.is_feasible((0,0), constraints):
            corner_points.append((0,0))
            report += " - Origin Point Check: (0,0) is Feasible\n"

        for row, op, rhs, idx in constraints:
            report += f"\nConstraint L{idx}: {row[0]}X1 + {row[1]}X2 = {rhs}\n"
            # Let X2 = 0
            if row[0] != 0:
                val = rhs/row[0]
                report += f" - Let X2 = 0: {row[0]}X1 + {row[1]}(0) = {rhs}\n"
                report += f"   => {row[0]}X1 = {rhs} -> X1 = {val:.2f}. Point: ({val:.2f}, 0)\n"
                if HusseinSolver.is_feasible((val, 0), constraints):
                    corner_points.append((val, 0))
                    report += "   [Status: Feasible Corner Point]\n"
                else: report += "   [Status: Discarded - Outside Area]\n"
            
            # Let X1 = 0
            if row[1] != 0:
                val = rhs/row[1]
                report += f" - Let X1 = 0: {row[0]}(0) + {row[1]}X2 = {rhs}\n"
                report += f"   => {row[1]}X2 = {rhs} -> X2 = {val:.2f}. Point: (0, {val:.2f})\n"
                if HusseinSolver.is_feasible((0, val), constraints):
                    corner_points.append((0, val))
                    report += "   [Status: Feasible Corner Point]\n"
                else: report += "   [Status: Discarded - Outside Area]\n"

        report += "\n" + "="*45 + "\nSTEP 2: LINE INTERSECTIONS (ELIMINATION)\n"
        for i in range(len(constraints)):
            for j in range(i+1, len(constraints)):
                pt, info = HusseinSolver.solve_intersection(constraints[i], constraints[j], constraints)
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
                z = obj_c[0]*p[0] + obj_c[1]*p[1]
                unique_corners.append((p, z))
                report += f" Evaluating ({p[0]:.2f}, {p[1]:.2f}) -> Z = {z:.2f}\n"

        best = max(unique_corners, key=lambda x: x[1]) if mode == "max" else min(unique_corners, key=lambda x: x[1])
        report += f"\n>>> OPTIMAL SOLUTION <<<\nZ = {best[1]:.2f} at X1={best[0][0]:.2f}, X2={best[0][1]:.2f}"

        # --- الرسم البياني ---
        with col_graph:
            st.subheader("📊 Visualization")
            fig, ax = plt.subplots(figsize=(8, 8))
            fig.patch.set_facecolor('#0f0f0f'); ax.set_facecolor('#1a1a1a')
            
            all_pts = [p[0] for p in corner_points] + [p[1] for p in corner_points]
            limit = max(all_pts) * 1.3 if all_pts else 10
            x = np.linspace(0, limit, 400)
            
            for r, o, rhs, idx in constraints:
                if r[1] != 0: ax.plot(x, (rhs - r[0]*x)/r[1], label=f"L{idx}")
                else: ax.axvline(x=rhs/r[0], label=f"L{idx}", color="orange")

            if len(unique_corners) >= 3:
                pts = np.array([u[0] for u in unique_corners])
                center = np.mean(pts, axis=0)
                angles = np.arctan2(pts[:,1]-center[1], pts[:,0]-center[0])
                pts = pts[np.argsort(angles)]
                ax.fill(pts[:,0], pts[:,1], color="#00d1ff", alpha=0.3)

            ax.scatter(best[0][0], best[0][1], color='red', s=200, zorder=5)
            ax.set_xlim(0, limit); ax.set_ylim(0, limit)
            ax.tick_params(colors='white'); ax.grid(alpha=0.2)
            ax.legend()
            st.pyplot(fig)

        # عرض التقرير المفصل مثل الصورة
        st.markdown("### 📝 Detailed Mathematical Analysis")
        st.markdown(f'<div class="steps-container">{report}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
