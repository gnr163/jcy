import os
from pathlib import Path
import json
import sys
from jcy_constants import *

def get_config_path() -> Path:
    """
    获取配置路径
    - 打包模式: C:/Users/{用户名}/AppData/Local/{APP_NAME}
    - 开发模式: 当前项目 assets 文件夹
    """
    if getattr(sys, 'frozen', False):
        base_dir = Path(os.environ["LOCALAPPDATA"]) / D2R_MOD_JCY
        base_dir.mkdir(parents=True, exist_ok=True)
    else:
        base_dir = Path(__file__).resolve().parent / "assets"
    return base_dir


def get_assets_file(relative_path: str) -> Path:
    """
    获取内置静态资源文件路径
    - 打包模式: PyInstaller 解包到 sys._MEIPASS
    - 开发模式: 项目 assets 文件夹
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS) / "assets"
    else:
        base_path = Path(__file__).resolve().parent / "assets"
    return base_path / relative_path


def get_bin_file(relative_path: str) -> Path:
    """
    获取外部可执行/二进制文件路径
    - 打包模式: PyInstaller 解包到 sys._MEIPASS/bin
    - 开发模式: 项目 bin 文件夹
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS) / "bin"
    else:
        base_path = Path(__file__).resolve().parent / "bin"
    return base_path / relative_path


def get_data_file(relative_path: str) -> Path:
    """
    获取外部可写文件路径（例如 mod 文件）
    - 打包模式: exe 所在目录
    - 开发模式: 当前项目目录
    """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path


# --- 文件名 ---
# 用户配置路径 C:/Users/{用户名}/AppData/Local/D2R_Mod_jcy
D2R_MOD_JCY = "D2R_Mod_jcy"
# MOD目录
JCY_DOT_MPQ = "jcy.mpq"

# --- 配置文件 ---
# 版本文件
DOT_VERSION = ".version"
# 账号文件
ACCOUNTS_JSON = "accounts.json"
# 用户配置文件
SETTINGS_JSON = "settings.json"
# 恐怖地带文件
TERROR_ZONE_JSON = "terror_zone.json"
# 窗口配置文件
WIN_JSON = "win.json"
# --- ASSETS文件 ---
# LOGO
BEAR_ICO = "bear.ico"
# 抖内微信码
DONATE_WECHAT_PNG = 'donate_wechat.png'
# HELP
HELP_PNG = 'help.png'
# --- BIN文件 ---
# HANDLE64
HANDLE64_EXE = 'handle64.exe'

# --- 文件绝对路径 ---
# 配置路径
CONFIG_PATH = get_config_path()
# 版本文件
VERSION_PATH = CONFIG_PATH / DOT_VERSION
# 账号文件
ACCOUNTS_PATH = CONFIG_PATH / ACCOUNTS_JSON
# 用户配置文件
USER_SETTINGS_PATH = CONFIG_PATH / SETTINGS_JSON
# 恐怖地带文件
TERROR_ZONE_PATH = CONFIG_PATH / TERROR_ZONE_JSON
# 窗口配置文件
WIN_PATH = CONFIG_PATH / WIN_JSON
# LOGO
LOGO_PATH = get_assets_file(BEAR_ICO)
# 抖内微信码
DONATE_WECHAT_PATH = get_assets_file(DONATE_WECHAT_PNG)
# HELP
HELP_PATH = get_assets_file(HELP_PNG)
# 默认配置i文件
DEFAULT_SETTINGS_PATH = get_assets_file(SETTINGS_JSON)
# HANDLE64
HANDLE64_PATH = get_bin_file(HANDLE64_EXE)
# MOD路径
MOD_PATH = get_data_file(JCY_DOT_MPQ)


def ensure_appdata_files() -> bool:
    """返回是否执行了初始化"""
    initialized = False
    if not VERSION_PATH.exists():
        VERSION_PATH.write_text(APP_VERSION, encoding='utf-8')
        print(f"[DEBUG] 创建版本文件 {APP_VERSION}")
        initialized = True
    else:
        saved_version = VERSION_PATH.read_text().strip()
        if saved_version != APP_VERSION:
            VERSION_PATH.write_text(APP_VERSION, encoding='utf-8')
            print(f"[DEBUG] 更新版本文件 {saved_version} -> {APP_VERSION}")
            initialized = True
    return initialized


def load_default_config() -> dict:
    """加载默认配置文件(作者版)"""
    with open(DEFAULT_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
    

def load_user_config() -> dict:
    """加载用户配置文件"""
    with open(USER_SETTINGS_PATH, 'r', encoding="utf-8") as f:
        return json.load(f);
    

def merge_configs(default: dict, user: dict) -> dict:
    """
    以 user 配置优先合并 default 配置
    - 只保留 default 中存在的键，顺序跟 default 一致
    """
    def merge(d_def, d_user):
        merged = {}
        for key in d_def:
            def_val = d_def[key]
            user_val = d_user.get(key, None)

            if isinstance(def_val, dict):
                # 递归合并 dict
                merged[key] = merge(def_val, user_val if isinstance(user_val, dict) else {})
            else:
                # 用户配置存在则使用，否则用默认
                merged[key] = user_val if key in d_user else def_val
        return merged

    return merge(default, user)


# 导出所有需要的符号
__all__ = [
    'get_config_path',
    'get_assets_file',
    'get_bin_file',
    'get_data_file',

    'D2R_MOD_JCY',
    'JCY_DOT_MPQ',
    'DOT_VERSION',
    'ACCOUNTS_JSON',
    'SETTINGS_JSON',
    'TERROR_ZONE_JSON',
    'BEAR_ICO',
    'DONATE_WECHAT_PNG',
    'HELP_PNG',
    'HANDLE64_EXE',
    
    'CONFIG_PATH',
    'VERSION_PATH',
    'ACCOUNTS_PATH',
    'USER_SETTINGS_PATH',
    'TERROR_ZONE_PATH',
    'WIN_PATH',
    'LOGO_PATH',
    'DONATE_WECHAT_PATH',
    'HELP_PATH',
    'DEFAULT_SETTINGS_PATH',
    'HANDLE64_PATH',
    'MOD_PATH',
    
    'ensure_appdata_files',
    'load_default_config',
    'load_user_config',
    'merge_configs'
]
