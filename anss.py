import tkinter as tk
from tkinter import messagebox, scrolledtext
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- الإعدادات البصرية ---
BG_COLOR = "#0f0f0f"
SIDE_COLOR = "#1a1a1a"
ACCENT_COLOR = "#00d1ff"
TEXT_COLOR = "#e0e0e0"

class HusseinGraphicalPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphical Method - mhm")
        self.root.geometry("1400x900")
        self.root.configure(bg=BG_COLOR)
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=SIDE_COLOR, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="GRAPHICAL METHOD REASONING SYSTEM", font=("Segoe UI", 16, "bold"), 
                 fg=ACCENT_COLOR, bg=SIDE_COLOR).pack(pady=15)

        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # مدخلات المسألة
        input_frame = tk.LabelFrame(main_frame, text=" 1. LP Problem Input ", 
                                    font=("Arial", 11, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
        input_frame.pack(fill=tk.X, pady=10)

        self.txt_input = scrolledtext.ScrolledText(input_frame, height=5, font=("Consolas", 13), 
                                                   bg="#222", fg="#00ff00")
        self.txt_input.pack(fill=tk.X, padx=10, pady=10)
        self.txt_input.insert(tk.END, "Max Z = 3X1 + 5X2\n2X1 + 1X2 <= 8\n1X1 + 2X2 <= 10\n1X1 + 0X2 <= 3")

        tk.Button(input_frame, text="START MATHEMATICAL ANALYSIS", font=("Arial", 12, "bold"),
                  bg=ACCENT_COLOR, fg="black", command=self.process_lp).pack(pady=10)

        # النتائج والرسم
        display_frame = tk.Frame(main_frame, bg=BG_COLOR)
        display_frame.pack(fill=tk.BOTH, expand=True)

        self.plot_container = tk.Frame(display_frame, bg="#252526", bd=1, relief=tk.SOLID)
        self.plot_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.step_box = scrolledtext.ScrolledText(display_frame, width=65, font=("Courier New", 11), 
                                                  bg=SIDE_COLOR, fg=TEXT_COLOR)
        self.step_box.pack(side=tk.RIGHT, fill=tk.BOTH)

    def is_feasible(self, p, constraints):
        x1, x2 = p
        if x1 < -1e-7 or x2 < -1e-7: return False
        for row, op, rhs, _ in constraints:
            val = row[0]*x1 + row[1]*x2
            if op == "<=" and val > rhs + 1e-7: return False
            if op == ">=" and val < rhs - 1e-7: return False
            if op == "=" and abs(val - rhs) > 1e-7: return False
        return True

    def solve_intersection(self, c1, c2, constraints):
        a1, b1 = c1[0]; r1 = c1[2]
        a2, b2 = c2[0]; r2 = c2[2]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9: return None, ""
        x = (r1 * b2 - r2 * b1) / det
        y = (a1 * r2 - a2 * r1) / det
        
        if self.is_feasible((x, y), constraints):
            steps = f"INTERSECTION L{c1[3]} & L{c2[3]} (Substitution):\n"
            steps += f"  (1) {a1}X1 + {b1}X2 = {r1}\n"
            steps += f"  (2) {a2}X1 + {b2}X2 = {r2}\n"
            steps += f"  => Result: Feasible Corner at ({x:.2f}, {y:.2f})\n\n"
            return (x, y), steps
        return None, ""

    def parse_lp(self):
        raw = self.txt_input.get("1.0", tk.END).strip().lower().replace(" ", "")
        lines = [l for l in raw.split('\n') if l]
        mode = "max" if "max" in lines[0] else "min"
        obj_m = re.findall(r'([-+]?\d*\.?\d*)x(\d+)', lines[0])
        obj_c = [0.0, 0.0]
        for v, i in obj_m: obj_c[int(i)-1] = float(v) if v not in ["", "+", "-"] else float(v + "1")
        constraints = []
        for idx, l in enumerate(lines[1:]):
            op = "<=" if "<=" in l else (">=" if ">=" in l else "=")
            lhs, rhs = l.split(op)
            m = re.findall(r'([-+]?\d*\.?\d*)x(\d+)', lhs)
            row = [0.0, 0.0]
            for v, i in m: row[int(i)-1] = float(v) if v not in ["", "+", "-"] else float(v + "1")
            constraints.append((row, op, float(rhs), idx + 1))
        return mode, obj_c, constraints

    def process_lp(self):
        try:
            mode, obj_c, constraints = self.parse_lp()
            self.step_box.delete('1.0', tk.END)
            report = "--- STEP-BY-STEP MATHEMATICAL ANALYSIS ---\n\n"
            
            # --- الخطوة الأولى: نقاط التقاطع مع المحاور بالتفصيل ---
            report += "STEP 1: AXIS INTERCEPTS (SUBSTITUTION MATH)\n"
            corner_points = []
            if self.is_feasible((0,0), constraints):
                corner_points.append((0,0))
                report += f"  - Origin Point Check: (0,0) is Feasible\n"

            for row, op, rhs, idx in constraints:
                report += f"\nConstraint L{idx}: {row[0]}X1 + {row[1]}X2 = {rhs}\n"
                
                # التقاطع مع محور X1
                if row[0] != 0:
                    val = rhs/row[0]
                    report += f"  - Let X2 = 0: {row[0]}X1 + {row[1]}(0) = {rhs}\n"
                    report += f"    => {row[0]}X1 = {rhs} -> X1 = {val:.2f}. Point: ({val:.2f}, 0)\n"
                    if self.is_feasible((val, 0), constraints):
                        corner_points.append((val, 0))
                        report += "    [Status: Feasible Corner Point]\n"
                    else:
                        report += "    [Status: Discarded - Outside Area]\n"
                
                # التقاطع مع محور X2
                if row[1] != 0:
                    val = rhs/row[1]
                    report += f"  - Let X1 = 0: {row[0]}(0) + {row[1]}X2 = {rhs}\n"
                    report += f"    => {row[1]}X2 = {rhs} -> X2 = {val:.2f}. Point: (0, {val:.2f})\n"
                    if self.is_feasible((0, val), constraints):
                        corner_points.append((0, val))
                        report += "    [Status: Feasible Corner Point]\n"
                    else:
                        report += "    [Status: Discarded - Outside Area]\n"
            
            # --- الخطوة الثانية: تقاطع المستقيمات ---
            report += "\n" + "="*45 + "\nSTEP 2: LINE INTERSECTIONS (ELIMINATION)\n"
            for i in range(len(constraints)):
                for j in range(i+1, len(constraints)):
                    pt, math_steps = self.solve_intersection(constraints[i], constraints[j], constraints)
                    if pt:
                        corner_points.append(pt)
                        report += math_steps
            
            # --- الخطوة الثالثة: اختبار النقاط الركنية ---
            report += "="*45 + "\nSTEP 3: CORNER POINT Z-EVALUATION\n"
            unique_corners = []
            seen = set()
            for p in corner_points:
                rnd = (round(p[0], 4), round(p[1], 4))
                if rnd not in seen:
                    seen.add(rnd)
                    z = obj_c[0]*p[0] + obj_c[1]*p[1]
                    unique_corners.append((p, z))
                    report += f"  Evaluating ({p[0]:.2f}, {p[1]:.2f}) -> Z = {z:.2f}\n"

            best = max(unique_corners, key=lambda x: x[1]) if mode == "max" else min(unique_corners, key=lambda x: x[1])
            report += f"\n>>> OPTIMAL SOLUTION <<<\nZ = {best[1]:.2f} at X1={best[0][0]:.2f}, X2={best[0][1]:.2f}"
            
            self.step_box.insert(tk.END, report)
            self.render_graph(constraints, [p[0] for p in unique_corners], best)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def render_graph(self, constraints, f_pts, best_pt):
        for w in self.plot_container.winfo_children(): w.destroy()
        fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
        fig.patch.set_facecolor('#252526'); ax.set_facecolor('#1e1e1e')
        
        max_v = max([c[2] for c in constraints]) + 2
        x = np.linspace(0, max_v, 400)
        
        colors = ['#ff8c00', '#00ff7f', '#ff00ff', '#1e90ff']
        for i, (coeffs, op, rhs, idx) in enumerate(constraints):
            if coeffs[1] != 0:
                y = (rhs - coeffs[0]*x) / coeffs[1]
                ax.plot(x, y, label=f"L{idx}", color=colors[i%4], lw=2)
            else: ax.axvline(x=rhs/coeffs[0], label=f"L{idx}", color=colors[i%4], lw=2)

        if len(f_pts) >= 3:
            pts = np.array(f_pts)
            center = np.mean(pts, axis=0)
            angles = np.arctan2(pts[:,1] - center[1], pts[:,0] - center[0])
            pts = pts[np.argsort(angles)]
            ax.fill(pts[:,0], pts[:,1], color=ACCENT_COLOR, alpha=0.3, label="Feasible Region")

        ax.plot(best_pt[0][0], best_pt[0][1], 'ro', markersize=12)
        ax.set_xlim(0, max_v); ax.set_ylim(0, max_v)
        ax.tick_params(colors='white'); ax.grid(color='#444', linestyle='--')
        ax.legend(facecolor='#333', labelcolor='white')
        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
        canvas.draw(); canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk(); HusseinGraphicalPro(root); root.mainloop()