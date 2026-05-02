import streamlit as st
import re
import matplotlib.pyplot as plt
import numpy as np

# --- 1. إعدادات الصفحة المتقدمة ---
st.set_page_config(
    page_title="Graphical Method Pro - Hussein",
    page_icon="📊",
    layout="wide"
)

# --- 2. تخصيص المظهر (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0f0f0f; color: #e0e0e0; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(45deg, #00d1ff, #008fb3); 
        color: black; 
        font-weight: bold; 
        border: none;
        padding: 10px;
        border-radius: 8px;
    }
    .stTextArea>div>div>textarea { 
        background-color: #1a1a1a; 
        color: #00ff00; 
        font-family: 'Consolas', monospace; 
        border: 1px solid #333;
    }
    .report-card { 
        background-color: #1e1e1e; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #00d1ff; 
        margin-top: 20px;
    }
    .metric-box {
        background-color: #252526;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. المحرك الرياضي (Mathematical Engine) ---
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
        if abs(det) < 1e-9: return None
        x = (r1 * b2 - r2 * b1) / det
        y = (a1 * r2 - a2 * r1) / det
        if HusseinSolver.is_feasible((x, y), constraints):
            return (x, y)
        return None

# --- 4. واجهة المستخدم (UI) ---
st.title("🚀 Graphical Method Reasoning System")
st.markdown("Developed by **Hussein** | Advanced LP Solver")
st.write("---")

col_in, col_graph = st.columns([1, 1.2], gap="large")

with col_in:
    st.subheader("📥 Input LP Problem")
    st.info("Example Format: Max Z = 3X1 + 5X2")
    input_text = st.text_area("Constraints & Objective:", 
                             value="Max Z = 3X1 + 5X2\n2X1 + 1X2 <= 8\n1X1 + 2X2 <= 10\n1X1 + 0X2 <= 3", 
                             height=250)
    analyze_btn = st.button("RUN MATHEMATICAL ANALYSIS")

if analyze_btn:
    try:
        # --- Parsing Logic ---
        raw = input_text.strip().lower().replace(" ", "")
        lines = [l for l in raw.split('\n') if l]
        mode = "max" if "max" in lines[0] else "min"
        obj_m = re.findall(r'([-+]?\d*\.?\d*)x(\d+)', lines[0])
        obj_c = [0.0, 0.0]
        for v, i in obj_m: 
            idx = int(i)-1
            if idx < 2:
                obj_c[idx] = float(v) if v not in ["", "+", "-"] else float(v + "1")
        
        constraints = []
        for idx, l in enumerate(lines[1:]):
            op = "<=" if "<=" in l else (">=" if ">=" in l else "=")
            lhs, rhs = l.split(op)
            m = re.findall(r'([-+]?\d*\.?\d*)x(\d+)', lhs)
            row = [0.0, 0.0]
            for v, i in m:
                c_idx = int(i)-1
                if c_idx < 2:
                    row[c_idx] = float(v) if v not in ["", "+", "-"] else float(v + "1")
            constraints.append((row, op, float(rhs), idx + 1))

        # --- Solve logic ---
        points = []
        if HusseinSolver.is_feasible((0,0), constraints): points.append((0,0))
        
        for r, o, rhs, idx in constraints:
            if r[0] != 0:
                p = (rhs/r[0], 0)
                if HusseinSolver.is_feasible(p, constraints): points.append(p)
            if r[1] != 0:
                p = (0, rhs/r[1])
                if HusseinSolver.is_feasible(p, constraints): points.append(p)
        
        for i in range(len(constraints)):
            for j in range(i+1, len(constraints)):
                pt = HusseinSolver.solve_intersection(constraints[i], constraints[j], constraints)
                if pt: points.append(pt)

        # Result filtering
        unique_results = []
        seen = set()
        for p in points:
            p_rnd = (round(p[0], 4), round(p[1], 4))
            if p_rnd not in seen:
                seen.add(p_rnd)
                unique_results.append((p, obj_c[0]*p[0] + obj_c[1]*p[1]))

        if not unique_results:
            st.error("No Feasible Region Found!")
        else:
            best = max(unique_results, key=lambda x: x[1]) if mode == "max" else min(unique_results, key=lambda x: x[1])

            # --- Visualization ---
            with col_graph:
                st.subheader("📊 Feasible Region Graph")
                fig, ax = plt.subplots(figsize=(8, 8))
                fig.patch.set_facecolor('#0f0f0f')
                ax.set_facecolor('#1a1a1a')
                
                # Dynamic scaling
                all_coords = [p[0] for p in points] + [p[1] for p in points]
                lim = max(all_coords) * 1.3 if all_coords else 10
                x_vals = np.linspace(0, lim, 400)
                
                # Plot lines
                colors = ['#ff8c00', '#00ff7f', '#ff00ff', '#1e90ff']
                for i, (r, o, rhs, idx) in enumerate(constraints):
                    color = colors[i % len(colors)]
                    if r[1] != 0:
                        ax.plot(x_vals, (rhs - r[0]*x_vals)/r[1], label=f"L{idx}", color=color, lw=2)
                    else:
                        ax.axvline(x=rhs/r[0], label=f"L{idx}", color=color, lw=2)

                # Fill region
                if len(unique_results) >= 3:
                    poly_pts = np.array([r[0] for r in unique_results])
                    center = np.mean(poly_pts, axis=0)
                    angles = np.arctan2(poly_pts[:,1]-center[1], poly_pts[:,0]-center[0])
                    poly_pts = poly_pts[np.argsort(angles)]
                    ax.fill(poly_pts[:,0], poly_pts[:,1], color="#00d1ff", alpha=0.3, label="Feasible Area")

                # Optimal point marker
                ax.scatter(best[0][0], best[0][1], color='red', s=250, edgecolors='white', zorder=5, label="Optimal Solution")
                
                ax.set_xlim(0, lim); ax.set_ylim(0, lim)
                ax.tick_params(colors='white', labelsize=10)
                ax.grid(color='#333', linestyle='--', alpha=0.5)
                ax.legend(facecolor='#1e1e1e', labelcolor='white')
                st.pyplot(fig)

            # --- Final Stats ---
            st.markdown("---")
            st.subheader("🏁 Optimization Results")
            res_c1, res_c2, res_c3 = st.columns(3)
            with res_c1:
                st.markdown(f'<div class="metric-box"><p style="color:#00d1ff;margin:0;">Optimal Value (Z)</p><h2>{best[1]:.2f}</h2></div>', unsafe_allow_html=True)
            with res_c2:
                st.markdown(f'<div class="metric-box"><p style="color:#00d1ff;margin:0;">X1 Value</p><h2>{best[0][0]:.2f}</h2></div>', unsafe_allow_html=True)
            with res_c3:
                st.markdown(f'<div class="metric-box"><p style="color:#00d1ff;margin:0;">X2 Value</p><h2>{best[0][1]:.2f}</h2></div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Input Error: Please ensure you follow the 'Max Z = AX1 + BX2' format.")
        st.info("Error details: " + str(e))
