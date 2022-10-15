import os
from stat import *
import time
from datetime import datetime
from subprocess import Popen
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from winotify import Notification, audio

LASTMOD = None
MODTIME = None
PREVMOD = None
STATTIME = 30 # seconds between polling the file status


def win_notify(msg):
    toast = Notification(app_id="FileMonitor",
                         title="File was modified.",
                         msg=msg)
                         
    toast.set_audio(audio.Mail, loop=False)
    toast.show()



def get_file(event=None):
    global LASTMOD
    global MODTIME
    global PREVMOD
    # clear all variables in case file changed
    LASTMOD = None
    MODTIME = None
    PREVMOD = None
    prev_mod_var.set('')
    prev_mod_1_var.set('')
    mod_var.set('')
    if event:
        # function was called from ent_box
        file_path = ent_box.get()
    else:
        # open choose file dialog
        file_path = filedialog.askopenfilename(title="Choose File to Monitor")
    if file_path:
        file_path = os.path.normpath(file_path)
        # set string variables
        path_lbl_var.set(f"Monitoring: {file_path}")
        path_var.set(file_path)
        # add labels to GUI
        frame.grid(column=0, row=2, columnspan=3, rowspan=5)
        path_lbl.pack()
        mod_lbl.pack()
        history_lbl.pack()
        prev_lbl.pack()
        prev_lbl_1.pack()
        # call the looping status function
        update_file_status()


def update_file_status():
    global LASTMOD
    global MODTIME
    global PREVMOD
    was_modded = False
    try:
        file_stat = os.stat(path_var.get())
    except FileNotFoundError as er:
        mod_var.set('')
        mod_var.set(er.strerror.title())
        return
    # set globals
    if MODTIME is None:
        MODTIME = file_stat.st_mtime
    elif MODTIME != file_stat.st_mtime:
        LASTMOD = PREVMOD
        PREVMOD = MODTIME
        MODTIME = file_stat.st_mtime
        was_modded = True
    # set sring varables
    mod_str = timestamp_to_str(MODTIME)
    mod_var.set(f'Last Modified: {mod_str}')
    if PREVMOD is not None:
        prev_mod_var.set(timestamp_to_str(PREVMOD))
    if LASTMOD is not None:
        prev_mod_1_var.set(timestamp_to_str(LASTMOD))
    if was_modded:
        win_notify(mod_str)
    # add timer to GUI mainloop
    frame.after((STATTIME * 1000), update_file_status)


def timestamp_to_str(timestamp):
    stamp_str = datetime.fromtimestamp(timestamp)
    return stamp_str.strftime('%b %d %y %I:%M:%S %p')


# start GUI
window = tk.Tk()
window.title('File Monitor')

# make a frame with some padding
content = ttk.Frame(window, padding=(12, 0, 12, 12))

# initialize string variables
path_var = tk.StringVar(content)
path_lbl_var = tk.StringVar(content)
mod_var = tk.StringVar(content)
prev_mod_var = tk.StringVar(content)
prev_mod_1_var = tk.StringVar(content)


# initialize widgets
btn_1 = ttk.Button(content, text="Choose File", command=get_file)

ent_box = ttk.Entry(content)

ent_lbl = ttk.Label(content, text='or   Enter Path', padding=10, anchor='w')


# add message box frame
frame = ttk.Frame(content, borderwidth=8, relief="ridge",
                  width=300, height=100)
# associate message labels with string variables
path_lbl = ttk.Label(frame, textvariable=path_lbl_var)
mod_lbl = ttk.Label(frame, textvariable=mod_var, padding=4,
                    font=("Helvetica", 14))
history_lbl = ttk.Label(frame, text='History')
prev_lbl = ttk.Label(frame, textvariable=prev_mod_var)
prev_lbl_1 = ttk.Label(frame, textvariable=prev_mod_1_var)

# place widgets in grid
content.grid(column=0, row=0)
btn_1.grid(column=0, row=0)
ent_lbl.grid(column=1, row=0)
ent_box.grid(column=2, row=0, columnspan=2)

# bind keys
ent_box.bind("<Return>", get_file)

window.mainloop()
