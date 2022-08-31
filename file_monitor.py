import os
from stat import *
import time
from datetime import datetime
from subprocess import Popen
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk


def get_file(event=None):
    if event:
        # function was called from ent_box
        file_path = ent_box.get()
        print(f'FILEPATH: {file_path}')
    else:
        # open choose file dialog
        file_path = filedialog.askopenfilename(title="Choose File to Monitor")
    if file_path:
        # parse file name from path
        file_path = os.path.normpath(file_path)
        print(f'file_path type {type(file_path)} - {file_path}')
        if '/' in file_path:
            lbl = file_path.split('/')[-1]
        elif '\\' in file_path:
            lbl = file_path.split('\\')[-1]
        else:
            lbl = file_path
        if len(lbl) > 28:
            lbl = f'...{lbl[-28:]}'
        # set string variables
        path_lbl_var.set(f"Monitoring: {lbl}")
        path_var.set(file_path)
        # add labels to GUI
        frame.grid(column=0, row=2, columnspan=3, rowspan=5)
        path_lbl.pack()
        mod_lbl.pack()
        acc_lbl.pack()
        # call the looping status function
        update_file_status()


def update_file_status():
    try:
        file_stat = os.stat(path_var.get())
    except FileNotFoundError as er:
        mod_var.set('')
        print(type(er.strerror.title()))
        mod_var.set(er.strerror.title())
        acc_var.set('')
        return
    mod_var.set(f'Last Modified: {timestamp_to_str(file_stat.st_mtime)}')
    acc_var.set(f'Last Accessed: {timestamp_to_str(file_stat.st_atime)}')
    # add timer to GUI mainloop
    frame.after(30000, update_file_status)


def timestamp_to_str(timestamp):
    stamp_str = datetime.fromtimestamp(timestamp)
    return stamp_str.strftime('%b %d %y %I:%M:%S %p')


# start GUI
window = tk.Tk()
window.title('File Monitor')
# window.geometry("600x400")

# make a frame with some padding
content = ttk.Frame(window, padding=(12, 0, 12, 12))
print(f'Content Keys: {content.keys()}')

# initialize string variables
path_var = tk.StringVar(content)
path_lbl_var = tk.StringVar(content)
mod_var = tk.StringVar(content)
acc_var = tk.StringVar(content)


# initialize widgets
btn_1 = ttk.Button(content, text="Choose File", command=get_file)
print(f'Button Keys: {btn_1.keys()}')

ent_box = ttk.Entry(content)
print(f'Entry Keys: {ent_box.keys()}')

ent_lbl = ttk.Label(content, text='or   Enter Path', padding=10, anchor='w')
print(f'Entry Label Keys: {ent_lbl.keys()}')

# add message box frame
frame = ttk.Frame(content, borderwidth=8, relief="ridge", width=300, height=100)
print(f'Frame Keys: {frame.keys()}')
# associate message labels with variables
path_lbl = ttk.Label(frame, textvariable=path_lbl_var, font=("Helvetica", 14))
mod_lbl = ttk.Label(frame, textvariable=mod_var, padding=4, font=("Helvetica", 14))
acc_lbl = ttk.Label(frame, textvariable=acc_var)

# place widgets in grid
content.grid(column=0, row=0)
btn_1.grid(column=0, row=0)
ent_lbl.grid(column=1, row=0)
ent_box.grid(column=2, row=0, columnspan=2)

ent_box.bind("<Return>", get_file)

window.mainloop()
