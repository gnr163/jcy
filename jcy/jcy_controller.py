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

# ---- UAC ----
def is_admin():
    """UAC检查"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
if not is_admin():
    # 重新以管理员权限启动自己
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

# ---- 单例检查----
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

class FeatureController:
    def __init__(self, master):
        self.master = master
        self.current_states = {}
        self.dialogs = "" 
        self.feature_config = FeatureConfig()
        self.file_operations = FileOperations(self.feature_config)
        self.feature_state_manager = FeatureStateManager(self.feature_config)

        # 无配置文件,以默认文件为准
        if not os.path.exists(USER_SETTINGS_PATH):
            os.makedirs(os.path.dirname(USER_SETTINGS_PATH), exist_ok=True)
            shutil.copyfile(DEFAULT_SETTINGS_PATH, USER_SETTINGS_PATH)

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
        else:
            print("[DEBUG] 配置已是最新版本")

        
        # 恐怖区域更新
        self.terror_zone_fetcher = TerrorZoneFetcher()
        # 初始化 UI（内部需要用到 current_states）
        self.feature_config.all_features_config
        self.feature_view = FeatureView(master, self.feature_config.all_features_config, self)

        # ???
        self.feature_state_manager.load_settings()
        self.current_states = copy.deepcopy(self.feature_state_manager.loaded_states)
        self.feature_view.update_ui_state(self.current_states)

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
                handler(default_value)
        
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
            # "点击角色快速建立最高难度游戏",
            "101": self.file_operations.toggle_quick_game,
            # "Esc=存儲並離開",
            "102": self.file_operations.toggle_escape,
            # "更大的好友菜单",
            "103": self.file_operations.toggle_context_menu,
            # "特殊词缀蓝装变色(红/绿)",
            "104": self.file_operations.toggle_global_excel_affixes,
            # "经验祭坛/宝石祭坛 特效标识",
            "106": self.file_operations.toggle_shrine,
            # "暗黑2百科",
            "107": self.file_operations.toogle_d2r_wiki,
            # "物品栏+精品词缀",
            "108": self.file_operations.toggle_inventory_expansion,
            # "储物箱+精品词缀",
            "109": self.file_operations.toggle_bank_expansion,
            # "赫拉迪姆方塊+符文升级公式",
            "110": self.file_operations.toogle_cube_formula,
            # "MINI方块常开before蓝球",
            "111": self.file_operations.toggle_mini_cube,
            # "画面变亮",
            "112": self.file_operations.toggle_env_vis,
            # "蓝怪/金怪/暗金怪随机染色",
            "113": self.file_operations.toggle_hd_global_palette_randtransforms_json,
            # "怪物光源+危险标识",
            "114": self.file_operations.toggle_character_enemy,
            # "屏蔽 劣等的/損壞的/破舊的武器装备",
            "115": self.file_operations.toggle_low_quality,
            # "咒符/22#+符文增加掉落光柱",
            "117": self.file_operations.toggle_droped_highlight, 
            # "咒符/22#+符文增加掉落提示音 & 技能结束提示音",
            "118": self.file_operations.toggle_sound,
            # "技能图标(头顶:熊之印记/狼之印记 脚下:附魔/速度爆发+影散/BO 右侧:刺客聚气)",
            "119": self.file_operations.toggle_skill_logo,
            # "A1兵营/A4火焰之河/A5尼拉塞克/BOSS 指引",
            "120": self.file_operations.toggle_pointer,
            # "交互对象增加蓝色火苗",
            "121": self.file_operations.toggle_chest_highlight, 
            # "马赛克护眼",
            "122": self.file_operations.toggle_no_mosaic_sin,
            # "6BOSS钥匙皮肤+掉落光柱",
            "124": self.file_operations.toggle_mephisto_key,
            # "屏蔽 开场/过场/结束动画",
            "125": self.file_operations.toggle_hd_local_video,
            # "屏蔽 地狱火炬火焰风暴特效",
            "126": self.file_operations.toggle_hellfire_torch,
            # "屏蔽 A4火焰之河岩浆特效",
            "127": self.file_operations.toggle_lava_river_flow,
            # "屏蔽 A5督军山克死亡特效",
            "128": self.file_operations.toggle_shenk,
            # "屏蔽 开门动画,极速进站",
            "129": self.file_operations.toggle_load_screen_panel,
            # "展示 A2贤者之谷小站塔墓标记 & 屏蔽 A3崔凡克议会墙屋/A4混沌庇护所大门/A5毁灭王座石柱",
            "130": self.file_operations.toggle_hd_env_presets,
            # "经验条变色",
            "131": self.file_operations.toggle_experience_bar,
            # "屏蔽 影散隐身特效",
            "132": self.file_operations.toggle_fade_dummy,
            # "屏蔽 头环类装备外观",
            "133": self.file_operations.toggle_circlet,
            # "屏蔽 雷云风暴吓人特效",
            "134": self.file_operations.toggle_lightningbolt_big,
            # "降低 闪电新星亮度",
            "135": self.file_operations.toggle_electric_nova,
            # "怪物血条加宽加高",
            "136": self.file_operations.toggle_monster_health,
            # "死灵召唤骷髅 火焰刀+圣盾特效",
            "137": self.file_operations.toggle_necroskeleton,
            # "投掷标枪->闪电枪特效",
            "138": self.file_operations.toggle_missiles_javelin,
            # "投掷飞刀->闪电尾特效",
            "139": self.file_operations.toggle_missiles_throw,
            # "德鲁伊飓风术 特效",
            "140": self.file_operations.toggle_hurricane,
            # "左键快速购买",
            "141": self.file_operations.toggle_quick_buy,
            # "入口 箭头指引",
            "142": self.file_operations.toggle_roomtiles_arrow,
            # "小站 箭头指引",
            "143": self.file_operations.toggle_waypoint_arrow,
            
            
            # 佣兵图标位置
            "201": self.file_operations.select_hireables_panel,
            # 传送门皮肤
            "202": self.file_operations.select_town_portal,
            # 传送术皮肤
            "203": self.file_operations.select_teleport_skin,
            # 弩/箭皮肤
            "204": self.file_operations.select_arrow_skin,
            # 老鼠刺针/剥皮吹箭样式
            "205": self.file_operations.select_enemy_arrow_skin,
            # 符文皮肤
            "206": self.file_operations.select_rune_skin,
            

            #角色特效
            "301": self.file_operations.select_character_effects,
            # 属性词条特效
            "302": self.file_operations.select_entry_effects,
            # 装备名称特效
            "303": self.file_operations.select_item_name_effects,

            # 照亮范围
            "401": self.file_operations.modify_character_player,
            # 22#+符文名称大小
            "402": self.file_operations.modify_rune_rectangle,

            # 道具屏蔽
            "501": self.file_operations.modify_item_names,
        }

    def apply_settings(self):
        """
        应用所有功能设置，执行文件操作。
        此方法被“应用设置”按钮调用。
        保留用户原有的比较逻辑和对话框显示机制。
        """
        self.dialogs = "" # 每次应用设置前清空 dialogs
        changes_detected = False

        # -------------------- 独立功能 (Checkbutton) --------------------
        for feature_id, description in self.feature_config.all_features_config["checkbutton"].items():
            current_value = self.current_states.get(feature_id)
            loaded_value = self.feature_state_manager.loaded_states.get(feature_id)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                if feature_id in self._handlers:
                    result = self._handlers[feature_id](current_value) 
                    self.dialogs += f"{description} = {'开启' if current_value else '关闭'} 操作文件数量 {result[0]}/{result[1]} \n"



        # -------------------- 单选功能 (RadioGroup) --------------------
        for fid, info in self.feature_config.all_features_config["radiogroup"].items():
            current_value = self.current_states.get(fid)
            loaded_value = self.feature_state_manager.loaded_states.get(fid)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                selected_description = next((param_dict[current_value] for param_dict in info["params"] if current_value in param_dict), current_value)
                if fid in self._handlers:
                    result = self._handlers[fid](current_value)
                    self.dialogs += f"{info['text']} = {selected_description} 操作文件数量 {result[0]}/{result[1]} \n"


        # -------------------- 多选功能 (CheckGroup) --------------------
        for fid, info in self.feature_config.all_features_config["checkgroup"].items():
            current_value = self.current_states.get(fid)
            loaded_value = self.feature_state_manager.loaded_states.get(fid)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                if fid in self._handlers:
                    result = self._handlers[fid](current_value)
                    self.dialogs += f"{info['text']} 操作文件数量 {result[0]}/{result[1]} \n"


        #  -------------------- 区间功能 (Spinbox) --------------------
        for feature_id, description in self.feature_config.all_features_config["spinbox"].items():
            current_value = self.current_states.get(feature_id)
            loaded_value = self.feature_state_manager.loaded_states.get(feature_id)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                if feature_id in self._handlers:
                    result = self._handlers[feature_id](current_value) 
                    self.dialogs += f"{description} = {current_value} 操作文件数量 {result[0]}/{result[1]} \n"

        # -- 屏蔽道具 --
        for fid, info in self.feature_config.all_features_config["checktable"].items():
            current_value = self.current_states.get(fid)
            loaded_value = self.feature_state_manager.loaded_states.get(fid)
            if current_value is not None and current_value != loaded_value:
                changes_detected = True
                if fid in self._handlers:
                    result = self._handlers[fid](current_value)
                    self.dialogs += f"{info} 操作文件数量 {result[0]}/{result[1]} \n"
        

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
    def __init__(self, n_times_per_hour=5):
        self.running = False
        self.first = True
        self.thread = None
        self.n_times_per_hour = n_times_per_hour

    def fetch_once_with_retry(self, max_retries=9):
        """
        爬取TZ最新数据
        """
        randint = random.randint(0, 1)
        for attempt in range(1, max_retries + 1):
            try:
                api = TERROR_ZONE_API[randint % 2]
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
            time.sleep(random.randint(3, 10))

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
                    print(f"[保存] 数据已保存到 {TERROR_ZONE_PATH}")
                except Exception as e:
                    print(f"[错误] 保存数据失败: {e}")

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
    root = tk.Tk()

    app = FeatureController(root)

    root.iconbitmap(LOGO_PATH)
    
    # 恐怖区域数据更新回调
    def notify_fetch_success(data):
        print("[通知] 恐怖区域数据更新成功！")
        try:
            rec = data["data"][0]
            raw_time = rec.get("time")
            zone_key = rec.get("zone")
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(raw_time)) if raw_time else "未知时间"
            
            zone_info = TERROR_ZONE_DICT.get(zone_key, {})
            zone_name = zone_info.get(LANG, zone_info.get(ENUS)) if zone_info else f"未知区域（{zone_key}）"
            message = f"{formatted_time} {zone_name}"
        except Exception as e:
            print("[通知构造异常]", e)
            message = "恐怖区域数据更新成功，但部分信息解析失败。"

        toast("恐怖区域已更新", message)

    # 启动自动获取恐怖区域数据的后台线程
    app.terror_zone_fetcher.start_auto_fetch_thread(notify_fetch_success)

    root.mainloop()