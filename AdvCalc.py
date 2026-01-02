import tkinter as tk
import math
import ast
import operator
import json
import numpy as np
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt


# ---------------- SAFE MATH ENGINE ---------------- #
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}

FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "log": math.log,
    "abs": abs
}

class SafeEvaluator:
    def __init__(self):
        self.vars = {}

    def assign(self, name, value):
        self.vars[name] = value

    def eval(self, expr):
        tree = ast.parse(expr, mode="eval")
        return self._eval_node(tree.body)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid constant")

        if isinstance(node, ast.Name):
            if node.id in self.vars:
                return self.vars[node.id]
            raise ValueError(f"Unknown variable '{node.id}'")

        if isinstance(node, ast.BinOp):
            return OPS[type(node.op)](
                self._eval_node(node.left),
                self._eval_node(node.right)
            )

        if isinstance(node, ast.UnaryOp):
            return OPS[type(node.op)](
                self._eval_node(node.operand)
            )

        if isinstance(node, ast.Call):
            func = FUNCS.get(node.func.id)
            if not func:
                raise ValueError("Unknown function")
            return func(self._eval_node(node.args[0]))

        raise ValueError("Invalid expression")

# ---------------- GRAPHING ---------------- #

def graph_expression(expr, evaluator):
    expr = expr.strip()
    
    # Block assignments
    if "=" in expr:
        messagebox.showinfo("Graph", "Cannot graph assignments")
        return
    
    # Generate x values
    x_vals = np.linspace(-10, 10, 400)
    y_vals = []

    for x in x_vals:
        evaluator.vars["x"] = x
        try:
            # Evaluate numbers / expressions safely
            y = evaluator.eval(expr)
            y_vals.append(y)
        except:
            y_vals.append(np.nan)  # use NaN for matplotlib
     
    # Check if all y_vals are identical numbers
    if all(y == y_vals[0] for y in y_vals if y is not np.nan):
        messagebox.showinfo("Graph", f"Plotting constant: y = {y_vals[0]}")
    
    plt.figure("Graph")
    plt.plot(x_vals, y_vals)
    plt.xlabel("x")
    plt.ylabel(expr)
    plt.grid(True)
    plt.show()


# ---------------- CALCULATOR APP ---------------- #

class Calculator(tk.Tk):
    SAVE_FILE = "calc_history.json"

    def __init__(self):
        super().__init__()
        self.title("Advanced Calculator")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")

        self.evaluator = SafeEvaluator()

        self.create_widgets()
        self.bind_keys()
        self.load_state()

    # ---------------- UI ---------------- #

    def create_widgets(self):
        self.display = tk.Entry(
            self, font=("Consolas", 16),
            bg="#2d2d2d", fg="white",
            justify="right", borderwidth=0
        )
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="we")

        self.history = tk.Listbox(
            self, height=6,
            bg="#252526", fg="white", borderwidth=0
        )
        self.history.grid(row=1, column=0, columnspan=5, padx=10, sticky="we")
        self.history.bind("<<ListboxSelect>>", self.use_history)

        buttons = [
            "7", "8", "9", "/", "sin",
            "4", "5", "6", "*", "cos",
            "1", "2", "3", "-", "tan",
            "0", ".", "(", ")", "+",
            "sqrt", "log", "^", "⌫", "="
        ]

        row, col = 2, 0
        for text in buttons:
            self.make_button(text, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1

        self.make_button("GRAPH", row + 1, 0, colspan=2)
        self.make_button("CLEAR", row + 1, 2, colspan=3)

    def make_button(self, text, row, col, colspan=1):
        tk.Button(
            self, text=text, width=6 * colspan, height=2,
            bg="#3c3c3c", fg="white",
            borderwidth=0,
            command=lambda t=text: self.press(t)
        ).grid(row=row, column=col, columnspan=colspan, padx=2, pady=2)

    # ---------------- LOGIC ---------------- #

    def press(self, value):
        if value == "=":
            self.calculate()
        elif value == "⌫":
            self.display.delete(len(self.display.get()) - 1)
        elif value == "^":
            self.display.insert(tk.END, "**")
        elif value == "CLEAR":
            self.display.delete(0, tk.END)
        elif value == "GRAPH":
            graph_expression(self.display.get(), self.evaluator)
        else:
            self.display.insert(tk.END, value)

    def calculate(self):
        expr = self.display.get().strip()

        try:
            # VARIABLE ASSIGNMENT
            if "=" in expr:
                name, rhs = expr.split("=", 1)
                name = name.strip()

                if not name.isidentifier():
                    raise ValueError("Invalid variable name")

                value = self.evaluator.eval(rhs.strip())
                self.evaluator.assign(name, value)

                # CLEAN assignment history
                self.history.insert(0, f"{name} = {value}")
                self.display.delete(0, tk.END)
                self.display.insert(0, value)

            # NORMAL EXPRESSION
            else:
                result = self.evaluator.eval(expr)
                self.history.insert(0, f"{expr} = {result}")
                self.display.delete(0, tk.END)
                self.display.insert(0, result)

        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")



    # ---------------- HISTORY ---------------- #

    def use_history(self, event):
        if not self.history.curselection():
            return
        text = self.history.get(self.history.curselection())
        expr = text.split("=")[0].strip()
        self.display.delete(0, tk.END)
        self.display.insert(0, expr)

    def save_state(self):
        data = {
            "history": list(self.history.get(0, tk.END)),
            "vars": self.evaluator.vars
        }
        with open(self.SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load_state(self):
        try:
            with open(self.SAVE_FILE, "r") as f:
                data = json.load(f)
                for item in data["history"]:
                    self.history.insert(tk.END, item)
                self.evaluator.vars = data["vars"]
        except:
            pass

    # ---------------- KEYS ---------------- #

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<Escape>", lambda e: self.display.delete(0, tk.END))

    def destroy(self):
        self.save_state()
        super().destroy()

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    Calculator().mainloop()
