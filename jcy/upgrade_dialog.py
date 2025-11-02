import tkinter as tk
from tkinter import ttk, messagebox
import threading
import copy
import json
import time
import shutil
import os

class UpgradeDialog(tk.Toplevel):
    """升级配置文件对话框"""
    def __init__(self, master, total_steps):
        super().__init__(master)
        self.title("配置升级中")
        self.geometry("500x400")
        self.resizable(False, False)
        self.total_steps = total_steps

        # 文本区域
        self.text = tk.Text(self, height=20, width=60, state='disabled')
        self.text.pack(padx=10, pady=10)

        # 进度条
        self.progress = ttk.Progressbar(self, length=460, maximum=total_steps, mode='determinate')
        self.progress.pack(pady=(0,10))

        # 关闭按钮，升级完成前禁用
        self.btn_close = tk.Button(self, text="关闭", command=self.destroy, state='disabled')
        self.btn_close.pack(pady=(0,10))

        self.update_idletasks()

    def log(self, message: str):
        self.text.config(state='normal')
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.config(state='disabled')
        self.update_idletasks()

    def step(self):
        self.progress['value'] += 1
        self.update_idletasks()

    def complete(self):
        self.progress['value'] = self.progress['maximum']
        self.btn_close.config(state='normal')
        self.update_idletasks()
        messagebox.showinfo("升级完成", "配置文件升级完成！")