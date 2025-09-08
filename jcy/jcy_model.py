import json
from tkinter import messagebox
from jcy_constants import *
from jcy_paths import *



class FeatureConfig:
    """
    管理所有功能配置、默认状态以及与功能相关的资源文件路径。
    """
    def __init__(self):
        self.all_features_config = {
            "checkbutton": {
                "101": "点击角色快速建立最高难度游戏",
                "102": "Esc=存儲並離開",
                "103": "更大的好友菜单",
                "104": "特殊词缀蓝装变色(红/绿)",
                "142": "入口 箭头指引",
                "143": "小站 箭头指引",
                "106": "经验祭坛/宝石祭坛 特效标识",
                "141": "左键快速购买",
                "113": "蓝色/金色/暗金色精英怪随机染色",
                "114": "怪物光源+危险标识",
                "115": "屏蔽 劣等的/損壞的/破舊的武器装备",
                "117": "咒符/22#+符文增加掉落光柱",
                "118": "咒符/22#+符文增加掉落提示音 & 技能结束提示音",
                "119": "技能图标(头顶:熊之印记/狼之印记 脚下:附魔/速度爆发+影散/BO 右侧:刺客聚气)",
                "120": "A1兵营/A4火焰之河/A5尼拉塞克/BOSS 指引",
                "112": "画面变亮",
                "121": "交互对象增加蓝色火苗",
                "122": "马赛克护眼",

                "124": "6BOSS钥匙皮肤+掉落光柱",
                "125": "屏蔽 开场/过场/结束动画",
                "126": "屏蔽 地狱火炬火焰风暴特效",
                "127": "屏蔽 A4火焰之河岩浆特效",
                "128": "屏蔽 A5督军山克死亡特效",
                "129": "屏蔽 开门动画,极速进站",
                "130": "展示 A2贤者之谷小站塔墓标记 & 屏蔽 A3崔凡克议会墙屋/A4混沌庇护所大门/A5毁灭王座石柱",
                "131": "经验条变色",
                "132": "屏蔽 影散隐身特效",
                "133": "屏蔽 头环类装备外观",
                "134": "屏蔽 雷云风暴吓人特效",
                "135": "降低 闪电新星亮度",
                "136": "怪物血条D3风格",
                "137": "死灵召唤骷髅 火焰刀+圣盾特效",
                "138": "投掷标枪->闪电枪特效",
                "139": "投掷飞刀->闪电尾特效",
                "140": "德鲁伊飓风术 特效",

                "146": "正副手防呆提示",
                "144": "A2佣兵 女性化特效",
                "145": "A5佣兵 火焰刀特效",
            },
            "radiogroup": {
                "201": {
                    "text": "佣兵图标位置",
                    "params": [
                        {"default":"原版"},
                        {"1":"左上角缩进"},
                        {"2":"红球之上"},
                        {"3":"红球之上上"},
                    ]
                },
                "202": {
                    "text": "传送门皮肤",
                    "params": [
                        {"default":"原版蓝门"},
                        {"1":"原版红门"},
                        {"2":"双圈蓝门"},
                        {"3":"单圈红门"},
                    ]
                },
                "203": {
                    "text": "传送术皮肤",
                    "params": [
                        {"default":"原版"},
                        {"1":"冰霜"},
                        {"2":"火焰"},
                    ]
                },
                "204": {
                    "text": "弩/箭皮肤",
                    "params": [
                        {"default":"原皮"},
                        {"1":"魔法箭"},
                        {"2":"冷霜箭"},
                        {"3":"火焰箭"},
                    ]
                },
                "205": {
                    "text": "老鼠刺针/剥皮吹箭皮肤",
                    "params": [
                        {"default":"原皮"},
                        {"1":"魔法箭"},
                        {"2":"冷霜箭"},
                        {"3":"火焰箭"},
                    ]
                },
                "206": {
                    "text": "符文皮肤",
                    "params": [
                        {"default":"原皮"},
                        {"1":"1"},
                        {"2":"2"},
                        {"3":"3"},
                        {"4":"4"},
                        {"5":"5"},
                        {"6":"6"},
                        {"7":"7"},
                        {"8":"8"},
                        {"9":"9"},
                    ]
                },
                "207": {
                    "text": "HUD面板尺寸",
                    "params": [
                        {"default":"100%"},
                        {"1":"85%"},
                        {"2":"75%"},
                        {"3":"65%"},
                    ]
                },
            },
            "checkgroup":{
                "301": {
                    "text": "角色特效",
                    "params": [
                        {"1":"套装特效"},
                        {"2":"脚下电圈特效"},
                        {"3":"红色闪电特效"},
                        {"4":"红色火焰特效"},
                        {"5":"小翅膀"},
                    ],
                },
                "303": {
                    "text": "装备特效",
                    "params": [
                        {"0":"底材阶级"},
                        {"1":"底材重量"},
                        {"2":"有用孔数"},
                        {"3":"底材防御"},
                        {"4":"附带英文"},
                        {"5":"MAX变量"},
                        {"6":"吐槽信息"}
                    ]
                },
                "302": {
                    "text": "属性词条特效",
                    "params": [
                        {"1":"英文缩写"},
                        {"2":"词条着色"}
                    ]
                },
            },
            "spinbox" : {
                "401": "照亮范围",
                "402": "22#+符文名称大小"
            },
            "checktable": {
                "501": "道具屏蔽"
            }
        }

        # ---初始化默认功能状态---
        self.default_feature_states = {
            **{fid: False for fid in self.all_features_config["checkbutton"]},
            **{fid: "default" for fid in self.all_features_config["radiogroup"]},
            **{fid: [] for fid in self.all_features_config["checkgroup"]},
            **{fid: 0 for fid in self.all_features_config["spinbox"]},
            **{fid: False for fid in self.all_features_config["checktable"]}
        }
        

class FeatureStateManager:
    """
    配置文件操作类
    """
    def __init__(self, config: FeatureConfig):
        self.config = config
        self.loaded_states = {}

    def load_settings(self):
        """
        读取配置文件
        """
        try:
            with open(USER_SETTINGS_PATH, 'r', encoding='utf-8') as f:
                self.loaded_states = json.load(f)

            for fid in self.config.all_features_config["checkbutton"]:
                if fid not in self.loaded_states:
                    self.loaded_states[fid] = False

            for fid, info in self.config.all_features_config["radiogroup"].items():
                if fid not in self.loaded_states:
                    self.loaded_states[fid] = "default"
            
            for fid, info in self.config.all_features_config["checkgroup"].items():
                if fid not in self.loaded_states: 
                    self.loaded_states[fid] = []

            for fid in self.config.all_features_config["spinbox"]:
                if fid not in self.loaded_states:
                    self.loaded_states[fid] = 0

            for fid in self.config.all_features_config["checktable"]:
                if fid not in self.loaded_states:
                    self.loaded_states[fid] = {}

        except json.JSONDecodeError:
            messagebox.showerror("错误", "配置文件损坏，已重置为默认设置。")
            self.loaded_states = self.config.default_feature_states.copy()
        except Exception as e:
            messagebox.showerror("错误", f"读取配置文件失败：{e}\n已重置为默认设置。")
            self.loaded_states = self.config.default_feature_states.copy()


    def save_settings(self, config: dict = None):
        """确保保存完整配置"""
        
        print(f"[保存] 正在写入配置到 {USER_SETTINGS_PATH}")
        print(f"[保存] 包含的键: {list(config.keys())}")
        
        try:
            with open(USER_SETTINGS_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print("[保存] 配置写入成功")
        except Exception as e:
            print(f"[错误] 保存失败: {str(e)}")
            raise

    def get_default_value(self, feature_id: str):
        """获取功能的默认值"""
        # 根据feature_config实现具体逻辑
        if feature_id in self.feature_config.all_features_config["checkbutton"]:
            return False
        elif feature_id in self.feature_config.all_features_config["radiogroup"]:
            return list(self.feature_config.all_features_config["radiogroup"][feature_id]["params"][0].keys())[0]
        # ...其他类型处理...