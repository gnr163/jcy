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
                            "text": "网易国服-本地化(装备/道具/符文/符文之语/词缀/技能/地图)",
                            "colspan": 100,
                            "params": {
                                ZHCN2: "简中翻译",
                                S2T: "简中翻译->繁体",
                                ENUS: "enUS",
                                ZHTW2: "繁中翻译",
                                T2S: "繁中翻译->简体",
                            }
                        },
                        {
                            "fid": BATTLE_NET_LANGUAGE,
                            "type": RADIO,
                            "text": "暴雪國際服-本地化(裝備/道具/符文/符文之語/詞綴/技能/地图)",
                            "colspan": 100,
                            "params": {
                                ZHCN2: "简中翻译",
                                S2T: "简中翻译->繁体",
                                ENUS: "enUS",
                                ZHTW2: "繁中翻译",
                                T2S: "繁中翻译->简体",
                            }
                        },
                        {
                            "type": SEPARATOR
                        },
                        {
                            "fid": TERROR_ZONE_SERVER,
                            "type": RADIO,
                            "text": "恐怖区域-服务器",
                            "colspan": 40,
                            "params": {
                                "1": "暴雪国际服",
                                "2": "网易国服"
                            }
                        },
                        {
                            "fid": TERROR_ZONE_LANGUAGE,
                            "type": RADIO,
                            "text": "恐怖区域-语言",
                            "colspan": 60,
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
                            "colspan": 40,
                            "params": {
                                "1": "Win系统通知",
                                "2": "游戏内预告"
                            }
                        },
                        {
                            "fid": TERROR_ZONE_TABLE,
                            "type": TERROR_ZONE_TABLE,
                            "text": "恐怖区域",
                            "colspan": 100
                        }
                    ]
                },
                {
                    "text": "环境设置",
                    "children": [
                        {
                            "fid": GAME_SETTING,
                            "type": CHECK,
                            "text": "游戏设置",
                            "colspan": 80,
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
                            "colspan": 20
                        },
                        {
                            "fid": HUD_SIZE,
                            "type": RADIO,
                            "text": "HUD面板缩放",
                            "colspan": 50,
                            "params": {
                                "0": "100%",
                                "1": "85%",
                                "2": "75%",
                                "3": "65%"
                            }
                        },
                        {
                            "fid": PORTAL_SKIN,
                            "type": RADIO,
                            "text": "传送门皮肤",
                            "colspan": 50,
                            "params": {
                                "0": "原版蓝门",
                                "1": "原版红门",
                                "2": "双圈蓝门",
                                "3": "单圈红门"
                            }
                        },
                        {
                            "fid": GAME_SETTING2,
                            "type": CHECK,
                            "text": "游戏设置2",
                            "colspan": 100,
                            "params": {
                                "1": "隐藏任务按钮",
                                "2": "经验条彩色格式化",
                                "3": "左键快速购买",
                                "4": "经验/宝石祭坛特效标识",
                                "5": "交互对象增加蓝色火苗"
                            }
                        },
                        {
                            "fid": GAME_SETTING3,
                            "type": CHECK,
                            "text": "游戏设置3",
                            "colspan": 100,
                            "params": {
                                "1": "隐藏左右面板边框&铰链"
                            }
                        },
                        {
                            "fid": CONTROLS_SETTING,
                            "type": CHECK,
                            "text": "控件设置",
                            "colspan": 100,
                            "params": {
                                "1": "正副手提示",
                                "2": "默认开启迷你血条",
                                "3": "默认开启MINI盒子",
                                "4": "H键帮助面板+字典"
                            }
                        },
                        {
                            "fid": DISABLE_EFFECTS,
                            "type": CHECK,
                            "text": "环境-屏蔽元素",
                            "colspan": 100,
                            "params": {
                                "1": "动画",
                                "2": "崔凡克议会墙壁",
                                "3": "火焰之河岩浆",
                                "4": "混沌避难所大门",
                                "6": "毁灭王座石柱"
                            }
                        },
                        {
                            "fid": ENABLE_POINTER,
                            "type": CHECK,
                            "text": "环境-开启指引",
                            "colspan": 100,
                            "params": {
                                "3": "A1兵营",
                                "4": "A2贤者小站",
                                "5": "A4火焰之河",
                                "6": "A5尼拉塞克"
                            }
                        },
                        {
                            "fid": WAYPOINT_POINTER,
                            "type": RADIO,
                            "text": "环境-小站指引",
                            "colspan": 50,
                            "params": {
                                "0": "原皮无指引",
                                "1": "箭头指引",
                                "2": "蓝环指引*",
                            }
                        },
                        {
                            "fid": MISSION_POINTER,
                            "type": RADIO,
                            "text": "环境-任务指引",
                            "colspan": 50,
                            "params": {
                                "0": "原皮无指引",
                                "1": "箭头指引",
                                "2": "红环指引*",
                            }
                        },
                        {
                            "fid": UPSTAIRS_POINTER,
                            "type": RADIO,
                            "text": "环境-上口指引",
                            "colspan": 50,
                            "params": {
                                "0": "原皮无指引",
                                "1": "箭头指引*",
                                "2": "黄环指引",
                            }
                        },
                        {
                            "fid": DOWNSTAIRS_POINTER,
                            "type": RADIO,
                            "text": "环境-下口指引",
                            "colspan": 50,
                            "params": {
                                "0": "原皮无指引",
                                "1": "箭头指引*",
                                "2": "绿环指引",
                            }
                        }
                    ]
                },
                {
                    "text": "角色设置",
                    "children": [
                        {
                            "fid": CHARACTER_EFFECTS,
                            "type": CHECK,
                            "text": "角色特效",
                            "colspan": 100,
                            "params": {
                                "1": "套装金色光圈",
                                "2": "脚下电圈特效",
                                "3": "红色闪电特效",
                                "4": "红色火焰特效",
                                "5": "小翅膀"
                            }
                        },
                        {
                            "fid": COMMON_SETTING,
                            "type": CHECK,
                            "text": "通用设置",
                            "colspan": 100,
                            "params": {
                                "1": "屏蔽 地狱火炬 火焰风暴特效",
                                "2": "开启 技能图标(头顶:熊之印记/狼之印记 脚下:附魔/速度爆发+影散/BO 右侧:刺客聚气)"
                            }
                        },
                        {
                            "fid": ARROW,
                            "type": RADIO,
                            "text": "弓/弩箭特效",
                            "colspan": 100,
                            "params": {
                                "0": "默认",
                                "1": "魔法箭",
                                "2": "冷霜箭",
                                "3": "火焰箭"
                            }
                        },
                        {
                            "fid": SOR_SETTING,
                            "type": CHECK,
                            "text": "魔法师",
                            "colspan": 50,
                            "params": {
                                "1": "取消雷云风暴吓人特效",
                                "2": "降低闪电新星亮度"
                            }
                        },
                        {        
                            "fid": TELEPORT_SKIN,
                            "type": RADIO,
                            "text": "传送术皮肤",
                            "colspan": 50,
                            "params": {
                                "0": "原版",
                                "1": "冰霜",
                                "2": "火焰"
                            }
                        },
                        {
                            "fid": NEC_SETTING,
                            "type": CHECK,
                            "text": "死灵法师",
                            "colspan": 20,
                            "params": {
                                "1": "骷髅火刀圣盾"
                            }
                        },
                        {
                            "fid": DRU_SETTING,
                            "type": CHECK,
                            "text": "德鲁伊",
                            "colspan": 20,
                            "params": {
                                "1": "飓风术特效"
                            }
                        },
                        {
                            "fid": ASN_SETTING,
                            "type": CHECK,
                            "text": "刺客",
                            "colspan": 60,
                            "params": {
                                "1": "马赛克护眼",
                                "2": "取消影散隐身效果"
                            }
                        },
                        {
                            "fid": SKILL_OFF_SOUNDS,
                            "type": CHECK,
                            "text": "技能结束提示音",
                            "colspan": 100,
                            "columns": 5,
                            "flac": True,
                            "params": {
                                "enchant_off": "@skillname52",
                                "frozenarmor_off": "@skillname40",
                                "shiverarmor_off": "@skillname50",
                                "chillingarmor_off": "@skillname60",
                                "energyshield_off": "@skillname58",
                                "shout_off": "@skillname138",
                                "battleorders_off": "@skillname149",
                                "battlecommand_off": "@skillname155",
                                "bonearmor_off": "@skillname68",
                                "venom_off": "@Skillname279",
                                "fade_off": "@Skillname268",
                                "quickness_off": "@Skillname259",
                                "bladeshield_off": "@Skillname278",
                                "holyshield_off": "@skillname117",
                                "cyclonearmor_off": "@Skillname236",
                                "wolf_off": "@Skillname224",
                                "bear_off": "@Skillname229",
                                "markwolf_off": "@SkillnameMetamorphosisWolf",
                                "markbear_off": "@SkillnameMetamorphosisBear",
                            }
                        },
                    ]
                },
                {
                    "text": "怪物设置",
                    "children": [
                        {
                            "fid": MERCENARY_LOCATION,
                            "type": RADIO,
                            "text": "佣兵-图标位置",
                            "colspan": 100,
                            "params": {
                                "0": "原版",
                                "1": "左上角缩进",
                                "2": "红球之上",
                                "3": "红球之上上",
                                "9": "自定义"
                            }
                        },
                        {
                            "fid": MERCENARY_100,
                            "type": LOCATION,
                            "text": "佣兵-坐标 x HUD100%",
                            "colspan": 25,
                            "params": {
                                "x": 1286,
                                "y": 1640
                            }
                        },
                        {
                            "fid": MERCENARY_85,
                            "type": LOCATION,
                            "text": "佣兵-坐标 x HUD85%",
                            "colspan": 25,
                            "params": {
                                "x": 1656,
                                "y": 2025
                            }
                        },
                        {
                            "fid": MERCENARY_75,
                            "type": LOCATION,
                            "text": "佣兵-坐标 x HUD75%",
                            "colspan": 25,
                            "params": {
                                "x": 1981,
                                "y": 2375
                            }
                        },
                        {
                            "fid": MERCENARY_65,
                            "type": LOCATION,
                            "text": "佣兵-坐标 x HUD65%",
                            "colspan": 25,
                            "params": {
                                "x": 2381,
                                "y": 2785
                            }
                        },
                        {
                            "fid": MERCENARY,
                            "type": CHECK,
                            "text": "佣兵-皮肤",
                            "colspan": 50,
                            "params": {
                                "1": "A1白毛罗格",
                                "2": "A2女性佣兵",
                                "5": "A5火焰刀佣兵"
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": MONSTER_SETTING,
                            "type": CHECK,
                            "text": "怪物-配置",
                            "colspan": 100,
                            "params": {
                                "2": "危险怪物增加光源标识",
                                "4": "屏蔽A5督军山克死亡特效",
                                "5": "蓝色精英随机染色"
                            }
                        },                        
                        {
                            "fid": MONSTER_HEALTH,
                            "type": RADIO,
                            "text": "怪物-血条样式",
                            "colspan": 50,
                            "params": {
                                "0": "原皮",
                                "1": "加宽加高",
                                "2": "D3风格",
                                "3": "Jerry风格"
                            }
                        },
                        {
                            "fid": MONSTER_MISSILE,
                            "type": RADIO,
                            "text": "老鼠刺针/剥皮吹箭样式",
                            "colspan": 50,
                            "params": {
                                "0": "原皮",
                                "1": "魔法箭",
                                "2": "冷霜箭",
                                "3": "火焰箭"
                            }
                        }
                    ]
                },
                {
                    "text": "物品设置",
                    "children": [
                        {
                            "fid": EQIUPMENT_EFFECTS,
                            "type": CHECK,
                            "text": "装备-名称特效",
                            "colspan": 100,
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
                        {
                            "fid": EQIUPMENT_SETTING,
                            "type": CHECK,
                            "text": "装备-设置",
                            "colspan": 50,
                            "params": {
                                "1": "屏蔽 劣等/损坏/破旧武器装备底材",
                                "2": "开启 蓝色装备染色(特殊词缀)"
                            }
                        },
                        {
                            "fid": AFFIX_EFFECTS,
                            "type": CHECK,
                            "text": "装备-词缀特效",
                            "colspan": 50,
                            "params": {
                                "1": "英文缩写",
                                "2": "词缀着色"
                            }
                        },
                        {
                            "fid": SETS_EFFECTS,
                            "type": CHECK,
                            "text": "装备-套装特效",
                            "colspan": 50,
                            "params": {
                                "4": "附带英文",
                                "5": "MAX变量",
                                "6": "吐槽信息"
                            }
                        },
                        {
                            "fid": MODEL_EFFECTS,
                            "type": CHECK,
                            "text": "装备-模型特效",
                            "colspan": 100,
                            "params": {
                                "1": "隐藏 头饰模型",
                                "2": "开启 投掷标枪-闪电枪特效",
                                "3": "开启 投掷飞斧-闪电拖尾特效"
                            }
                        },
                        {
                            "type": "Separator"
                        },
                        {
                            "fid": TORCH_KEY,
                            "type": CHECK,
                            "text": "火炬钥匙",
                            "colspan": 70,
                            "params": {
                                "1": "金属颜色皮肤",
                                "2": "掉落光柱提醒",
                                "3": "掉落声音提醒"
                            }
                        },
                        {
                            "fid": RUNE_SIZE,
                            "type": SPIN,
                            "text": "22#+符文名称大小(越大越容易发现/选中)",
                            "colspan": 30
                        },
                        {
                            "fid": DROPED_LIGHT,
                            "type": CHECK,
                            "text": "掉落光柱提醒",
                            "colspan": 100,
                            "params": {
                                "1": "戒指",
                                "2": "项链",
                                "3": "小符",
                                "4": "中符",
                                "5": "大符",
                                "6": "珠宝",
                                "7": "宝石"
                            }
                        },
                        {
                            "fid": ITEM_DROP_SOUNDS,
                            "type": CHECK,
                            "text": "物品掉落提示音",
                            "colspan": 100,
                            "columns": 5,
                            "flac": True,
                            "params": {
                                "diadem": "@Diadem",
                                "sc": "@cm1",
                                "gc": "@cm3",
                            }
                        },
                        
                    ]
                }
            ],
            "checktable": {
                RUNE_SETTING: "符文提醒",
                ITEM_FILTER: "道具过滤"
            }

        }

        # ---初始化默认功能状态---
        self.default_feature_states = {
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

