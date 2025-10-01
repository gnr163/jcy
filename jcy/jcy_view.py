import base64
import webbrowser
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import threading
import tkinter as tk
import uuid
import win32gui
import win32process


import pystray

from cryptography.fernet import Fernet, InvalidToken
from jcy_constants import *
from jcy_paths import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, scrolledtext, ttk

class FeatureView:
    """
    UI控制
    """
    def __init__(self, master, all_features_config, controller):
        self.master = master
        self.all_features_config = all_features_config
        self.controller = controller
        # <tab_name, frame>
        self.tab_map = {}

        master.title(APP_FULL_NAME)
        master.geometry(APP_SIZE)

        # 新增的退出控制变量
        self.is_quitting = False
        self.tray_icon_running = threading.Event()
        
        self.feature_vars = {} 
        self.group_radio_buttons = {} 
        self.notebooke = None
        self.tz_tab = None
        self.tray_icon = None
        
        self._create_ui()
        self._create_tray_icon()  
        
        self._tray_cleanup_lock = threading.Lock()
        self._tray_cleanup_done = False

        # 绑定窗口销毁事件
        master.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)
        master.bind("<Destroy>", self._on_destroy)

    def _create_ui(self):
        # 创建底部按钮容器
        button_frame = ttk.Frame(self.master)
        button_frame.pack(side=tk.BOTTOM, pady=5)

        # 创建并加入“配置路径”按钮
        self.appdata_button = ttk.Button(button_frame, text="配置路径", command=self.controller.open_appdata)
        self.appdata_button.pack(side=tk.LEFT, padx=10, ipady=5)

        # 创建并加入“应用设置”按钮
        self.apply_button = ttk.Button(button_frame, text="应用设置", command=self.controller.apply_settings)
        self.apply_button.pack(side=tk.LEFT, padx=10, ipady=5)

        # 创建 Notebook 
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.notebook = notebook

        # 动态Tab
        for config in self.controller.feature_config.all_features_config.get("tabs"):
            self._create_tab(config)

        # --- D2R多开器 ---
        launcher_tab = D2RLauncherApp(notebook)
        self.add_tab(launcher_tab, "D2R多开器")

        # --- checktable ---
        filter_tab = ttk.Frame(notebook)
        self.add_tab(filter_tab, "道具屏蔽")

        columns = ["简体中文", "繁體中文", "enUS"]
        data = self.controller.file_operations.load_filter_config()
                
        checktable = TableWithCheckbox(
            filter_tab, columns, data,
            config_dict=self.controller.current_states,
            config_key="501",
            on_change=lambda new_val: self.controller.execute_feature_action("501", new_val)
        )
        checktable.pack(fill="both", expand=True, padx=10, pady=10)
        self.feature_vars["501"] = checktable


        # -- Donate --
        donate_tab = ttk.Frame(notebook)
        self.add_tab(donate_tab, "免责声明")

        try:
            image = Image.open(DONATE_WECHAT_PATH)
            image = image.resize((330, 440))
            photo = ImageTk.PhotoImage(image)
            label_img = tk.Label(donate_tab, image=photo)
            label_img.image = photo  # 防止垃圾回收
            label_img.pack(pady=10)
        except Exception as e:
            tk.Label(donate_tab, text="无法加载二维码图片").pack()

        disclaimer_text = """
            本Mod为Diablo爱好者制作，请您酌情考虑使用。如果您使用后导致账号被Ban，本人概不负责！如果您很介意这一点，建议您不要使用！
            本Mod完全免费使用。添加收款码仅为接受用户自愿打赏，不会为任何打赏提供额外功能或优先服务，所有功能对所有用户公开且无条件。
            如果您是相关权利方并认为本项目中的内容侵犯了您的权益，请联系我们，我们将在第一时间内进行删除或调整。
            Email: CMCC_1020@163.com
            感谢支持!
        """.strip()

        text_box = scrolledtext.ScrolledText(donate_tab, wrap='word', height=15)
        text_box.insert('1.0', disclaimer_text)
        text_box.configure(state='disabled')
        text_box.pack(fill='both', expand=True, padx=10, pady=10)

        # 绑定事件
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.notebook = notebook

    def _create_tab(self, config):
        tab = ttk.Frame(self.notebook)
        self.add_tab(tab, config.get("text"))

        total_columns = 10  # 每行总列数
        current_row = 0
        current_col = 0

        for child in config.get("children", []):
            fid = child.get("fid")
            type = child.get("type")
            colspan = child.get("colspan", total_columns)  # 默认占满整行
            
            if RADIO == type:
                group = LabeledRadioGroup(
                    tab,
                    feature_id=fid,
                    data=child,
                    command=self.controller.execute_feature_action
                )
                # 如果当前行剩余列不足，换行
                if current_col + colspan > total_columns:
                    current_row += 1
                    current_col = 0
                # 放置控件
                group.grid(row=current_row, column=current_col, columnspan=colspan,
                        sticky="nsew", padx=10, pady=5)
                # 更新当前列索引
                current_col += colspan
                # 保存引用
                self.feature_vars[fid] = group
            
            elif CHECK == type:
                group = LabeledCheckGroup(
                    tab,
                    feature_id=fid,
                    data=child,
                    command=self.controller.execute_feature_action
                )
                # 如果当前行剩余列不足，换行
                if current_col + colspan > total_columns:
                    current_row += 1
                    current_col = 0
                # 控件
                group.grid(row=current_row, column=current_col, columnspan=colspan, 
                           sticky="ew", padx=10, pady=5)
                # 更新当前列索引
                current_col += colspan
                self.feature_vars[fid] = group

            elif SPIN == type:
                text = child.get("text")
                spinbox = LabeledSpinBox(
                    master=tab,
                    feature_id=fid,
                    text=text,    
                    from_=0, to=9, increment=1,
                    default_value=0,
                    command=self.controller.execute_feature_action
                )
                # 如果当前行剩余列不足，换行
                if current_col + colspan > total_columns:
                    current_row += 1
                    current_col = 0

                spinbox.grid(row=current_row, column=current_col, columnspan=colspan, 
                             sticky="ew", padx=20, pady=5)
                # 更新当前列索引
                current_col += colspan
                self.feature_vars[fid] = spinbox  # 如果你要后面取值

            elif SEPARATOR == type:
                current_row += 1  
                sep = ttk.Separator(tab, orient='horizontal')
                sep.grid(row=current_row, column=0, columnspan=total_columns,
                        sticky="ew", pady=10)
                current_row += 1  
                current_col = 0   # 回到第一列

        # 均分每列权重，让控件按比例拉伸
        for i in range(total_columns):
            tab.grid_columnconfigure(i, weight=1)

    def _create_tray_icon(self):
        """创建支持双击的系统托盘图标"""
        try:
            
            
            image = Image.open(LOGO_PATH)
            
            # 创建菜单项
            menu_items = [
                pystray.MenuItem('显示主界面', self.restore_from_tray),
                pystray.MenuItem('退出', self._quit_app)
            ]
            
            # 创建托盘图标
            self.tray_icon = pystray.Icon(
                APP_FULL_NAME,
                icon=image,
                menu=pystray.Menu(*menu_items)
            )
            
            # 添加双击支持 (Windows特定实现)
            if sys.platform == 'win32':
                def win32_double_click(icon, item):
                    self.restore_from_tray()
                
                # 修改内部菜单结构以支持双击
                self.tray_icon._menu = pystray.Menu(
                    pystray.MenuItem(
                        '__DOUBLE_CLICK__', 
                        win32_double_click, 
                        default=True, 
                        visible=False
                    ),
                    *menu_items
                )
            
            self.tray_icon_running.set()
            self.tray_thread = threading.Thread(
                target=self._run_tray_icon,
                daemon=True
            )
            self.tray_thread.start()
            
        except ImportError:
            print("警告：pystray 未安装，系统托盘功能不可用")
        except Exception as e:
            print(f"创建托盘图标失败: {e}")

    def _run_tray_icon(self):
        """运行托盘图标的线程函数"""
        try:
            while self.tray_icon_running.is_set():
                try:
                    self.tray_icon.run()
                    break
                except Exception as e:
                    print(f"托盘图标运行错误: {e}")
                    time.sleep(1)
        finally:
            # 确保资源清理
            with self._tray_cleanup_lock:
                self._tray_cleanup_done = True

    def _on_destroy(self, event):
        """窗口销毁时的清理工作"""
        if event.widget == self.master:
            self._cleanup_tray_icon()

    def _cleanup_tray_icon(self):
        """清理托盘图标资源"""
        with self._tray_cleanup_lock:
            if self._tray_cleanup_done:
                return
            
            self.is_quitting = True
            self.tray_icon_running.clear()
            
            if self.tray_icon:
                try:
                    # 仅停止图标，不尝试加入线程
                    self.tray_icon.stop()
                except:
                    pass
            
            self._tray_cleanup_done = True

    def _quit_app(self, icon=None, item=None):
        """退出应用程序"""
        self._cleanup_tray_icon()

        # 保存win配置
        self.save_window_geometry()

        # 清空tz预告信息
        self.controller.file_operations.writeTerrorZone("")

        # 使用after来在主线程中安全执行退出
        self.master.after(100, self._final_quit)

    def _final_quit(self):
        """最终退出处理"""
        try:
            self.master.destroy()
        except:
            pass
        os._exit(0)

    def minimize_to_tray(self):
        """最小化到托盘"""
        if not self.is_quitting and hasattr(self, 'tray_icon') and self.tray_icon:
            self.master.withdraw()
            try:
                if hasattr(self.tray_icon, 'notify'):
                    self.tray_icon.notify("程序已最小化到托盘", APP_FULL_NAME)
            except:
                pass
    
    def wnd_proc(self, hwnd, msg, wParam, lParam):
        """在窗口类中定义消息处理"""
    
        if msg == WM_SHOW_WINDOW:
            self.restore_from_tray()  
            return 0

    def restore_from_tray(self, icon=None, item=None):
        """从托盘恢复窗口（兼容菜单点击和双击）"""
        if not self.is_quitting:
            try:
                # 确保在主线程执行UI操作
                self.master.after(0, self._do_restore_window)
            except:
                pass

    def _do_restore_window(self):
        """实际执行窗口恢复操作"""
        try:
            if not self.master.winfo_viewable():
                self.master.deiconify()
            self.master.lift()
            if self.master.state() == 'iconic':
                self.master.state('normal')
        except tk.TclError:
            pass

    def on_tab_changed(self, event):
        """修改后的标签页切换回调"""
        if hasattr(self, 'is_quitting') and self.is_quitting:
            return
            
        try:
            notebook = event.widget
            selected = notebook.tab(notebook.select(), "text")
            
            if selected in ("D2R多开器", "恐怖区域", "免责声明"):
                try:
                    self.apply_button.config(state='disabled')
                except tk.TclError:
                    pass
                if selected == "恐怖区域":
                    self.tz_tab.load_and_display_data()
            else:
                try:
                    self.apply_button.config(state='normal')
                except tk.TclError:
                    pass
        except tk.TclError:
            pass

    def update_ui_state(self, current_states: dict):
        """
        根据加载的设置更新 UI 元素的状态。
        """
        tab_fids = [
            child["fid"]
            for tab in self.all_features_config.get("tabs", [])
            for child in tab.get("children", [])
            if "fid" in child
        ]
        
        for fid, var in self.feature_vars.items():
            if fid in self.all_features_config["checkbutton"]:
                value = current_states.get(fid, False)
                var.set(value)
            elif fid in self.all_features_config["radiogroup"]:
                value = current_states.get(fid, None)
                var.set(value)
            elif fid in self.all_features_config["checkgroup"]:
                value = current_states.get(fid, [])
                var.set(value)
            elif fid in self.all_features_config["spinbox"]:
                value = current_states.get(fid, 0)
                var.set(value) 
            elif fid in self.all_features_config["checktable"]:
                value = current_states.get(fid, {})
                var.set(value)
            elif fid in tab_fids:
                value = current_states.get(fid)
                var.set(value)


    def save_window_geometry(self):
        """保存窗口配置"""
        self.master.update_idletasks()       # 确保 geometry 是最新
        geom = self.master.geometry()         # 格式: "800x600+100+200"
        size, x, y = geom.split('+')[0], geom.split('+')[1], geom.split('+')[2]
        width, height = size.split('x')
        data = {
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height)
        }
        self.controller.file_operations.save_win_config(data)

    def load_window_geometry(self):
        """加载窗口配置"""
        data = self.controller.file_operations.load_win_config()
        if data is not None:
            self.master.geometry(f"{data['width']}x{data['height']}+{data['x']}+{data['y']}")

    def add_tab(self, tab, tab_name: str):
        """添加Tab"""
        if self.notebook:
            self.notebook.add(tab, text=tab_name)
            self.tab_map[tab_name] = tab


    def hide_tab(self, tab_name: str):
        """隐藏Tab"""
        tab = self.tab_map.get(tab_name)
        if tab and str(tab) in self.notebook.tabs():
            self.notebook.tab(tab, state="hidden")


    def show_tab(self, tab_name: str):
        """显示Tab"""
        tab = self.tab_map.get(tab_name)
        if tab and str(tab) in self.notebook.tabs():
            self.notebook.tab(tab, state="normal")        


    def visible(self):
        """窗口终始化"""
        self.load_window_geometry()

        # if not "2" in self.controller.current_states["399"]:
        #     self.hide_tab("恐怖区域")

        # if not "1" in self.controller.current_states["399"]:
        #     self.hide_tab("D2R多开器")


class LabeledRadioGroup(ttk.LabelFrame):
    def __init__(self, master, feature_id, data, default_selected=None, command=None, **kwargs):
        super().__init__(master, text=data["text"], **kwargs)
        self.feature_id = feature_id
        self.command = command
        self.var = tk.StringVar(value=default_selected)

        params = data.get("params", {})
        # 如果是 list（老版本），把 list of dict 转成 dict
        if isinstance(params, list):
            merged = {}
            for item in params:
                merged.update(item)
            params = merged 

        for j, (key, label) in enumerate(params.items()):
            rb = ttk.Radiobutton(self, text=label, value=key, variable=self.var, command=self._on_select)
            rb.grid(row=0, column=j, sticky="ew", padx=5, pady=5)
            self.columnconfigure(j, weight=1)

    def _on_select(self):
        if self.command:
            self.command(self.feature_id, self.var.get())

    def get(self):
        return self.var.get()

    def set(self, key):
        self.var.set(key)

    @property
    def text(self):
        return self.cget("text")

class LabeledCheckGroup(ttk.LabelFrame):
    def __init__(self, master, feature_id, data, default_selected=None, command=None, **kwargs):
        super().__init__(master, text=data["text"], **kwargs)
        self.feature_id = feature_id
        self.command = command
        self.vars = {}

        if default_selected is None:
            default_selected = []

        params = data.get("params", {})
        # 兼容旧格式：如果是 list，则合并成 dict
        if isinstance(params, list):
            merged = {}
            for item in params:
                merged.update(item)
            params = merged

        for j, (key, label) in enumerate(params.items()):
            var = tk.BooleanVar(value=(key in default_selected))
            chk = ttk.Checkbutton(self, text=label, variable=var, command=self._on_check)
            chk.grid(row=0, column=j, sticky="ew", padx=5, pady=5)
            self.columnconfigure(j, weight=1)
            self.vars[key] = var

    def _on_check(self):
        if self.command:
            selected = self.get()
            self.command(self.feature_id, selected)

    def get(self):
        return [key for key, var in self.vars.items() if var.get()]
        # return sorted([key for key, var in self.vars.items() if var.get()])

    def set(self, selected_keys):
        if selected_keys is None:
            selected_keys = []
        for key, var in self.vars.items():
            var.set(key in selected_keys)

    @property
    def text(self):
        return self.cget("text")
    

class LabeledSpinBox(ttk.LabelFrame):
    def __init__(self, master, feature_id, text, from_=0, to=9, increment=1,
                 default_value=0, command=None, **kwargs):
        """
        :param master: 父容器
        :param feature_id: 功能id，用于回调
        :param text: LabelFrame 标题
        :param from_: 最小值
        :param to: 最大值
        :param increment: 步进
        :param default_value: 初始值
        :param command: 选值变动回调，签名为 command(feature_id, value)
        :param kwargs: 传给 ttk.LabelFrame 的其他参数
        """
        super().__init__(master, text=text, **kwargs)
        self.feature_id = feature_id
        self.command = command

        # 容器（为了控制内边距）
        spin_container = ttk.Frame(self)
        spin_container.pack(fill=tk.X, padx=15, pady=5)

        self.var = tk.IntVar(value=default_value)

        self.spin = ttk.Spinbox(
            spin_container,
            from_=from_,
            to=to,
            increment=increment,
            textvariable=self.var,
            state='readonly',
            command=self._on_change
        )
        self.spin.pack(anchor=tk.W, padx=10, pady=2)

    def _on_change(self):
        if self.command:
            self.command(self.feature_id, self.var.get())

    def get(self):
        """返回当前值"""
        return self.var.get()

    def set(self, value):
        """设置当前值"""
        self.var.set(value)


class TableWithCheckbox(tk.Frame):
    """
    Scroll-able checkbox table:
        - columns:  ['英文', '简体', '繁體', ...]
        - data:     [[id, col1, col2, ...], ...]
        - config_dict / config_key: 用来读写 {id: bool} 状态到外部字典
    """
    def __init__(self, master, columns, data,
                 config_dict=None, config_key=None,
                 col_width=14, wrap_px=0,
                 on_change=None,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.columns      = columns
        self.data         = data
        self.config_dict  = config_dict or {}
        self.config_key   = config_key
        self.on_change    = on_change

        if self.config_key and self.config_key not in self.config_dict:
            self.config_dict[self.config_key] = {}
        self.state_dict = self.config_dict[self.config_key] if self.config_key else {}

        # ---------- 滚动容器 ----------
        canvas = tk.Canvas(self, highlightthickness=0)
        vbar   = tk.Scrollbar(self, orient="vertical",   command=canvas.yview)
        hbar   = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        vbar.pack(side="right", fill="y")
        hbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        self._tbl = tk.Frame(canvas)
        tbl_window = canvas.create_window((0, 0), window=self._tbl, anchor="nw")

        # 滚轮支持
        # ---------- 滚轮支持（加这段） ----------
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows

        # ---------- 替换这部分开始 ----------
        def _on_config(event=None):
            # 当内层 Frame 尺寸变化时更新 scrollregion（不再在这里设置 window 宽度）
            canvas.configure(scrollregion=canvas.bbox("all"))

        self._tbl.bind("<Configure>", _on_config)

        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(tbl_window, width=e.width))

        # 在构建完所有控件后做一次初始刷新（延迟很短，确保 geometry 已计算）
        def _initial_update():
            # 强制布局计算后再读 bbox/winfo_width
            self._tbl.update_idletasks()
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfigure(tbl_window, width=canvas.winfo_width())

        # ---------- 构建表格 ----------
        self.vars    = []
        self.row_ids = []

        # 全选框变量 + 函数
        self._select_all_var = tk.BooleanVar(value=False)

        def _toggle_all():
            new_state = self._select_all_var.get()
            for var in self.vars:
                var.set(new_state)
            if self.on_change:
                self.on_change(self.get())  # 只通知外部

        # 表头第0列改为全选框（包Frame）
        frame = tk.Frame(self._tbl, borderwidth=1, relief="solid")
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Checkbutton(frame,
                    text="",
                    variable=self._select_all_var,
                    command=_toggle_all).pack(expand=True, fill="both")

        # 其他表头
        for j, col in enumerate(columns, start=1):
            tk.Label(self._tbl, text=col, width=col_width, wraplength=wrap_px,
                    borderwidth=1, relief="solid", anchor="w"
                    ).grid(row=0, column=j, sticky="nsew")

        # 表体
        for i, row in enumerate(data, start=1):
            rid = str(row[0])
            self.row_ids.append(rid)

            var = tk.BooleanVar(value=self.state_dict.get(rid, False))
            self.vars.append(var)

            # 包Frame
            frame = tk.Frame(self._tbl, borderwidth=1, relief="solid")
            frame.grid(row=i, column=0, sticky="nsew")
            tk.Checkbutton(frame,
                        variable=var,
                        command=self._make_callback(),
                        anchor="center").pack(expand=True, fill="both")

            for j, text in enumerate(row[1:], start=1):
                tk.Label(self._tbl, text=text, width=col_width,
                        wraplength=wrap_px, borderwidth=1, relief="solid",
                        anchor="w").grid(row=i, column=j, sticky="nsew")

        # 列均分伸缩
        for c in range(len(columns) + 1):
            self._tbl.grid_columnconfigure(c, weight=1)

        self.after(1, _initial_update)

    def get(self):
        """返回 {id: bool}"""
        return {rid: var.get() for rid, var in zip(self.row_ids, self.vars)}

    def set(self, state_dict: dict):
        """根据字典批量设定勾选状态"""
        for rid, var in zip(self.row_ids, self.vars):
            var.set(state_dict.get(rid, False))
        # 同步表头全选状态
        self._select_all_var.set(all(var.get() for var in self.vars))

    def update_config(self):
        """把当前勾选同步进外部 config_dict"""
        if self.config_key:
            self.config_dict[self.config_key] = self.get()

    def _make_callback(self):
        def callback():
            if self.on_change:
                self.on_change(self.get())
            # 行点击时自动刷新表头全选状态
            self._select_all_var.set(all(var.get() for var in self.vars))
        return callback


class D2RLauncherApp(tk.Frame):
    """
    D2R多开器
    """
    def __init__(self, master=None):
        super().__init__(master)  # 继承 Frame
        self.master = master
        self.pack(fill="both", expand=True)

        self.machine_key = self.get_machine_key()
        self.fernet = Fernet(self.machine_key)
        self.accounts = []
        self.load_config()
        self.build_ui()

    def load_config(self):
        if os.path.exists(ACCOUNTS_PATH):
            with open(ACCOUNTS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.global_config = data.get("global", {
                    "d2r_path": "",
                    "region": "kr.actual.battle.net",
                    "launch_interval": 5
                })
                encrypted_accounts = data.get("accounts", [])
                self.accounts = [self.decrypt_account_data(acc) for acc in encrypted_accounts]  # 解密后加载
        else:
            self.global_config = {
                "d2r_path": "",
                "region": "kr.actual.battle.net",
                "launch_interval": 5
            }
            self.accounts = []

    def save_config(self):
        self.sync_ui_to_config()
        self.global_config["region"] = self.region_var.get()  
        data = {
            "global": self.global_config,
            "accounts": [self.encrypt_account_data(acc) for acc in self.accounts]
        }
        with open(ACCOUNTS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def build_ui(self):
        # 全局设置区
        frame_global = ttk.LabelFrame(self, text="全局设置")
        frame_global.pack(fill="x", padx=10, pady=5)
        # logo
        self.help_img = tk.PhotoImage(file=HELP_PATH)  # 防止被GC回收
        lbl_help = tk.Label(frame_global, image=self.help_img, cursor="hand2")
        lbl_help.grid(row=0, column=3, padx=2)
        lbl_help.bind("<Button-1>", lambda e: self.open_help_link())

        # 游戏路径
        ttk.Label(frame_global, text="游戏路径:").grid(row=0, column=0, sticky="w")
        self.entry_path = ttk.Entry(frame_global, width=60)
        self.entry_path.grid(row=0, column=1, padx=5)
        self.entry_path.insert(0, self.global_config.get("d2r_path", ""))

        btn_browse = ttk.Button(frame_global, text="浏览", command=self.select_d2r_path)
        btn_browse.grid(row=0, column=2, padx=5)

        # 区服
        ttk.Label(frame_global, text="区服:").grid(row=1, column=0, sticky="w")
        self.region_var = tk.StringVar(value=self.global_config.get("region", "kr"))

        frame_region = ttk.Frame(frame_global)
        frame_region.grid(row=1, column=1, columnspan=10, sticky="w")

        for key, label in REGION_NAME_MAP.items():
            ttk.Radiobutton(
                frame_region, text=label, variable=self.region_var, value=key
            ).pack(side="left", padx=5, pady=2)
        
        # 国服禁用
        ttk.Radiobutton(
            frame_region, text="国服不能用", variable=self.region_var, value="cn", state="disabled"
        ).pack(side="left", padx=5, pady=2)

        # 启动间隔
        ttk.Label(frame_global, text="启动间隔(秒):").grid(row=2, column=0, sticky="w")
        self.entry_interval = ttk.Entry(frame_global, width=5)
        self.entry_interval.grid(row=2, column=1, sticky="w")
        self.entry_interval.insert(0, str(self.global_config.get("launch_interval", 5)))

        # 账号列表区
        self.frame_accounts = ttk.LabelFrame(self, text="账号列表")
        self.frame_accounts.pack(fill="both", expand=True, padx=10, pady=5)

        self.account_vars = []  # 每个账号行对应的控件变量，用于保存状态
        self.draw_account_table()

        # 底部按钮区
        frame_bottom = ttk.Frame(self)
        frame_bottom.pack(pady=10)

        btn_add = ttk.Button(frame_bottom, text="添加账号", command=lambda: self.edit_account(None))
        btn_add.pack(side="left", padx=5)

        btn_save = ttk.Button(frame_bottom, text="保存设置", command=self.on_save)
        btn_save.pack(side="left", padx=5)

        btn_launch_all = ttk.Button(frame_bottom, text="一键多开", command=self.launch_all_accounts)
        btn_launch_all.pack(side="left", padx=5)

        btn_kill_proc = ttk.Button(frame_bottom, text="杀进程", command=self.release_mutex)
        btn_kill_proc.pack(side="left", padx=5)

        btn_close_all = ttk.Button(frame_bottom, text="全部关闭", command=self.close_all)
        btn_close_all.pack(side="left", padx=5)

    def select_d2r_path(self):
        path = filedialog.askopenfilename(title="选择 D2R.exe", filetypes=[("D2R.exe", "D2R.exe")])
        if path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, path)

    def draw_account_table(self):
        # 清理旧控件
        for widget in self.frame_accounts.winfo_children():
            widget.destroy()
        self.account_vars.clear()

        # 设置列宽度和居中
        # 设置列权重，允许列拉伸
        for col in range(11):
            self.frame_accounts.grid_columnconfigure(col, weight=1)

        headers = ["启用", "昵称", "用户名", "Mod", "窗口", "静音", "编辑", "启动", "上移", "下移", "删除"]
        for col, h in enumerate(headers):
            ttk.Label(self.frame_accounts, text=h, font=("Arial", 10, "bold"), anchor='center').grid(row=0, column=col, padx=3, pady=3, sticky='nsew')

        for idx, acc in enumerate(self.accounts):
            row = idx + 1
            var_enabled = tk.BooleanVar(value=acc.get("enabled", False))
            chk_enabled = ttk.Checkbutton(self.frame_accounts, variable=var_enabled)
            chk_enabled.grid(row=row, column=0, sticky='nsew')
            
            self.account_vars.append(var_enabled)

            lbl_nick = ttk.Label(self.frame_accounts, text=acc.get("nickname", ""), width=15, anchor='center')
            lbl_nick.grid(row=row, column=1, sticky='nsew')

            lbl_user = ttk.Label(self.frame_accounts, text=acc.get("username", ""), width=20, anchor='center')
            lbl_user.grid(row=row, column=2, sticky='nsew')

            lbl_mod = ttk.Label(self.frame_accounts, text=acc.get("mod", ""), width=15, anchor='center')
            lbl_mod.grid(row=row, column=3, sticky='nsew')

            lbl_win = ttk.Label(self.frame_accounts, text="✅" if acc.get("windowed") else "❌", anchor='center')
            lbl_win.grid(row=row, column=4, sticky='nsew')

            lbl_mute = ttk.Label(self.frame_accounts, text="✅" if acc.get("mute") else "❌", anchor='center')
            lbl_mute.grid(row=row, column=5, sticky='nsew')

            btn_edit = ttk.Button(self.frame_accounts, text="编辑", width=6, command=lambda i=idx: self.edit_account(i))
            btn_edit.grid(row=row, column=6, sticky='nsew', padx=1)

            btn_launch = ttk.Button(self.frame_accounts, text="启动", width=6, command=lambda i=idx: self.launch_account(i))
            btn_launch.grid(row=row, column=7, sticky='nsew', padx=1)

            btn_up = ttk.Button(self.frame_accounts, text="↑", width=3, command=lambda i=idx: self.move_account(i, -1))
            btn_up.grid(row=row, column=8, sticky='nsew', padx=1)

            btn_down = ttk.Button(self.frame_accounts, text="↓", width=3, command=lambda i=idx: self.move_account(i, 1))
            btn_down.grid(row=row, column=9, sticky='nsew', padx=1)

            btn_del = ttk.Button(self.frame_accounts, text="删除", width=6, command=lambda i=idx: self.delete_account(i))
            btn_del.grid(row=row, column=10, sticky='nsew', padx=1)

    def sync_ui_to_config(self):
        self.global_config["d2r_path"] = self.entry_path.get()
        self.global_config["region"] = self.region_var.get()
        try:
            self.global_config["launch_interval"] = int(self.entry_interval.get())
        except ValueError:
            self.global_config["launch_interval"] = 5

        for idx, var_enabled in enumerate(self.account_vars):
            self.accounts[idx]["enabled"] = var_enabled.get()

    def on_save(self):
        self.sync_ui_to_config()
        self.save_config()
        messagebox.showinfo("提示", "配置已保存")

    def edit_account(self, idx=None):
        """
        idx=None 表示添加新账号，idx有值表示编辑已有账号
        """
        if idx is None:
            account = {
                "enabled": False,
                "nickname": "",
                "username": "",
                "password": "",
                "windowed": False,
                "mute": False,
                "mod": ""
            }
        else:
            account = self.accounts[idx]

        win = tk.Toplevel(self)
        win.title("添加账号" if idx is None else "编辑账号")
        win.geometry("350x300+150+150")

        labels = ["启用", "昵称", "用户名", "密码", "窗口模式", "静音", "Mod"]
        vars_ = {}

        vars_["enabled"] = tk.BooleanVar(value=account.get("enabled", False))
        vars_["nickname"] = tk.StringVar(value=account.get("nickname", ""))
        vars_["username"] = tk.StringVar(value=account.get("username", ""))
        vars_["password"] = tk.StringVar(value=account.get("password", ""))
        vars_["windowed"] = tk.BooleanVar(value=account.get("windowed", False))
        vars_["mute"] = tk.BooleanVar(value=account.get("mute", False))
        vars_["mod"] = tk.StringVar(value=account.get("mod", ""))

        for i, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)

        tk.Checkbutton(win, variable=vars_["enabled"]).grid(row=0, column=1, sticky="w")
        tk.Entry(win, textvariable=vars_["nickname"]).grid(row=1, column=1)
        tk.Entry(win, textvariable=vars_["username"]).grid(row=2, column=1)
        tk.Entry(win, textvariable=vars_["password"], show="*").grid(row=3, column=1)
        tk.Checkbutton(win, variable=vars_["windowed"]).grid(row=4, column=1, sticky="w")
        tk.Checkbutton(win, variable=vars_["mute"]).grid(row=5, column=1, sticky="w")
        tk.Entry(win, textvariable=vars_["mod"]).grid(row=6, column=1)

        def save():
            data = {
                "enabled": vars_["enabled"].get(),
                "nickname": vars_["nickname"].get(),
                "username": vars_["username"].get(),
                "password": vars_["password"].get(),
                "windowed": vars_["windowed"].get(),
                "mute": vars_["mute"].get(),
                "mod": vars_["mod"].get(),
            }
            if idx is None:
                self.accounts.append(data)
            else:
                self.accounts[idx] = data
            self.save_config()  
            self.draw_account_table()
            win.destroy()

        tk.Button(win, text="保存", command=save).grid(row=7, column=0, columnspan=2, pady=10)

        win.transient(self)
        win.grab_set()
        self.wait_window(win)

    def move_account(self, idx, direction):
        new_idx = idx + direction
        if 0 <= new_idx < len(self.accounts):
            self.accounts[idx], self.accounts[new_idx] = self.accounts[new_idx], self.accounts[idx]
            self.draw_account_table()

    def delete_account(self, idx):
        if messagebox.askyesno("确认", "确定删除该账号？"):
            if 0 <= idx < len(self.accounts):
                del self.accounts[idx]
                self.draw_account_table()
                self.save_config()

    def launch_account(self, idx):
        acc = self.accounts[idx]
        nickname = acc.get("nickname", f"账号{idx+1}")
        print(f"准备启动账号: {nickname} ({acc.get('username')})")

        # 线程启动
        threading.Thread(target=self._handle_and_launch, args=(acc,), daemon=True).start()

    def _handle_and_launch(self, acc):
        self.release_mutex()  # 你的 handle64.exe 操作
        d2r_path = self.global_config.get("d2r_path", "")
        if not d2r_path or not os.path.exists(d2r_path):
            messagebox.showerror("错误", f"游戏路径不存在：{d2r_path}")
            return
        region_key = self.global_config.get("region", "kr")
        region_domain = REGION_DOMAIN_MAP.get(region_key, "kr.actual.battle.net")

        args = [
            d2r_path,
            "-username", acc.get("username", ""),
            "-password", acc.get("password", ""),
            "-address", region_domain
        ]

        if acc.get("windowed"):
            args.append("-w")
        if acc.get("mute"):
            args.append("-ns")
        if acc.get("mod"):
            args += ["-mod", acc["mod"], "-txt"]

        try:
            proc = subprocess.Popen(args)
            print(f"启动成功: PID {proc.pid}")

            time.sleep(3)  # 等待窗口创建
            self.rename_d2r_window_by_pid(proc.pid, region_key, acc.get("nickname", ""), acc.get("mod", ""))
        except Exception as e:
            print(f"启动失败: {e}")

    def release_mutex(self):
        try:
            cmd_list = [str(HANDLE64_PATH), "-a", "Check For Other Instances", "-nobanner"]
            print(f"执行命令: {' '.join(cmd_list)}")

            result = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            output_lines = result.stdout.splitlines()

            for line in output_lines:
                parts = line.split()
                if len(parts) >= 6:
                    pid, handle = parts[2], parts[5]
                    subprocess.run([str(HANDLE64_PATH), "-p", pid, "-c", handle, "-y"], stdout=subprocess.DEVNULL)
            print("释放互斥体成功")
        except subprocess.TimeoutExpired:
            print("调用 handle64 超时")
        except Exception as e:
            print(f"释放互斥体失败: {e}")

    def launch_all_accounts(self):
        self.sync_ui_to_config()
        self.save_config()

        def launcher():
            for idx, acc in enumerate(self.accounts):
                if acc.get("enabled"):
                    self.launch_account(idx)
                    time.sleep(self.global_config.get("launch_interval", 5))

        threading.Thread(target=launcher, daemon=True).start()

    def close_all(self):
        if messagebox.askyesno("确认", "确定关闭所有D2R窗口?"):
            subprocess.run(["taskkill", "/IM", "D2R.exe", "/F"], shell=True)

    def rename_d2r_window_by_pid(self, pid, region_key, nickname, mod):
        region_name = REGION_NAME_MAP.get(region_key, region_key)
        title = f"{region_name}.{nickname}"
        if mod:
            title += f".{mod}"

        def callback(hwnd, lParam):
            try:
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                if window_pid == lParam:  # 使用 lParam 传递 pid
                    win32gui.SetWindowText(hwnd, title)
                    return False  # 找到目标窗口后停止枚举
            except Exception as e:
                print(f"窗口处理失败: {e}")
            return True  # 继续枚举其他窗口

        win32gui.EnumWindows(callback, pid)  # 把 pid 作为 lParam 传入

    def encrypt_account_data(self, account: dict) -> dict:
        encrypted = account.copy()
        for key in ['username', 'password']:
            val = encrypted.get(key, "")
            if val and not val.startswith("gAAAA"):  # 判断是否已经加密
                encrypted[key] = self.encrypt(val)
        return encrypted
    
    def decrypt_account_data(self, account: dict) -> dict:
        decrypted = account.copy()
        for key in ['username', 'password']:
            decrypted[key] = self.decrypt(decrypted.get(key, ""))
        return decrypted

    def get_machine_key(self) -> bytes:
        """
        获取本机唯一密钥（基于 MAC 地址派生）
        """
        node = uuid.getnode()
        raw = str(node).encode()
        sha = hashlib.sha256(raw).digest()
        return base64.urlsafe_b64encode(sha[:32])  # Fernet 需要 32-byte base64 key

    def encrypt(self, text: str) -> str:
        """
        加密文本（UTF-8） → base64编码密文
        """
        f = Fernet(self.get_machine_key())
        return f.encrypt(text.encode()).decode()

    def decrypt(self, token: str) -> str:
        """
        解密 base64密文 → 原始文本；解密失败返回原始字符串
        """
        f = Fernet(self.get_machine_key())
        try:
            return f.decrypt(token.encode()).decode()
        except InvalidToken:
            return token  # 可能是明文
        
    def open_help_link(self):
        url = "https://bbs.d.163.com/forum.php?mod=viewthread&tid=175119207&page=5#pid218155737"
        webbrowser.open(url)
        
class TerrorZoneUI(tk.Frame):
    def __init__(self, master, controller, fetcher=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.fetcher = fetcher  # TerrorZoneFetcher实例
        self.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_and_display_data()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("time", "name"), show="headings")
        self.tree.heading("time", text="时间")
        self.tree.heading("name", text="恐怖地带")
        self.tree.column("time", width=150, anchor=tk.CENTER)
        self.tree.column("name", width=350, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_and_display_data(self):
        if not os.path.isfile(TERROR_ZONE_PATH):
            return

        try:
            with open(TERROR_ZONE_PATH, "r", encoding="utf-8") as f:
                full_data = json.load(f)
            data_list = full_data.get("data", [])

            self.tree.delete(*self.tree.get_children())

            for item in data_list:
                if isinstance(item, dict):
                    zone_key = item.get("zone")
                    raw_time = item.get("time")
                    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(raw_time)) if raw_time else "未知时间"
                    if not zone_key:
                        continue
                    zone_info = TERROR_ZONE_DICT.get(zone_key)
                    if isinstance(zone_info, dict):
                        language =self.controller.current_states[TERROR_ZONE_LANGUAGE]
                        name = zone_info.get(language)
                    else:
                        name = "未知名称"
                    self.tree.insert("", "end", values=(formatted_time, name))
        except Exception as e:
            messagebox.showerror("错误", f"加载数据失败: {e}")

    def manual_refresh(self):
        if not self.fetcher:
            messagebox.showerror("错误", "未初始化数据获取器")
            return
        
        def do_fetch():
            try:
                self.fetcher.fetch_manual(ui_refresh_func=lambda data: self.master.after(0, self.load_and_display_data))
            except Exception as e:
                self.master.after(0, lambda: messagebox.showerror("错误", f"刷新失败: {e}"))
        
        threading.Thread(target=do_fetch, daemon=True).start()