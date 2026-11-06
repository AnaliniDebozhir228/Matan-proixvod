"""
Интерактивный визуализатор производных
Зависимости: numpy, sympy, matplotlib
Установка: python -m pip install -r requirements.txt
Запуск:    python derivative_visualizer.py
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

x = sp.symbols("x")
ALLOWED = {
    "x": x, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sqrt": sp.sqrt, "log": sp.log, "ln": sp.log,
    "exp": sp.exp, "abs": sp.Abs, "pi": sp.pi, "e": sp.E,
}

def parse_function(source: str):
    source = source.strip().replace("^", "**")
    if not source:
        raise ValueError("Введите формулу функции.")
    try:
        expr = sp.sympify(source, locals=ALLOWED, evaluate=True)
    except Exception as exc:
        raise ValueError("Не удалось разобрать формулу. Проверьте скобки и знаки.") from exc
    unknown_symbols = expr.free_symbols - {x}
    allowed_functions = {sp.sin, sp.cos, sp.tan, sp.asin, sp.acos, sp.atan,
                          sp.sqrt, sp.log, sp.exp, sp.Abs}
    unknown_functions = {
        node.func for node in sp.preorder_traversal(expr)
        if isinstance(node, sp.Function) and node.func not in allowed_functions
    }
    if unknown_symbols or unknown_functions or expr.has(sp.I, sp.zoo, sp.nan):
        raise ValueError("Разрешены только x, числа и стандартные функции: sin, cos, tan, sqrt, log, exp, abs.")
    return expr

class DerivativeVisualizer:
    def __init__(self, root):
        self.root = root
        root.title("Интерактивный визуализатор производных")
        root.geometry("1120x760")
        root.minsize(850, 600)
        self.expr = x**2
        self.derivative = sp.diff(self.expr, x)
        self.x0 = tk.DoubleVar(value=1.0)
        self.h = tk.DoubleVar(value=1.0)
        self.show_derivative = tk.BooleanVar(value=True)
        self.show_secant = tk.BooleanVar(value=True)
        self.show_tangent = tk.BooleanVar(value=True)
        self.formula = tk.StringVar(value="x^2")
        self.status = tk.StringVar(value="Готово")
        self._build_ui()
        self.redraw()

    def _build_ui(self):
        top = ttk.Frame(self.root, padding=(10, 10, 10, 4))
        top.pack(fill=tk.X)
        ttk.Label(top, text="Функция f(x) =", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        entry = ttk.Entry(top, textvariable=self.formula, width=34, font=("Consolas", 12))
        entry.pack(side=tk.LEFT, padx=7)
        entry.bind("<Return>", lambda _event: self.apply_function())
        ttk.Button(top, text="Построить", command=self.apply_function).pack(side=tk.LEFT)
        ttk.Label(top, text="Примеры: x^2, sin(x) + 0.5*x, e^(-x^2)",
                  foreground="#555").pack(side=tk.LEFT, padx=12)

        controls = ttk.Frame(self.root, padding=(10, 4))
        controls.pack(fill=tk.X)
        ttk.Label(controls, text="Точка x₀:").grid(row=0, column=0, sticky="w")
        self.x0_scale = ttk.Scale(controls, from_=-5, to=5, variable=self.x0,
                                  command=lambda _v: self.redraw())
        self.x0_scale.grid(row=0, column=1, sticky="ew", padx=8)
        self.x0_label = ttk.Label(controls, width=7)
        self.x0_label.grid(row=0, column=2, sticky="w")
        ttk.Label(controls, text="Шаг Δx:").grid(row=1, column=0, sticky="w")
        self.h_scale = ttk.Scale(controls, from_=0.05, to=3, variable=self.h,
                                 command=lambda _v: self.redraw())
        self.h_scale.grid(row=1, column=1, sticky="ew", padx=8)
        self.h_label = ttk.Label(controls, width=7)
        self.h_label.grid(row=1, column=2, sticky="w")
        checks = ttk.Frame(controls)
        checks.grid(row=0, column=3, rowspan=2, padx=(18, 0), sticky="w")
        ttk.Checkbutton(checks, text="График производной f′(x)",
                        variable=self.show_derivative, command=self.redraw).pack(anchor="w")
        ttk.Checkbutton(checks, text="Секущая", variable=self.show_secant,
                        command=self.redraw).pack(anchor="w")
        ttk.Checkbutton(checks, text="Касательная", variable=self.show_tangent,
                        command=self.redraw).pack(anchor="w")
        controls.columnconfigure(1, weight=1)

        self.fig = Figure(figsize=(9, 5.7), dpi=100, layout="constrained")
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(2, 0))
        toolbar_frame = ttk.Frame(self.root)
        toolbar_frame.pack(fill=tk.X, padx=10)
        NavigationToolbar2Tk(self.canvas, toolbar_frame).update()
        bottom = ttk.Frame(self.root, padding=10)
        bottom.pack(fill=tk.X)
        self.derivative_label = ttk.Label(bottom, text="", font=("Arial", 11, "bold"))
        self.derivative_label.pack(anchor="w")
        self.info_label = ttk.Label(bottom, text="", font=("Arial", 10))
        self.info_label.pack(anchor="w", pady=(4, 0))
        ttk.Label(self.root, textvariable=self.status, relief=tk.SUNKEN,
                  anchor="w", padding=4).pack(fill=tk.X, side=tk.BOTTOM)

    def apply_function(self):
        try:
            new_expr = parse_function(self.formula.get())
            new_derivative = sp.diff(new_expr, x)
            sp.lambdify(x, new_expr, modules=["numpy"])
            self.expr, self.derivative = new_expr, new_derivative
            self.status.set("Функция успешно построена.")
            self.redraw()
        except Exception as exc:
            messagebox.showerror("Ошибка формулы", str(exc))
            self.status.set("Ошибка ввода формулы.")

    @staticmethod
    def numeric_function(expr):
        return sp.lambdify(x, expr, modules=["numpy"])

    @staticmethod
    def safe_values(func, values):
        with np.errstate(all="ignore"):
            result = np.asarray(func(values), dtype=float)
        if result.ndim == 0:
            result = np.full_like(values, float(result), dtype=float)
        return np.where(np.isfinite(result) & (np.abs(result) < 1e8), result, np.nan)

    def redraw(self):
        if not hasattr(self, "ax"):
            return
        x0, h = float(self.x0.get()), max(float(self.h.get()), 1e-4)
        self.x0_label.configure(text=f"{x0:.2f}")
        self.h_label.configure(text=f"{h:.2f}")
        f, df = self.numeric_function(self.expr), self.numeric_function(self.derivative)
        xs = np.linspace(-10, 10, 1200)
        ys = self.safe_values(f, xs)
        y0 = float(self.safe_values(f, np.array([x0]))[0])
        y1 = float(self.safe_values(f, np.array([x0 + h]))[0])
        slope = float(self.safe_values(df, np.array([x0]))[0])
        self.ax.clear()
        self.ax.axhline(0, color="#555", linewidth=0.8)
        self.ax.axvline(0, color="#555", linewidth=0.8)
        self.ax.grid(True, alpha=0.25)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title("График функции и её производной")
        self.ax.plot(xs, ys, color="#1769aa", linewidth=2.2,
                     label=f"f(x) = {sp.sstr(self.expr)}")
        if self.show_derivative.get():
            dys = self.safe_values(df, xs)
            self.ax.plot(xs, dys, color="#e07a1f", linewidth=1.8, linestyle="--",
                         label=f"f′(x) = {sp.sstr(self.derivative)}")
        if np.isfinite(y0) and np.isfinite(y1):
            secant_slope = (y1 - y0) / h
            if self.show_secant.get():
                line_x = np.array([x0 - 1.5, x0 + h + 1.5])
                self.ax.plot(line_x, y0 + secant_slope * (line_x - x0),
                             color="#269b58", linewidth=1.7,
                             label=f"Секущая, наклон = {secant_slope:.4g}")
                self.ax.scatter([x0, x0 + h], [y0, y1], color="#269b58", zorder=5)
            if self.show_tangent.get() and np.isfinite(slope):
                line_x = np.array([x0 - 1.5, x0 + h + 1.5])
                self.ax.plot(line_x, y0 + slope * (line_x - x0),
                             color="#b23a8a", linewidth=1.8,
                             label=f"Касательная, наклон = f′({x0:.2f}) = {slope:.4g}")
                self.ax.scatter([x0], [y0], color="#b23a8a", zorder=6)
        self.ax.legend(loc="best", fontsize=8)
        self.canvas.draw_idle()
        self.derivative_label.configure(text=f"Производная:  f′(x) = {sp.sstr(self.derivative)}")
        if np.isfinite(y0) and np.isfinite(y1) and np.isfinite(slope):
            secant_slope = (y1 - y0) / h
            self.info_label.configure(
                text=f"В точке x₀ = {x0:.3f}: f(x₀) = {y0:.5g};  "
                     f"наклон секущей = {secant_slope:.5g};  "
                     f"наклон касательной = f′(x₀) = {slope:.5g}. "
                     "При уменьшении Δx наклон секущей приближается к производной."
            )
        else:
            self.info_label.configure(text="В выбранной точке функция или производная не определена.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DerivativeVisualizer(root)
    root.mainloop()
