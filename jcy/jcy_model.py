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
            "tabs": [
                {
                    "text": "总体设置",
                    "children":[
                        {
                            "fid": NETEASE_LANGUAGE,
                            "type": RADIO,
                            "text": "网易国服语言(装备/道具/符文/符文之语)",
                            "colspan": 10,
                            "params": {
                                "bak": "国服简中-zhCN",
                                "zhTW": "国际繁中-zhTW",
                                "enUS": "英文-enUS"
                            }
                        },
                        {
                            "type": SEPARATOR
                        },
                        {
                            "fid": TERROR_ZONE_SERVER,
                            "type": RADIO,
                            "text": "恐怖区域-服务器",
                            "colspan": 4,
                            "params": {
                                "1": "暴雪国际服",
                                "2": "网易国服"
                            }
                        },
                        {
                            "fid": TERROR_ZONE_LANGUAGE,
                            "type": RADIO,
                            "text": "恐怖区域-语言",
                            "colspan": 6,
                            "params": {
                                "zhCN": "简体中文-zhCN",
                                "zhTW": "繁體中文-zhTW",
                                "enUS": "英文-enUS"
                            }
                        },
                        {
                            "fid": TERROR_ZONE_NEXT,
                            "type": CHECK,
                            "text": "恐怖区域-预告",
                            "colspan": 4,
                            "params": {
                                "1": "Win系统通知",
                                "2": "游戏内预告"
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": GAME_SETTING,
                            "type": CHECK,
                            "text": "游戏设置",
                            "colspan": 8,
                            "params": {
                                "1": "快速创建游戏",
                                "2": "单击Esc退出游戏",
                                "3": "更大的好友菜单",
                                "4" : "画面变亮"
                            }
                        },
                        {
                            "fid": LIGHT_REDIUS,
                            "type": SPIN,
                            "text": "额外的照亮范围",
                            "colspan": 2
                        }
                    ]
                },
                {
                    "text": "职业设置",
                    "children": [
                        {
                            "fid": ARROW,
                            "type": RADIO,
                            "text": "弓/弩箭特效",
                            "colspan": 10,
                            "params": {
                                "0": "默认",
                                "1": "魔法箭",
                                "2": "冷霜箭",
                                "3": "火焰箭"
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": SOR_SETTING,
                            "type": CHECK,
                            "text": "魔法师",
                            "colspan": 10,
                            "params": {
                                "1": "取消雷云风暴吓人特效",
                                "2": "降低闪电新星亮度"
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": NEC_SETTING,
                            "type": CHECK,
                            "text": "死灵法师",
                            "colspan": 10,
                            "params": {
                                "1": "骷髅火刀圣盾"
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": DRU_SETTING,
                            "type": CHECK,
                            "text": "德鲁伊",
                            "colspan": 10,
                            "params": {
                                "1": "飓风术特效"
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": ASN_SETTING,
                            "type": CHECK,
                            "text": "刺客",
                            "colspan": 10,
                            "params": {
                                "1": "马赛克护眼",
                                "2": "取消影散影身效果"
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": MERCENARY,
                            "type": CHECK,
                            "text": "佣兵",
                            "colspan": 10,
                            "params": {
                                "1": "A1白毛罗格",
                                "2": "A2女性佣兵",
                                "5": "A5火焰刀佣兵"
                            }
                        }
                    ]
                }
            ],
            "checkbutton": {
                "104": "特殊词缀蓝装变色(红/绿)",
                "106": "经验祭坛/宝石祭坛 特效标识",
                "141": "左键快速购买",
                "113": "蓝色/金色/暗金色精英怪随机染色",
                "114": "怪物光源+危险标识",
                "115": "屏蔽 劣等的/損壞的/破舊的武器装备",
                "117": "咒符/22#+符文增加掉落光柱",
                "118": "咒符/22#+符文增加掉落提示音 & 技能结束提示音",
                "119": "技能图标(头顶:熊之印记/狼之印记 脚下:附魔/速度爆发+影散/BO 右侧:刺客聚气)",
                "120": "BOSS 指引",
                "121": "交互对象增加蓝色火苗",
                "124": "6BOSS钥匙皮肤+掉落光柱",
                "126": "屏蔽 地狱火炬火焰风暴特效",
                "131": "经验条变色",
                "136": "怪物血条D3风格",
                "147": "默认开启迷你血条",
                "148": "默认开启迷你盒子",
                "146": "正副手防呆提示",
                "149": "隐藏任务日志提示按钮"
            },
            "radiogroup": {
                "201": {
                    "text": "佣兵图标位置",
                    "colspan": 10,
                    "params": {
                        "default": "原版",
                        "1": "左上角缩进",
                        "2": "红球之上",
                        "3": "红球之上上"
                    }
                },
                "202": {
                    "text": "传送门皮肤",
                    "colspan": 10,
                    "params": {
                        "default": "原版蓝门",
                        "1": "原版红门",
                        "2": "双圈蓝门",
                        "3": "单圈红门"
                    }
                },
                "203": {
                    "text": "传送术皮肤",
                    "colspan": 10,
                    "params": {
                        "default": "原版",
                        "1": "冰霜",
                        "2": "火焰"
                    }
                },
                "205": {
                    "text": "老鼠刺针/剥皮吹箭皮肤",
                    "colspan": 10,
                    "params": {
                        "default": "原皮",
                        "1": "魔法箭",
                        "2": "冷霜箭",
                        "3": "火焰箭"
                    }
                },
                "206": {
                    "text": "符文皮肤",
                    "colspan": 10,
                    "params": {
                        "default": "原皮",
                        "1": "1",
                        "2": "2",
                        "3": "3",
                        "4": "4",
                        "5": "5",
                        "6": "6",
                        "7": "7",
                        "8": "8",
                        "9": "9"
                    }
                },
                "207": {
                    "text": "HUD面板尺寸",
                    "colspan": 10,
                    "params": {
                        "default": "100%",
                        "1": "85%",
                        "2": "75%",
                        "3": "65%"
                    }
                }
            },
            "checkgroup":{
                "399": {
                    "text": "控制器管理",
                    "colspan": 10,
                    "params": {
                        "1": "显示'D2R多开器'面板",
                        "2": "显示'恐怖区域'面板",
                        "3": "开启'恐怖区域'Win系统通知",
                        "4": "开启'恐怖区域'游戏内预告"
                    }
                },
                "301": {
                    "text": "角色特效",
                    "colspan": 10,
                    "params": {
                        "1": "套装特效",
                        "2": "脚下电圈特效",
                        "3": "红色闪电特效",
                        "4": "红色火焰特效",
                        "5": "小翅膀"
                    }
                },
                "303": {
                    "text": "装备特效",
                    "colspan": 10,
                    "params": {
                        "0": "底材阶级",
                        "1": "底材重量",
                        "2": "有用孔数",
                        "3": "底材防御",
                        "4": "附带英文",
                        "5": "MAX变量",
                        "6": "吐槽信息"
                    }
                },
                "302": {
                    "text": "属性词条特效",
                    "colspan": 10,
                    "params": {
                        "1": "英文缩写",
                        "2": "词条着色"
                    }
                },
                "304": {
                    "text": "选中屏蔽环境特效 (相关环境元素仅为不可见,碰撞体积,射击阻挡依然存在)",
                    "colspan": 10,
                    "params": {
                        "1": "动画",
                        "2": "崔凡克议会墙壁",
                        "3": "火焰之河岩浆",
                        "4": "混沌避难所大门",
                        "5": "督军山克死亡",
                        "6": "毁灭王座石柱"
                    }
                },
                "305": {
                    "text": "选中开启环境指引",
                    "colspan": 10,
                    "params": {
                        "1": "出/入口",
                        "2": "小站",
                        "3": "A1兵营",
                        "4": "A2贤者小站",
                        "5": "A4火焰之河",
                        "6": "A5尼拉塞克"
                    }
                },
                "306": {
                    "text": "选中屏蔽角色特效",
                    "colspan": 10,
                    "params": {
                        "1": "刺客-武学亮度",
                        "2": "刺客-影散隐身",
                        "3": "法师-雷云风暴吓人",
                        "4": "法师-闪电新星亮度",
                        "5": "头饰-外观"
                    }
                },
                "307": {
                    "text": "选中开启角色特效",
                    "colspan": 10,
                    "params": {
                        "1": "死灵-骷髅火刀圣盾",
                        "2": "德鲁伊-飓风术",
                        "3": "标枪闪电枪",
                        "4": "飞斧闪电尾",
                        "5": "A2女性佣兵",
                        "6": "A5火焰刀佣兵"
                    }
                }
            },
            "spinbox" : {
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