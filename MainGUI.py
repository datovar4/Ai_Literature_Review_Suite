import tkinter as tk
from tkinter import ttk
from pdf_summary import process_pdfs as run_pdf_summary
from lit_review_summary import main as run_lit_review_summary
import subprocess
import sys


def run_pdf_interrogation_subprocess():
    try:
        process = subprocess.Popen([sys.executable, "pdf_interrogation.py"])
        process.wait()
    except Exception as e:
        print(f"Failed to start subprocess: {e}")


def run_pdf_loader_subprocess():
    try:
        process = subprocess.Popen([sys.executable, "pdf_search.py"])
        process.wait()
    except Exception as e:
        print(f"Failed to start subprocess: {e}")


def run_pdf_extract_subprocess():
    try:
        process = subprocess.Popen([sys.executable, "pdf_extracter.py"])
        process.wait()
    except Exception as e:
        print(f"Failed to start subprocess: {e}")


def run_combined():
    excel_filename = run_pdf_summary()
    run_lit_review_summary(excel_filename)

def close_gui():
    root.destroy()

root = tk.Tk()
root.geometry('800x800')
root.title('Literature Review GUI')
root.configure(bg='lightgray')

style = ttk.Style()

style.configure("TButton1.TButton", font=('Helvetica', '12'), 
                foreground='black', background='green', wraplength=200)
style.configure("TButton2.TButton", font=('Helvetica', '12'), 
                foreground='black', background='#60a3bc', wraplength=200)
style.configure("TButton3.TButton", font=('Helvetica', '12'), 
                foreground='black', background='blue', wraplength=200)
style.configure("TButton4.TButton", font=('Helvetica', '12'), 
                foreground='black', background='red', wraplength=200)
style.configure("TButton5.TButton", font=('Helvetica', '12'), 
                foreground='black', background='yellow', wraplength=200)
style.configure("TButton6.TButton", font=('Helvetica', '12'), 
                foreground='black', background='yellow', wraplength=200)
style.configure("TButton7.TButton", font=('Helvetica', '12'), 
                foreground='black', background='purple', wraplength=200)  # Define style for "All Done" button

btn1 = ttk.Button(root, text="PDF Search", command=run_pdf_loader_subprocess, style="TButton5.TButton")
btn1.grid(row=0, column=0, padx=50, pady=50, sticky='nesw')

btn2 = ttk.Button(root, text="Get PDFs from Article", command=run_pdf_extract_subprocess, style="TButton6.TButton")
btn2.grid(row=0, column=1, padx=50, pady=50, sticky='nesw')

btn3 = ttk.Button(root, text="Friendly chat with PDF", command=run_pdf_interrogation_subprocess, style="TButton3.TButton")
btn3.grid(row=1, column=0, padx=50, pady=50, sticky='nesw')

btn4 = ttk.Button(root, text="Excel Lit Table and Synthesis", command=run_combined, style="TButton4.TButton")
btn4.grid(row=1, column=1, padx=50, pady=50, sticky='nesw')

btn5 = ttk.Button(root, text="Create Excel Sheet Lit Review", command=run_pdf_summary, style="TButton1.TButton")
btn5.grid(row=2, column=0, padx=50, pady=50, sticky='nesw')

btn6 = ttk.Button(root, text="Lit Synthesis from Excel Sheet", command=run_lit_review_summary, style="TButton2.TButton")
btn6.grid(row=2, column=1, padx=50, pady=50, sticky='nesw')

btn7 = ttk.Button(root, text="All Done", command=close_gui, style="TButton7.TButton")  # Add "All Done" button
btn7.grid(row=3, column=0, columnspan=2, padx=50, pady=50, sticky='nesw')  # Put "All Done" button on the next row, centering it by spanning 2 columns

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)  # Configure the new row for the "All Done" button
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
