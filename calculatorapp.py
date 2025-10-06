import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
import os

# ------------------------- CALCULATOR CORE -------------------------
class Calculator:
    def __init__(self, entry_var):
        self.entry_var = entry_var
        self.expression = ""
        self.is_dark = True

    def press(self, value):
        self.expression += str(value)
        self.entry_var.set(self.expression)

    def clear(self):
        self.expression = ""
        self.entry_var.set("")

    def delete(self):
        self.expression = self.expression[:-1]
        self.entry_var.set(self.expression)

    def format_result(self, res):
        # Round to 10 decimals and remove trailing zeros
        res_rounded = round(res, 10)
        res_str = str(res_rounded)
        if '.' in res_str:
            res_str = res_str.rstrip('0').rstrip('.')
        return res_str

    def evaluate(self):
        try:
            # Replace ^ with ** for power operator support
            expression = self.expression.replace("^", "**")
            result = eval(expression)
            formatted_result = self.format_result(result)
            self.entry_var.set(formatted_result)
            self.expression = formatted_result
        except Exception:
            self.entry_var.set("Error")
            self.expression = ""

    def scientific_func(self, func):
        try:
            value = float(eval(self.expression)) if self.expression else 0
            if func == "sqrt":
                res = math.sqrt(value)
            elif func == "square":
                res = value ** 2
            elif func == "cube":
                res = value ** 3
            elif func == "pow":
                parts = self.expression.split("^")
                if len(parts) == 2:
                    base = float(eval(parts[0]))
                    exp = float(eval(parts[1]))
                    res = math.pow(base, exp)
                else:
                    res = value ** 2  # fallback
            elif func == "ten_pow":
                res = 10 ** value
            elif func == "log2":
                res = math.log2(value)
            elif func == "sin":
                res = math.sin(math.radians(value))
            elif func == "cos":
                res = math.cos(math.radians(value))
            elif func == "tan":
                res = math.tan(math.radians(value))
            elif func == "asin":
                res = math.degrees(math.asin(value))
            elif func == "acos":
                res = math.degrees(math.acos(value))
            elif func == "atan":
                res = math.degrees(math.atan(value))
            elif func == "sinh":
                res = math.sinh(value)
            elif func == "cosh":
                res = math.cosh(value)
            elif func == "tanh":
                res = math.tanh(value)
            elif func == "log":
                res = math.log10(value)
            elif func == "ln":
                res = math.log(value)
            elif func == "exp":
                res = math.exp(value)
            elif func == "inv":
                res = 1 / value
            elif func == "neg":
                res = -value
            elif func == "fact":
                res = math.factorial(int(value))
            elif func == "pi":
                res = math.pi
            elif func == "e":
                res = math.e
            else:
                res = value

            formatted_res = self.format_result(res)
            self.entry_var.set(formatted_res)
            self.expression = formatted_res
        except Exception:
            self.entry_var.set("Error")
            self.expression = ""

# ------------------------- THEME PERSISTENCE -------------------------
def save_theme(is_dark):
    try:
        with open("theme.json", "w") as f:
            json.dump({"dark": is_dark}, f)
    except Exception:
        pass  # Ignore file errors

def load_theme():
    try:
        if os.path.exists("theme.json"):
            with open("theme.json") as f:
                return json.load(f).get("dark", True)
    except Exception:
        pass
    return True

# ------------------------- MAIN UI -------------------------
def main():
    root = tk.Tk()
    root.title("Electric Purple Neon Calculator")
    root.geometry("480x600")
    root.resizable(False, False)

    # --------------- COLORS ---------------
    neon_purple = "#FF00FF"
    dark_bg = "#0D0D0D"
    light_bg = "#EAEAEA"
    dark_btn = "#1E1E1E"
    light_btn = "#FFFFFF"
    dark_text = "#FFFFFF"
    light_text = "#000000"

    # --------------- VARIABLES ---------------
    entry_var = tk.StringVar()
    calc = Calculator(entry_var)

    # Load saved theme preference
    calc.is_dark = load_theme()
    current_bg = dark_bg if calc.is_dark else light_bg
    current_btn = dark_btn if calc.is_dark else light_btn
    current_fg = dark_text if calc.is_dark else light_text

    # --------------- THEME TOGGLE ---------------
    def toggle_theme():
        nonlocal current_bg, current_btn, current_fg
        calc.is_dark = not calc.is_dark
        if calc.is_dark:
            current_bg, current_btn, current_fg = dark_bg, dark_btn, dark_text
        else:
            current_bg, current_btn, current_fg = light_bg, light_btn, light_text
        save_theme(calc.is_dark)
        apply_theme()

    # --------------- APPLY THEME FUNCTION ---------------
    def apply_theme():
        root.configure(bg=current_bg)
        entry.configure(bg=current_btn, fg=neon_purple if calc.is_dark else current_fg)
        style.configure("TNotebook", background=current_bg)
        style.configure("TNotebook.Tab", background=current_btn, foreground=neon_purple, padding=[10, 5])
        for frame in [std_frame, sci_frame]:
            frame.configure(bg=current_bg)
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg=current_btn, fg=neon_purple if calc.is_dark else current_fg,
                                     activebackground="#222222" if calc.is_dark else "#CCCCCC")

    # --------------- ENTRY FIELD ---------------
    entry = tk.Entry(root, textvariable=entry_var, font=("Consolas", 22, "bold"),
                     bd=8, insertwidth=2, width=22, relief=tk.FLAT,
                     bg=current_btn, fg=neon_purple if calc.is_dark else current_fg, justify="right")
    entry.pack(pady=20)

    # --------------- KEYBOARD SUPPORT ---------------
    def on_keypress(event):
        char = event.char
        if char in "0123456789.+-*/^()":
            calc.press(char)
        elif event.keysym == "Return":
            calc.evaluate()
        elif event.keysym == "BackSpace":
            calc.delete()
    root.bind("<Key>", on_keypress)

    # --------------- NOTEBOOK (TABS) ---------------
    style = ttk.Style()
    style.theme_use("default")
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    std_frame = tk.Frame(notebook, bg=current_bg)
    sci_frame = tk.Frame(notebook, bg=current_bg)

    notebook.add(std_frame, text="Standard")
    notebook.add(sci_frame, text="Scientific")

    # --------------- BUTTON CREATOR ---------------
    def create_button(parent, text, command, row, col):
        btn = tk.Button(parent, text=text, font=("Arial", 14, "bold"),
                        width=6, height=2, relief=tk.FLAT, bg=current_btn,
                        fg=neon_purple if calc.is_dark else current_fg, activebackground="#222222",
                        command=command)
        btn.grid(row=row, column=col, padx=6, pady=6)

        def on_enter(e): btn.configure(bg=neon_purple, fg=current_bg if calc.is_dark else light_bg)
        def on_leave(e): btn.configure(bg=current_btn, fg=neon_purple if calc.is_dark else current_fg)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # --------------- STANDARD BUTTONS ---------------
    std_buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"]
    ]
    for r, row in enumerate(std_buttons):
        for c, text in enumerate(row):
            if text == "=":
                create_button(std_frame, text, calc.evaluate, r, c)
            else:
                create_button(std_frame, text, lambda val=text: calc.press(val), r, c)

    create_button(std_frame, "C", calc.clear, 4, 0)
    create_button(std_frame, "DEL", calc.delete, 4, 1)
    create_button(std_frame, "Theme", toggle_theme, 4, 2)
    create_button(std_frame, "Exit", root.destroy, 4, 3)

    # --------------- SCIENTIFIC BUTTONS ---------------
    sci_buttons = [
        ["sqrt", "square", "cube", "pow", "ten_pow"],
        ["sin", "cos", "tan", "asin", "acos"],
        ["atan", "sinh", "cosh", "tanh", "log2"],
        ["ln", "log", "exp", "inv", "neg"],
        ["pi", "e", "C", "DEL", "Back"]
    ]

    sci_func_map = {
        "sqrt": "sqrt", "square": "square", "cube": "cube",
        "pow": "pow", "ten_pow": "ten_pow", "log2": "log2",
        "sin": "sin", "cos": "cos", "tan": "tan",
        "asin": "asin", "acos": "acos", "atan": "atan",
        "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
        "ln": "ln", "log": "log", "exp": "exp",
        "inv": "inv", "neg": "neg", "pi": "pi", "e": "e"
    }

    for r, row in enumerate(sci_buttons):
        for c, text in enumerate(row):
            if text == "C":
                create_button(sci_frame, text, calc.clear, r, c)
            elif text == "DEL":
                create_button(sci_frame, text, calc.delete, r, c)
            elif text == "Back":
                create_button(sci_frame, text, lambda: notebook.select(std_frame), r, c)
            else:
                create_button(sci_frame, text, lambda val=sci_func_map[text]: calc.scientific_func(val), r, c)

    # --------------- APPLY INITIAL THEME ---------------
    apply_theme()

    # --------------- ABOUT MENU ---------------
    menubar = tk.Menu(root)
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
        "About",
        "Electric Purple Neon Calculator\nDeveloped by Atkur Manasa\nOutriX Internship – Task 1"
    ))
    menubar.add_cascade(label="Help", menu=help_menu)
    root.config(menu=menubar)

    root.mainloop()

if __name__ == "__main__":
    main()
