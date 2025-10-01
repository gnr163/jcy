import copy
import ctypes
import json
import os
import random
import requests
import shutil
import sys
import threading
import time
import tkinter as tk
from datetime import datetime, timedelta, timezone
from tkinter import messagebox
from win11toast import toast
import subprocess

from file_operations import FileOperations
from jcy_constants import *
from jcy_model import FeatureConfig, FeatureStateManager
from jcy_paths import *
from jcy_view import FeatureView

class FeatureController:
    def __init__(self, master):
        self.master = master
        self.dialogs = "" 

        # 无配置文件,以默认文件为准
        if not os.path.exists(USER_SETTINGS_PATH):
            os.makedirs(os.path.dirname(USER_SETTINGS_PATH), exist_ok=True)
            shutil.copyfile(DEFAULT_SETTINGS_PATH, USER_SETTINGS_PATH)

        # 加载配置文件
        self.feature_config = FeatureConfig()
        self.feature_state_manager = FeatureStateManager(self.feature_config)
        self.feature_state_manager.load_settings()
        self.current_states = copy.deepcopy(self.feature_state_manager.loaded_states)

        # 文件操作类
        self.file_operations = FileOperations(self)
        # 同步APP信息到JSON
        self.file_operations.sync_app_data()
        # 注册控制器方法
        self._setup_feature_handlers()

        # 升级检查
        print("[DEBUG] 初始化配置系统...")
        need_upgrade = ensure_appdata_files()
        print(f"[DEBUG] 需要升级: {need_upgrade}")
        if need_upgrade:
            self._upgrade_config()
            self.current_states = copy.deepcopy(self.feature_state_manager.loaded_states)
        else:
            print("[DEBUG] 配置已是最新版本")

        # 恐怖区域更新
        self.terror_zone_fetcher = TerrorZoneFetcher(self)

        # 初始化 UI (根据jcy_model, 并设置默认值)
        self.feature_config.all_features_config
        self.feature_view = FeatureView(master, self.feature_config.all_features_config, self)

        # 按照配置更新到UI
        self.feature_view.update_ui_state(self.current_states)

        # 按配置显/隐面板
        self.feature_view.visible()

    def getCurrentState(self, key):
        return self.current_states.get(key)
    

    def _upgrade_config(self):
        """执行完整的配置升级流程"""
        toast("版本升级", "正在升级配置文件...", audio={'silent': True})
        
        # 加载配置
        default_config = load_default_config()
        user_config = load_user_config()
        
        # 合并配置
        merged_config, diff = merge_configs(default_config, user_config)
        print(f"[升级] 配置差异: {diff}")
        
        # 保存合并后的配置文件
        self.feature_state_manager.save_settings(merged_config)
        self.feature_state_manager.load_settings()

        # 应用差异到Mod
        self._apply_config_diff(diff)
        
        toast("升级完成", f"已按照用户配置更新Mod文件", audio={'silent': True})

    def _apply_config_diff(self, diff: dict):
        """实际应用配置差异到Mod文件"""
        # 处理新增配置项
        for feature_id in diff['added']:
            if handler := self._handlers.get(feature_id):
                default_value = self._get_default_value(feature_id)
                print(f"[升级] 应用新增配置 {feature_id} = {default_value}")
                # handler(default_value)
        
        # 处理修改项（保持用户设置）
        for feature_id in diff['modified']:
            if handler := self._handlers.get(feature_id):
                user_value = self.feature_state_manager.loaded_states.get(
                    feature_id,
                    self._get_default_value(feature_id)
                )
                print(f"[升级] 保持用户配置 {feature_id} = {user_value}")
                handler(user_value)

    def _get_default_value(self, feature_id: str):
        """获取功能的默认值"""
        # 根据feature_config实现具体逻辑
        config = self.feature_config.all_features_config
        if feature_id in config["checkbutton"]:
            return False
        elif feature_id in config["radiogroup"]:
            return list(config["radiogroup"][feature_id]["params"][0].keys())[0]
        elif feature_id in config["spinbox"]:
            return config["spinbox"][feature_id]["from_"]
        elif feature_id == "501":  # 道具屏蔽
            return {}
        return None


    
    def _setup_feature_handlers(self):
        """
        设置功能ID与对应的操作方法的映射。
        """
        
        self._handlers = {
            # 道具屏蔽
            "501": self.file_operations.modify_item_names,
            # 恐怖区域-服务器
            TERROR_ZONE_SERVER: self.file_operations.select_server,
            # 恐怖区域-语言
            TERROR_ZONE_LANGUAGE: self.file_operations.select_language,
            # 恐怖区域-预告
            TERROR_ZONE_NEXT: self.file_operations.void,
            # 网易国服语言翻译(装备/道具/符文/符文之语)
            NETEASE_LANGUAGE: self.file_operations.select_netease_language,
            # 暴雪国际服语言翻译(装备/道具/符文/符文之语)
            BATTLE_NET_LANGUAGE: self.file_operations.select_battle_net_language,
            # 游戏设置
            GAME_SETTING: self.file_operations.select_game_setting,
            # 游戏设置2
            GAME_SETTING2: self.file_operations.select_game_setting2,
            # 控件设置
            CONTROLS_SETTING: self.file_operations.select_controls_setting,
            # 额外的照亮范围
            LIGHT_REDIUS: self.file_operations.modify_character_player,
            # HUD面板缩放
            HUD_SIZE: self.file_operations.select_hudpanel_size,
            # 传送门皮肤
            PORTAL_SKIN: self.file_operations.select_town_portal,
            # 角色特效
            CHARACTER_EFFECTS: self.file_operations.select_character_effects,
            # 弓/弩箭皮肤
            ARROW: self.file_operations.select_arrow_skin,
            # 魔法师
            SOR_SETTING: self.file_operations.sorceress_setting,
            # 传送术皮肤
            TELEPORT_SKIN: self.file_operations.select_teleport_skin,
            # 死灵法师
            NEC_SETTING: self.file_operations.necromancer_setting,
            # 德鲁伊
            DRU_SETTING: self.file_operations.druid_setting,
            # 刺客
            ASN_SETTING: self.file_operations.assassin_setting,
            # 通用设置
            COMMON_SETTING: self.file_operations.common_setting,
            # 佣兵-配置
            MERCENARY: self.file_operations.select_mercenary_skin,
            # 佣兵-图标位置
            MERCENARY_LOCATION: self.file_operations.select_hireables_panel,
            # 怪物-配置
            MONSTER_SETTING: self.file_operations.select_monster_setting,
            # 怪物-导弹
            MONSTER_MISSILE: self.file_operations.select_enemy_arrow_skin,
            # 装备-特效
            EQIUPMENT_EFFECTS: self.file_operations.select_equipment_effects,
            # 装备-设置
            EQIUPMENT_SETTING: self.file_operations.select_equipment_setting,
            # 装备-词缀特效
            AFFIX_EFFECTS: self.file_operations.select_affix_effects,
            # 装备-模型特效
            MODEL_EFFECTS: self.file_operations.select_model_eccects,
            # 符文皮肤
            RUNE_SKIN: self.file_operations.select_rune_skin,
            # 掉落光柱提醒
            DROPED_LIGHT: self.file_operations.select_droped_light,
            # 22#+符文名称大小(越大越容易发现/选中)
            RUNE_SIZE: self.file_operations.modify_rune_rectangle,
            # 语音提示
            SOUND_PROMPTS: self.file_operations.toggle_sound,
            # 火炬钥匙
            TORCH_KEY: self.file_operations.torch_key,
            # 环境-关闭特效
            DISABLE_EFFECTS: self.file_operations.hide_environmental_effects,
            # 环境-开启指引
            ENABLE_POINTER: self.file_operations.show_environmental_pointer,
        }

    def apply_settings(self):
        """
        应用所有功能设置，执行文件操作。
        此方法被“应用设置”按钮调用。
        保留用户原有的比较逻辑和对话框显示机制。
        """
        self.dialogs = "" # 每次应用设置前清空 dialogs
        changes_detected = False

        # -------------------- 自定义面板功能 --------------------
        for tab in self.feature_config.all_features_config.get("tabs"):
            for child in tab.get("children"):
                fid = child.get("fid")
                text = child.get("text")
                type = child.get("type")

                current_value = self.current_states.get(fid)
                loaded_value = self.feature_state_manager.loaded_states.get(fid)
                if current_value is not None and current_value != loaded_value:
                    changes_detected = True
                    if fid in self._handlers:
                        result = self._handlers[fid](current_value) 
                        if "radio" == type:
                            selected_description = next((param_dict[current_value] for param_dict in child["params"] if current_value in param_dict), current_value)
                            self.dialogs += f"{text} = {selected_description} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"
                        else:
                            self.dialogs += f"{text} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"


        # -------------------- 独立功能 (Checkbutton) --------------------
        for feature_id, description in self.feature_config.all_features_config["checkbutton"].items():
            current_value = self.current_states.get(feature_id)
            loaded_value = self.feature_state_manager.loaded_states.get(feature_id)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                if feature_id in self._handlers:
                    result = self._handlers[feature_id](current_value) 
                    self.dialogs += f"{description} = {'开启' if current_value else '关闭'} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"



        # -------------------- 单选功能 (RadioGroup) --------------------
        for fid, info in self.feature_config.all_features_config["radiogroup"].items():
            current_value = self.current_states.get(fid)
            loaded_value = self.feature_state_manager.loaded_states.get(fid)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                selected_description = next((param_dict[current_value] for param_dict in info["params"] if current_value in param_dict), current_value)
                if fid in self._handlers:
                    result = self._handlers[fid](current_value)
                    self.dialogs += f"{info['text']} = {selected_description} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"


        # -------------------- 多选功能 (CheckGroup) --------------------
        for fid, info in self.feature_config.all_features_config["checkgroup"].items():
            current_value = self.current_states.get(fid)
            loaded_value = self.feature_state_manager.loaded_states.get(fid)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                if fid in self._handlers:
                    result = self._handlers[fid](current_value)
                    self.dialogs += f"{info['text']} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"


        #  -------------------- 区间功能 (Spinbox) --------------------
        for feature_id, description in self.feature_config.all_features_config["spinbox"].items():
            current_value = self.current_states.get(feature_id)
            loaded_value = self.feature_state_manager.loaded_states.get(feature_id)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                if feature_id in self._handlers:
                    result = self._handlers[feature_id](current_value) 
                    self.dialogs += f"{description} = {current_value} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"

        # -- 屏蔽道具 --
        for fid, info in self.feature_config.all_features_config["checktable"].items():
            current_value = self.current_states.get(fid)
            loaded_value = self.feature_state_manager.loaded_states.get(fid)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                if fid in self._handlers:
                    result = self._handlers[fid](current_value)
                    self.dialogs += f"{info} 操作文件数量 {result[0]}/{result[1]} {result[2] if len(result) > 2 else ''}\n"
        

        # 保存当前状态到 settings.json
        self.feature_state_manager.save_settings(self.current_states)
        # 核心：保存后，立即更新 loaded_states，使其反映当前已保存的状态
        # self.feature_state_manager.loaded_states.update(self.current_states) # 使用 update 方法
        self.feature_state_manager.loaded_states = copy.deepcopy(self.current_states)

        # 显示结果
        if changes_detected:
            messagebox.showinfo("设置已应用", self.dialogs)
        else:
            messagebox.showinfo("完成", "无变化!")

    def execute_feature_action(self, feature_id: str, value):
        self.current_states[feature_id] = value
    
    def open_appdata(self):
        subprocess.Popen(f'explorer "{CONFIG_PATH}"')  # 打开目录（Windows）


class TerrorZoneFetcher:
    def __init__(self, controller: FeatureController):
        self.running = False
        self.first = True
        self.thread = None
        self.controller = controller

    def fetch_once_with_retry(self, max_retries=20):
        """
        爬取TZ最新数据
        """
        randint = random.randint(0, 1)
        for attempt in range(1, max_retries + 1):
            try:
                # 区服配置
                server_cfg = self.controller.current_states[TERROR_ZONE_SERVER]
                api_array = TERROR_ZONE_API[server_cfg]
                api = api_array[randint % len(api_array)]

                print(f"[尝试] 第 {attempt} 次抓取 {api}")
                response = requests.get(api, timeout=10)
                response.raise_for_status()
                json_data = response.json()

                # 1. 检查 status 和 data
                if json_data.get("status") != "ok" or not json_data.get("data"):
                    print(f"[失败] 数据格式异常: {json_data}")
                else:
                    # 2. 解析时间戳（UTC时间）
                    tz_time = json_data["data"][0]["time"]
                    target_hour = datetime.fromtimestamp(tz_time, tz=timezone.utc).hour

                    # 3. 当前 UTC 时间 + 1
                    current_hour = datetime.now(timezone.utc).hour
                    expected_hour = (current_hour + 1) % 24

                    # 4. 判断是否为“下一个小时”
                    if target_hour == expected_hour:
                        print("[成功] 恐怖区域数据抓取成功（为下一个小时）")
                        return json_data
                    else:
                        print(f"[失败] 数据未更新：目标小时={target_hour}，当前+1={expected_hour}")
            except Exception as e:
                print(f"[异常] 第 {attempt} 次抓取失败: {e}")

            randint += 1
            time.sleep(random.randint(5 * attempt, 10 * attempt))

        print("[错误] 所有尝试均失败或数据未更新")
        return None

    def _run_fetch_loop(self, callback):
        print("[启动] 恐怖区域自动抓取线程已启动")
        self.running = True

        while self.running:
            if self.first:
                self.first = False
                print("[首次] 程序启动，立即执行一次抓取")
            else:
                now = datetime.now()
                target = now.replace(minute=0, second=30, microsecond=0)
                if now > target:
                    # 超过当前小时，推到下一个小时
                    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=30, microsecond=0)
                    target = next_hour

                wait_seconds = (target - now).total_seconds()
                print(f"[等待] 距离下次整点触发还有 {wait_seconds} 秒")
                time.sleep(wait_seconds)

                delay = random.randint(30, 90)
                print(f"[延迟] 随机延迟 {delay} 秒后开始抓取")
                time.sleep(delay)

            data = self.fetch_once_with_retry()

            if data:
                try:
                    with open(TERROR_ZONE_PATH, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                        
                        # 游戏内预告
                        if "2" in self.controller.current_states[TERROR_ZONE_NEXT]:
                            self.controller.file_operations.writeTerrorZone(data)
                        else:
                            self.controller.file_operations.writeTerrorZone("")

                    print(f"[保存] 数据已保存到 {TERROR_ZONE_PATH}")
                except Exception as e:
                    print(f"[错误] 保存数据失败: {e}")

                # Win系统通知
                if "1" in self.controller.current_states[TERROR_ZONE_NEXT]:
                    if callback:
                        callback(data)
            else:
                print("[提示] 当前时间点抓取失败，等待下个整点再尝试")

    def start_auto_fetch_thread(self, callback):
        if self.thread and self.thread.is_alive():
            print("[提示] 自动抓取线程已在运行")
            return

        self.thread = threading.Thread(target=self._run_fetch_loop, args=(callback,), daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

if not getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # ---- UAC ---- 
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

    # ---- 单例检查 ----
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    if kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        print("已有实例运行中, 显示实例窗口...")
        # 查找已有实例的主窗口
        hwnd = user32.FindWindowW(None, APP_FULL_NAME)  
        if hwnd:
            # 发送自定义消息通知已有实例显示窗口
            user32.SendMessageW(hwnd, WM_SHOW_WINDOW, 0, 0)
            # 激活已有实例窗口
            user32.ShowWindow(hwnd, 1)  # SW_SHOWNORMAL
        sys.exit(0)

    root = tk.Tk()
    root.iconbitmap(LOGO_PATH)
    app = FeatureController(root)
    
    # 恐怖区域数据更新回调
    def notify_fetch_success(data):
        print("[通知] 恐怖区域数据更新成功！")
        try:
            rec = data["data"][0]
            raw_time = rec.get("time")
            zone_key = rec.get("zone")
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(raw_time)) if raw_time else "未知时间"
            
            zone_info = TERROR_ZONE_DICT.get(zone_key, {})
            language = app.current_states[TERROR_ZONE_LANGUAGE]
            zone_name = zone_info.get(language) if zone_info else f"未知区域（{zone_key}）"
            message = f"{formatted_time} {zone_name}"
        except Exception as e:
            print("[通知构造异常]", e)
            message = "恐怖区域数据更新成功，但部分信息解析失败。"

        toast("恐怖区域已更新", message)

    # 启动自动获取恐怖区域数据的后台线程
    app.terror_zone_fetcher.start_auto_fetch_thread(notify_fetch_success)

    root.mainloop()