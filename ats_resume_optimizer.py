# =============================================
# ENTER YOUR GROQ API KEY HERE
# Get your key at: https://console.groq.com/keys
API_KEY = "grok_api_here"
# =============================================

import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

try:
    from groq import Groq
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "groq"])
    from groq import Groq

BG      = "#0f0f13"
BG2     = "#1a1a24"
BG3     = "#22223a"
ACCENT  = "#7c6ff7"
ACCENT2 = "#a78bfa"
GREEN   = "#4ade80"
YELLOW  = "#facc15"
RED     = "#f87171"
TEXT    = "#e2e8f0"
TEXT2   = "#94a3b8"
BORDER  = "#2e2e4a"

SYSTEM_PROMPT = """You are an elite Applicant Tracking System (ATS) optimization expert. Your task is to analyze the provided Job Description and Resume.
When I provide both documents, perform the following:
Calculate a realistic ATS Match Score (%) based on keyword alignment, skills match, experience relevance, education, certifications, and overall compatibility.
Identify the Top 5 Missing Keywords or Phrases that appear important in the Job Description but are absent or underrepresented in the Resume.
Explain briefly why each missing keyword matters for ATS ranking.
Rewrite 3 existing resume bullet points to naturally incorporate the missing keywords while maintaining professional, achievement-oriented language.
Highlight any critical ATS issues such as:
Missing hard skills
Missing certifications
Job title mismatches
Formatting concerns
Industry-specific terminology gaps
Provide actionable recommendations to increase the ATS score.
Output Format:
ATS Match Score: XX%
Top 5 Missing Keywords:
Keyword
Reason:
Keyword
Reason:
Keyword
Reason:
Keyword
Reason:
Keyword
Reason:
Rewritten Resume Bullet Points:
• Original:
Improved Version:
• Original:
Improved Version:
• Original:
Improved Version:
Additional ATS Optimization Recommendations:
Recommendation 1
Recommendation 2
Recommendation 3
Wait for me to provide the Job Description and Resume before starting the analysis."""


def analyze(job_description, resume):
    client = Groq(api_key=API_KEY)
    user_prompt = f"Job Description:\n{job_description}\n\nResume:\n{resume}"
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=2048,
    )
    return response.choices[0].message.content.strip()


def dark_scrollbar(widget):
    widget.vbar.configure(
        bg=BG3, troughcolor=BG2, activebackground=ACCENT,
        highlightbackground=BG, highlightcolor=BG,
        bd=0, relief="flat", width=10, elementborderwidth=0,
    )


def make_text(parent, **kw):
    t = scrolledtext.ScrolledText(parent, **kw)
    dark_scrollbar(t)
    return t


def open_result_window(root, report_text):
    win = tk.Toplevel(root)
    win.title("ATS Compatibility Report")
    win.geometry("820x900")
    win.minsize(700, 600)
    win.configure(bg=BG)

    try:
        win.update()
        from ctypes import windll, byref, sizeof, c_int
        HWND = windll.user32.GetParent(win.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(HWND, 20, byref(c_int(1)),          sizeof(c_int))
        windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x00130f0f)), sizeof(c_int))
        windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(0x00ffffff)), sizeof(c_int))
    except Exception:
        pass

    frame = tk.Frame(win, bg=BG, padx=18, pady=14)
    frame.pack(fill="both", expand=True)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    result_text = make_text(
        frame,
        font=("Segoe UI", 11), wrap="word",
        bg=BG2, fg=TEXT,
        relief="flat", bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        state="disabled",
        padx=20, pady=18,
    )
    result_text.grid(row=0, column=0, sticky="nsew")

    result_text.tag_config("header", font=("Segoe UI", 18, "bold"), foreground=ACCENT2)
    result_text.tag_config("body",   font=("Segoe UI", 11),         foreground=TEXT)
    result_text.tag_config("divider", foreground=BORDER)

    def write(text, tag="body"):
        result_text.config(state="normal")
        result_text.insert("end", text, tag)
        result_text.config(state="disabled")

    write("ATS Compatibility Report\n", "header")
    write("─" * 62 + "\n\n", "divider")
    write(report_text, "body")

    result_text.see("1.0")


def build_ui(root):
    root.title("ATS Resume Optimizer")
    root.geometry("1100x680")
    root.minsize(900, 560)
    root.configure(bg=BG)

    try:
        root.update()
        from ctypes import windll, byref, sizeof, c_int
        HWND = windll.user32.GetParent(root.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(HWND, 20, byref(c_int(1)),          sizeof(c_int))
        windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x00130f0f)), sizeof(c_int))
        windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(0x00ffffff)), sizeof(c_int))
    except Exception:
        pass

    header = tk.Frame(root, bg=BG2, pady=18)
    header.pack(fill="x")
    tk.Label(header, text="ATS Resume Optimizer",
             font=("Segoe UI", 20, "bold"), bg=BG2, fg=ACCENT2).pack()
    tk.Label(header,
             text="Paste your job description & resume — get an instant ATS compatibility report",
             font=("Segoe UI", 10), bg=BG2, fg=TEXT2).pack(pady=(4, 0))

    inp = tk.Frame(root, bg=BG, padx=18, pady=14)
    inp.pack(fill="both", expand=True)
    inp.columnconfigure(0, weight=1)
    inp.columnconfigure(1, weight=1)
    inp.rowconfigure(1, weight=1)

    tk.Label(inp, text="Job Description", font=("Segoe UI", 11, "bold"),
             bg=BG, fg=ACCENT2).grid(row=0, column=0, sticky="w", pady=(0, 6))
    tk.Label(inp, text="Resume / CV", font=("Segoe UI", 11, "bold"),
             bg=BG, fg=ACCENT2).grid(row=0, column=1, sticky="w", pady=(0, 6), padx=(12, 0))

    txt_cfg = dict(
        font=("Segoe UI", 10), wrap="word",
        bg=BG2, fg=TEXT,
        insertbackground=ACCENT2,
        selectbackground=ACCENT,
        selectforeground="white",
        relief="flat", bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        padx=10, pady=10,
    )

    jd_text = make_text(inp, **txt_cfg)
    jd_text.grid(row=1, column=0, sticky="nsew")

    cv_text = make_text(inp, **txt_cfg)
    cv_text.grid(row=1, column=1, sticky="nsew", padx=(12, 0))

    btn_frame = tk.Frame(root, bg=BG, pady=16)
    btn_frame.pack()

    analyze_btn = tk.Button(
        btn_frame, text="  Analyze Match  ",
        font=("Segoe UI", 12, "bold"),
        bg=ACCENT, fg="white",
        activebackground=ACCENT2, activeforeground="white",
        relief="flat", padx=28, pady=10,
        cursor="hand2", bd=0,
    )
    analyze_btn.pack()

    status_lbl = tk.Label(root, text="", font=("Segoe UI", 9), bg=BG, fg=TEXT2)
    status_lbl.pack(pady=(0, 10))

    def show_error(msg):
        analyze_btn.config(state="normal", text="  Analyze Match  ")
        status_lbl.config(text="")
        messagebox.showerror("Error", f"API request failed:\n\n{msg}")

    def run_thread(jd, cv):
        try:
            result = analyze(jd, cv)
            root.after(0, lambda: on_result(result))
        except Exception as exc:
            err_msg = str(exc)
            root.after(0, lambda: show_error(err_msg))

    def on_result(report_text):
        analyze_btn.config(state="normal", text="  Analyze Match  ")
        status_lbl.config(text="")
        open_result_window(root, report_text)

    def on_analyze():
        jd = jd_text.get("1.0", "end").strip()
        cv = cv_text.get("1.0", "end").strip()
        if not jd or not cv:
            messagebox.showwarning("Missing Input",
                                   "Please fill in both the job description and your resume.")
            return
        if "ENTER_GROQ_API_KEY_HERE" in API_KEY:
            messagebox.showerror("API Key Missing",
                                 "Please paste your Groq API key at the top of the file.\n\nGet it from: https://console.groq.com/keys")
            return
        analyze_btn.config(state="disabled", text="  Analyzing...  ")
        status_lbl.config(text="Sending request to Groq API...")
        threading.Thread(target=run_thread, args=(jd, cv), daemon=True).start()

    analyze_btn.config(command=on_analyze)


if __name__ == "__main__":
    root = tk.Tk()
    build_ui(root)
    root.mainloop()
