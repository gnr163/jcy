"""
常量模块
"""

# 互斥体名称
MUTEX_NAME = "Global\\D2R_MOD_JCY_MUTEX"

# 互斥错误 183, 表示互斥体已存在（即已有实例）
ERROR_ALREADY_EXISTS = 183

# 自定义消息ID(通知已有实例, restore窗口)
WM_SHOW_WINDOW = 0x5000

# 语言
ENUS = 'enUS'
ZHCN = 'zhCN'
ZHCN2 = 'zhCN2'
ZHTW = 'zhTW'
ZHTW2 = 'zhTW2'
# 简->繁
S2T = 'S2T'
# 繁->简
T2S = 'T2S'


LANG = None

# 控制器名称
APP_NAME = "jcy控制器"

# MOD版本
APP_VERSION = "v1.3.2.2"

# 发布日期
APP_DATE = "20251205"

# 控制器全称
APP_FULL_NAME = f"{APP_NAME}_{APP_VERSION}"

# APP大小
APP_SIZE = "750x700"

# 区服地址
REGION_DOMAIN_MAP = {
    "kr": "kr.actual.battle.net",
    "us": "us.actual.battle.net",
    "eu": "eu.actual.battle.net"
}

# 区服名称
REGION_NAME_MAP = {
    "kr": "亚服",
    "us": "美服",
    "eu": "欧服"
}

# Unicode私有区字符 for 屏蔽道具
UE01A = "" * 41

# 全局字典
GLOBAL_DICT = {}

def init_global_dict(file_operations):
    GLOBAL_DICT.clear()
    GLOBAL_DICT.update(file_operations.load_global_dict())

def translate(text: str) -> str:
    """如果首位是 @ 则按字典翻译，否则原样返回"""
    if isinstance(text, str) and text.startswith('@'):
        key = text[1:]  # 去掉@
        _dict = GLOBAL_DICT.get(key)
        if _dict: 
            return _dict[ZHCN]
    return text

# <!-- Function Identifier 
NETEASE_LANGUAGE = "NeteaseLanguage"
BATTLE_NET_LANGUAGE = "BattleNetLanguage"
TERROR_ZONE_SERVER = "TerrorZoneServer"
TERROR_ZONE_LANGUAGE = "TerrorZoneLanguage"
TERROR_ZONE_NEXT = "TerrorZoneNext"
TERROR_ZONE_TABLE = "TerrorZoneTable"
GAME_SETTING = "GameSetting"
GAME_SETTING2 = "GameSetting2"
GAME_SETTING3 = "GameSetting3"
CONTROLS_SETTING = "ControlsSetting"
LIGHT_REDIUS = "LightRedius"
HUD_SIZE = "HudSize"
PORTAL_SKIN = "ProtalSkin"
CHARACTER_EFFECTS = "CharacterEffects"
ARROW = "Arrow"
SOR_SETTING = "SorceressSetting"
TELEPORT_SKIN = "TeleportSkin"
NEC_SETTING = "NecromancerSetting"
PAL_SETTING = "PaladinSetting"
BAR_SETTING = "BarbarianSetting"
DRU_SETTING = "DruidSetting"
ASN_SETTING = "AssassinSetting"
COMMON_SETTING = "CommonSetting"
SKILL_OFF_SOUNDS = "SkillOffSounds"
MERCENARY = "Mercenary"
MERCENARY_LOCATION = "MercenaryLocation"
MERCENARY_100 = "Mercenary100"
MERCENARY_85 = "Mercenary85"
MERCENARY_75 = "Mercenary75"
MERCENARY_65 = "Mercenary65"
MONSTER_SETTING = "MonsterSetting"
MONSTER_HEALTH = "MonsterHealth"
MONSTER_MISSILE = "MonsterMissile"
EQIUPMENT_EFFECTS = "EquipmentEffects"
EQIUPMENT_SETTING = "EquipmentSetting"
AFFIX_EFFECTS = "AffixEffects"
SETS_EFFECTS = "SetsEffects"
MODEL_EFFECTS = "ModelEffects"
RUNE_SIZE = "RuneSize"
ITEM_NOTIFICATION = "ItemNotification"
ASSET_PATH = "AssetPath"
DISABLE_EFFECTS = "DisableEffects"
ENABLE_POINTER = "EnablePointer"
TORCH_KEY = "TorchKey"
ITEM_FILTER = "ItemFilter"
WAYPOINT_POINTER = "WayPointPointer"
MISSION_POINTER = "MissionPointer"
UPSTAIRS_POINTER = "UpstairsPointer"
DOWNSTAIRS_POINTER = "DownstairsPointer"
# Function Identifier -->

# <!-- Controller Type
RADIO = "RadioGroup"
CHECK = "CheckGroup"
SPIN = "SpinBox"
SEPARATOR = "Separator"
LOCATION = "Location"
# Controller Type -->

ITEM_ENUS = ["El Rune", "Eld Rune", "Tir Rune", "Nef Rune", "Eth Rune", "Ith Rune", "Tal Rune", "Ral Rune", "Ort Rune", "Thul Rune", "Amn Rune", "Sol Rune", "Shael Rune", "Dol Rune", "Hel Rune", "Io Rune", "Lum Rune", "Ko Rune", "Fal Rune", "Lem Rune", "Pul Rune", "Um Rune", "Mal Rune", "Ist Rune", "Gul Rune", "Vex Rune", "Ohm Rune", "Lo Rune", "Sur Rune", "Ber Rune", "Jah Rune", "Cham Rune", "Zod Rune", "Ring", "Amulet", "Jewel", "Small Charm", "Large Charm", "Grand Charm", "Diadem"]
ITEM_ZHTW = ["艾爾#01", "艾德#02", "特爾#03", "那夫#04", "愛斯#05", "伊司#06", "塔爾#07", "拉爾#08", "歐特#09", "書爾#10", "安姆#11", "索爾#12", "夏#13", "多爾#14", "海爾#15", "埃歐#16", "盧姆#17", "科#18", "法爾#19", "藍姆#20", "普爾#21", "烏姆#22", "馬爾#23", "伊司特#24", "古爾#25", "伐克斯#26", "歐姆#27", "羅#28", "瑟#29", "貝#30", "喬#31", "查姆#32", "薩德#33", "戒指", "項鏈", "珠寶", "小型咒符", "大型咒符", "巨型咒符", "權冠"]
# 本地化文件列表
LNG_STRINGS = [
    r"data/local/lng/strings/item-modifiers.json",
    r"data/local/lng/strings/item-nameaffixes.json",
    r"data/local/lng/strings/item-names.json",
    r"data/local/lng/strings/item-runes.json",
    r"data/local/lng/strings/levels.json",
    r"data/local/lng/strings/monsters.json",
    r"data/local/lng/strings/npcs.json",
    r"data/local/lng/strings/objects.json",
    r"data/local/lng/strings/quests.json",
    r"data/local/lng/strings/shrines.json",
    r"data/local/lng/strings/skills.json",
]

# 恐怖区域API
TERROR_ZONE_API = {
    "1" : ["https://asia.d2tz.info/terror_zone?mode=online", "https://api.d2tz.info/terror_zone?mode=online"],
    "2": ["https://api.d2-trade.com.cn/api/query/tz_online/zh-cn"],
}

# 恐怖地带
TERROR_ZONE_DICT = {
  "1-1": {"zhCN": "鲜血荒地、 邪恶洞穴", "zhTW": "鮮血荒地、 邪惡洞窟", "enUS": "Blood Moor, Den of Evil", "exp": "F", "drop": "F"},
  "1-2": {"zhCN": "冰冷之原、洞穴", "zhTW": "冰冷之原、洞穴", "enUS": "Cold Plains, The Cave", "exp": "C", "drop": "D"},
  "1-3": {"zhCN": "埋骨之地、墓穴、寝陵", "zhTW": "埋骨之地、墓穴、大陵墓", "enUS": "Burial Grounds, The Crypt, The Mausoleum", "exp": "F", "drop": "F"},
  "1-4": {"zhCN": "石块旷野", "zhTW": "亂石曠野", "enUS": "Stony Field", "exp": "F", "drop": "D"},
  "1-5": {"zhCN": "崔斯特姆", "zhTW": "崔斯特姆", "enUS": "Tristram", "exp": "F", "drop": "F"},
  "1-6": {"zhCN": "黑暗森林、地下通道", "zhTW": "黑暗森林、地底通道", "enUS": "Dark Wood, Underground Passage", "exp": "C", "drop": "D"},
  "1-7": {"zhCN": "黑色沼泽、 洞坑", "zhTW": "黑色荒地、 地洞", "enUS": "Black Marsh, The Hole", "exp": "C", "drop": "D"},
  "1-8": {"zhCN": "被遗忘的高塔", "zhTW": "遺忘之塔", "enUS": "The Forgotten Tower", "exp": "C", "drop": "A"},
  "1-9": {"zhCN": "深坑", "zhTW": "地穴", "enUS": "The Pit", "exp": "A", "drop": "A"},
  "1-10": {"zhCN": "监牢、营房", "zhTW": "監牢、兵營", "enUS": "Jail, Barracks", "exp": "B", "drop": "C"},
  "1-11": {"zhCN": "大教堂、地下墓穴", "zhTW": "大教堂、地下墓穴", "enUS": "Cathedral, Catacombs", "exp": "A", "drop": "A"},
  "1-12": {"zhCN": "哞哞农场", "zhTW": "哞哞農場", "enUS": "Moo Moo Farm", "exp": "B", "drop": "S"},
  "2-1": {"zhCN": "下水道", "zhTW": "鲁高因下水道", "enUS": "Lut Gholein Sewers", "exp": "B", "drop": "C"},
  "2-2": {"zhCN": "碎石荒野、碎石古墓", "zhTW": "碎石荒地、古老石墓", "enUS": "Rocky Waste, Stony Tomb", "exp": "B", "drop": "C"},
  "2-3": {"zhCN": "干燥高地、亡者大殿", "zhTW": "乾土高地、死亡之殿", "enUS": "Dry Hills, Halls of the Dead", "exp": "A", "drop": "C"},
  "2-4": {"zhCN": "偏远绿洲", "zhTW": "遙遠的綠洲", "enUS": "Far Oasis", "exp": "F", "drop": "F"},
  "2-5": {"zhCN": "古代水道", "zhTW": "古代通道", "enUS": "Ancient Tunnels", "exp": "D", "drop": "C"},
  "2-6": {"zhCN": "失落之城、群蛇峡谷、利爪蝮蛇神殿", "zhTW": "失落古城、群蛇峽谷、利爪蛇魔神殿", "enUS": "Lost City, Valley of Snakes, Claw Viper Temple", "exp": "C", "drop": "C"},
  "2-7": {"zhCN": "神秘避难所", "zhTW": "秘法聖殿", "enUS": "Arcane Sanctuary", "exp": "C", "drop": "A"},
  "2-8": {"zhCN": "塔•拉夏之墓、塔•拉夏的墓室", "zhTW": "塔拉夏的古墓、塔拉夏的密室", "enUS": "Tal Rasha's Tombs, Tal Rasha's Chamber", "exp": "S", "drop": "A"},
  "3-1": {"zhCN": "蜘蛛森林、蜘蛛洞穴", "zhTW": "蜘蛛森林、蜘蛛洞窟", "enUS": "Spider Forest, Spider Cavern", "exp": "C", "drop": "B"},
  "3-2": {"zhCN": "剥皮魔丛林、剥皮魔监牢", "zhTW": "剝皮叢林、剝皮地牢", "enUS": "Flayer Jungle, Flayer Dungeon", "exp": "A", "drop": "B"},
  "3-3": {"zhCN": "庞大湿地", "zhTW": "大沼澤", "enUS": "Great Marsh", "exp": "C", "drop": "B"},
  "3-4": {"zhCN": "库拉斯特集市、毁灭的神庙、废弃的礼拜堂", "zhTW": "庫拉斯特市集、荒廢的神殿、廢棄的寺院", "enUS": "Kurast Bazaar, Ruined Temple, Disused Fane", "exp": "C", "drop": "B"},
  "3-5": {"zhCN": "崔凡克", "zhTW": "崔凡克", "enUS": "Travincal", "exp": "B", "drop": "A"},
  "3-6": {"zhCN": "憎恨囚牢", "zhTW": "憎恨的囚牢", "enUS": "Durance of Hate", "exp": "C", "drop": "A"},
  "4-1": {"zhCN": "外围荒原、绝望平原", "zhTW": "外圍荒原、絕望平原", "enUS": "Outer Steppes, Plains of Despair", "exp": "C", "drop": "C"},
  "4-2": {"zhCN": "火焰之河、神罚之城", "zhTW": "火焰之河、罪罰之城", "enUS": "River of Flame, City of the Damned", "exp": "B", "drop": "B"},
  "4-3": {"zhCN": "混沌避难所", "zhTW": "混沌庇難所", "enUS": "Chaos Sanctuary", "exp": "S", "drop": "S"},
  "5-1": {"zhCN": "血腥丘陵、冰冻高地、亚巴顿", "zhTW": "血腥丘陵、冰凍高地、亞巴頓", "enUS": "Bloody Foothills, Frigid Highlands, Abaddon", "exp": "B", "drop": "B"},
  "5-2": {"zhCN": "冰川小径、漂流洞窟", "zhTW": "冰河小径、漂泊者洞窟", "enUS": "Glacial Trail, Drifter Cavern", "exp": "C", "drop": "C"},
  "5-3": {"zhCN": "先祖之路、寒冰地窖", "zhTW": "先祖之路、冰窖", "enUS": "Ancient's Way, Icy Cellar", "exp": "C", "drop": "C"},
  "5-4": {"zhCN": "亚瑞特高原、阿克隆深渊", "zhTW": "亞瑞特高原、冥河地穴", "enUS": "Arreat Plateau, Pit of Acheron", "exp": "B", "drop": "C"},
  "5-5": {"zhCN": "水晶通道、冰冻之河", "zhTW": "水晶通道、冰凍之河", "enUS": "Crystalline Passage, Frozen River", "exp": "C", "drop": "C"},
  "5-6": {"zhCN": "尼拉塞克的神殿、痛楚大厅、苦痛大厅、沃特大厅", "zhTW": "尼拉塞克神殿、怨慟之廳、苦痛之廳、沃特之廳", "enUS": "Nihlathak's Temple, Temple Halls", "exp": "B", "drop": "A"},
  "5-7": {"zhCN": "世界之石要塞、毁灭王座、世界之石大殿", "zhTW": "世界之石要塞、毀滅王座、世界之石大殿", "enUS": "Worldstone Keep, Throne of Destruction, Worldstone Chamber", "exp": "S", "drop": "S"}
}

TERROR_ZONE_MAP = {
    "精华荒地":"1-1",
    "鮮血荒地":"1-1",
    "邪恶洞穴":"1-1",
    "邪惡洞窟":"1-1",
    "冰冷之原":"1-2",
    "洞穴":"1-2",
    "埋骨之地":"1-3",
    "墓穴":"1-3",
    "墓地":"1-3",
    "大陵墓":"1-3",
    "寝陵":"1-3",
    "石块旷野":"1-4",
    "亂石曠野":"1-4",
    "崔斯特姆":"1-5",
    "黑暗森林":"1-6",
    "地底通道":"1-6",
    "地下通道":"1-6",
    "黑色沼泽":"1-7",
    "黑色荒地":"1-7",
    "地洞":"1-7",
    "被遗忘的高塔":"1-8",
    "遺忘之塔":"1-8",
    "地穴":"1-9",
    "深坑":"1-9",
    "监狱":"1-10",
    "監牢":"1-10",
    "兵營":"1-10",
    "营房":"1-10",
    "大教堂":"1-11",
    "地下墓穴":"1-11",
    "秘密乳牛關":"1-12",
    "神秘的奶牛关":"1-12",
    "下水道":"2-1",
    "鲁高因下水道":"2-1",
    "鲁·高因下水道":"2-1",
    "碎石荒野":"2-2",
    "碎石荒地":"2-2",
    "古老石墓":"2-2",
    "碎石古墓":"2-2",
    "乾土高地":"2-3",
    "干燥高地":"2-3",
    "死亡之殿":"2-3",
    "亡者大殿":"2-3",
    "遙遠的綠洲":"2-4",
    "偏远绿洲":"2-4",
    "古代通道":"2-5",
    "古代水道":"2-5",
    "失落古城":"2-6",
    "失落之城":"2-6",
    "群蛇峽谷":"2-6",
    "群蛇峡谷":"2-6",
    "利爪蛇魔神殿":"2-6",
    "利爪蝮蛇神殿":"2-6",
    "秘法聖殿":"2-7",
    "神秘避难所":"2-7",
    "塔拉夏的古墓":"2-8",
    "塔·拉夏之墓":"2-8",
    "塔拉夏的密室":"2-8",
    "塔·拉夏的墓室":"2-8",
    "蜘蛛森林":"3-1",
    "蜘蛛洞窟":"3-1",
    "蜘蛛洞穴":"3-1",
    "剝皮叢林":"3-2",
    "翠绿丛林":"3-2",
    "剝皮地牢":"3-2",
    "翠绿监牢":"3-2",
    "大沼澤":"3-3",
    "庞大湿地":"3-3",
    "庫拉斯特市集":"3-4",
    "库拉斯特集市":"3-4",
    "荒廢的神殿":"3-4",
    "毁灭的神庙":"3-4",
    "廢棄的寺院":"3-4",
    "废弃的礼拜堂":"3-4",
    "崔凡克":"3-5",
    "憎恨囚牢":"3-6",
    "外圍荒原":"4-1",
    "外域荒原":"4-1",
    "絕望平原":"4-1",
    "绝望平原":"4-1",
    "火焰之河":"4-2",
    "罪罰之城":"4-2",
    "神罚之城":"4-2",
    "混沌魔殿":"4-3",
    "混沌避难所":"4-3",
    "血腥丘陵":"5-1",
    "嗜战丘陵":"5-1",
    "苦战丘陵":"5-1",
    "冰凍高地":"5-1",
    "冰冻高地":"5-1",
    "亞巴頓":"5-1",
    "亚巴顿":"5-1",
    "冰河小徑":"5-2",
    "冰川小径":"5-2",
    "漂泊者洞窟":"5-2",
    "漂流洞窟":"5-2",
    "先祖之路":"5-3",
    "冰窖":"5-3",
    "寒冰地窖":"5-3",
    "亞瑞特高原":"5-4",
    "亚瑞特高原":"5-4",
    "冥河地穴":"5-4",
    "阿克隆深渊":"5-4",
    "水晶通道":"5-5",
    "冰凍之河":"5-5",
    "冰冻之河":"5-5",
    "尼拉塞克的神殿":"5-6",
    "怨慟之廳":"5-6",
    "痛楚大厅":"5-6",
    "苦痛之廳":"5-6",
    "苦痛大厅":"5-6",
    "沃特之廳":"5-6",
    "沃特大厅":"5-6",
    "世界之石要塞":"5-7",
    "毀滅王座":"5-7",
    "毁灭王座":"5-7",
    "世界之石大殿":"5-7"
}

# SETS_INDEX
SETS_INDEX = [
  "Civerb's Vestments",
  "Hsarus' Defense",
  "Cleglaw's Brace",
  "Iratha's Finery",
  "Isenhart's Armory",
  "Vidala's Rig",
  "Milabrega's Regalia",
  "Cathan's Traps",
  "Tancred's Battlegear",
  "Sigon's Complete Steel",
  "Infernal Tools",
  "Berserker's Garb",
  "Death's Disguise",
  "Angelical Raiment",
  "Arctic Gear",
  "Arcanna's Tricks",
  "Natalya's Odium",
  "Aldur's Watchtower",
  "Immortal King",
  "Tal Rasha's Wrappings",
  "Griswold's Legacy",
  "Trang-Oul's Avatar",
  "M'avina's Battle Hymn",
  "The Disciple",
  "Heaven's Brethren",
  "Orphan's Call",
  "Hwanin's Majesty",
  "Sazabi's Grand Tribute",
  "Bul-Kathos' Children",
  "Cow King's Leathers",
  "Naj's Ancient Set",
  "McAuley's Folly",
  "Warlord's Glory",
]

# SetItemIndex
SET_ITEM_INDEX = [
  "Civerb's Ward",
  "Civerb's Icon",
  "Civerb's Cudgel",
  "Hsarus' Iron Heel",
  "Hsarus' Iron Fist",
  "Hsarus' Iron Stay",
  "Cleglaw's Tooth",
  "Cleglaw's Claw",
  "Cleglaw's Pincers",
  "Iratha's Collar",
  "Iratha's Cuff",
  "Iratha's Coil",
  "Iratha's Cord",
  "Isenhart's Lightbrand",
  "Isenhart's Parry",
  "Isenhart's Case",
  "Isenhart's Horns",
  "Vidala's Barb",
  "Vidala's Fetlock",
  "Vidala's Ambush",
  "Vidala's Snare",
  "Milabrega's Orb",
  "Milabrega's Rod",
  "Milabrega's Diadem",
  "Milabrega's Robe",
  "Cathan's Rule",
  "Cathan's Mesh",
  "Cathan's Visage",
  "Cathan's Sigil",
  "Cathan's Seal",
  "Tancred's Crowbill",
  "Tancred's Spine",
  "Tancred's Hobnails",
  "Tancred's Weird",
  "Tancred's Skull",
  "Sigon's Gage",
  "Sigon's Visor",
  "Sigon's Shelter",
  "Sigon's Sabot",
  "Sigon's Wrap",
  "Sigon's Guard",
  "Infernal Cranium",
  "Infernal Torch",
  "Infernal Sign",
  "Berserker's Headgear",
  "Berserker's Hauberk",
  "Berserker's Hatchet",
  "Death's Hand",
  "Death's Guard",
  "Death's Touch",
  "Angelic Sickle",
  "Angelic Mantle",
  "Angelic Halo",
  "Angelic Wings",
  "Arctic Horn",
  "Arctic Furs",
  "Arctic Binding",
  "Arctic Mitts",
  "Arcanna's Sign",
  "Arcanna's Deathwand",
  "Arcanna's Head",
  "Arcanna's Flesh",
  "Expansion",
  "Natalya's Totem",
  "Natalya's Mark",
  "Natalya's Shadow",
  "Natalya's Soul",
  "Aldur's Stony Gaze",
  "Aldur's Deception",
  "Aldur's Gauntlet",
  "Aldur's Advance",
  "Immortal King's Will",
  "Immortal King's Soul Cage",
  "Immortal King's Detail",
  "Immortal King's Forge",
  "Immortal King's Pillar",
  "Immortal King's Stone Crusher",
  "Tal Rasha's Fire-Spun Cloth",
  "Tal Rasha's Adjudication",
  "Tal Rasha's Lidless Eye",
  "Tal Rasha's Howling Wind",
  "Tal Rasha's Horadric Crest",
  "Griswold's Valor",
  "Griswold's Heart",
  "Griswolds's Redemption",
  "Griswold's Honor",
  "Trang-Oul's Guise",
  "Trang-Oul's Scales",
  "Trang-Oul's Wing",
  "Trang-Oul's Claws",
  "Trang-Oul's Girth",
  "M'avina's True Sight",
  "M'avina's Embrace",
  "M'avina's Icy Clutch",
  "M'avina's Tenet",
  "M'avina's Caster",
  "Telling of Beads",
  "Laying of Hands",
  "Rite of Passage",
  "Spiritual Custodian",
  "Credendum",
  "Dangoon's Teaching",
  "Heaven's Taebaek",
  "Haemosu's Adament",
  "Ondal's Almighty",
  "Guillaume's Face",
  "Wilhelm's Pride",
  "Magnus' Skin",
  "Wihtstan's Guard",
  "Hwanin's Splendor",
  "Hwanin's Refuge",
  "Hwanin's Seal",
  "Hwanin's Justice",
  "Sazabi's Cobalt Redeemer",
  "Sazabi's Ghost Liberator",
  "Sazabi's Mental Sheath",
  "Bul-Kathos' Sacred Charge",
  "Bul-Kathos' Tribal Guardian",
  "Cow King's Horns",
  "Cow King's Hide",
  "Cow King's Hoofs",
  "Naj's Puzzler",
  "Naj's Light Plate",
  "Naj's Circlet",
  "McAuley's Paragon",
  "McAuley's Riprap",
  "McAuley's Taboo",
  "McAuley's Superstition",
  "Warlord's Conquest",
  "Warlord's Lust",
  "Warlord's Mantle",
  "Warlord's Crushers",
  "Warlord's Authority",
]


# 自定义声音
CUSTOM_SOUNDS = {
    # Item
    "sc":                 {True: r"item\sc.flac",                  False: r"item\item_charm_hd.flac",   "path": "data/hd/global/sfx/item/sc.flac"},
    "lc":                 {True: r"item\lc.flac",                  False: r"item\item_charm_hd.flac",   "path": "data/hd/global/sfx/item/lc.flac"},  
    "gc":                 {True: r"item\gc.flac",                  False: r"item\item_charm_hd.flac",   "path": "data/hd/global/sfx/item/gc.flac"},
    "r01":                {True: r"item\r01.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r31.flac"},
    "r02":                {True: r"item\r02.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r32.flac"},
    "r03":                {True: r"item\r03.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r33.flac"},
    "r04":                {True: r"item\r04.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r24.flac"},
    "r05":                {True: r"item\r05.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r25.flac"},
    "r06":                {True: r"item\r06.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r26.flac"},
    "r07":                {True: r"item\r07.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r27.flac"},
    "r08":                {True: r"item\r08.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r28.flac"},
    "r09":                {True: r"item\r09.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r29.flac"},
    "r10":                {True: r"item\r10.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r30.flac"},
    "r11":                {True: r"item\r11.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r31.flac"},
    "r12":                {True: r"item\r12.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r32.flac"},
    "r13":                {True: r"item\r13.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r33.flac"},
    "r14":                {True: r"item\r14.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r24.flac"},
    "r15":                {True: r"item\r15.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r25.flac"},
    "r16":                {True: r"item\r16.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r26.flac"},
    "r17":                {True: r"item\r17.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r27.flac"},
    "r18":                {True: r"item\r18.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r28.flac"},
    "r19":                {True: r"item\r19.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r29.flac"},
    "r20":                {True: r"item\r20.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r30.flac"},
    "r21":                {True: r"item\r21.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r31.flac"},
    "r22":                {True: r"item\r22.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r32.flac"},
    "r23":                {True: r"item\r23.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r33.flac"},
    "r24":                {True: r"item\r24.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r24.flac"},
    "r25":                {True: r"item\r25.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r25.flac"},
    "r26":                {True: r"item\r26.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r26.flac"},
    "r27":                {True: r"item\r27.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r27.flac"},
    "r28":                {True: r"item\r28.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r28.flac"},
    "r29":                {True: r"item\r29.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r29.flac"},
    "r30":                {True: r"item\r30.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r30.flac"},
    "r31":                {True: r"item\r31.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r31.flac"},
    "r32":                {True: r"item\r32.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r32.flac"},
    "r33":                {True: r"item\r33.flac",                 False: r"item\item_rune_hd.flac",    "path": "data/hd/global/sfx/item/r33.flac"},
    "rin":                {True: r"item\rin.flac",                 False: r"item\item_ring_hd.flac",    "path": "data/hd/global/sfx/item/rin.flac"},
    "amu":                {True: r"item\amu.flac",                 False: r"item\item_amulet_hd.flac",  "path": "data/hd/global/sfx/item/amu.flac"},
    "jew":                {True: r"item\jew.flac",                 False: r"item\item_jewel_hd.flac",   "path": "data/hd/global/sfx/item/jew.flac"},
    "diadem":             {True: r"item\diadem.flac",              False: r"item\item_helm_hd.flac",    "path": "data/hd/global/sfx/item/diadem.flac"},
    "mephisto_key":       {True: r"item\torch_key.flac",           False: r"item\item_key_hd.flac",     "path": "data/hd/global/sfx/item/mephisto_key.flac"},
    # Skill
    "enchant_off":        {True: r"skill\enchant_off.flac",        False: r"none.flac",                 "path": "data/hd/global/sfx/skill/enchant_off.flac"},
    "chillingarmor_off":  {True: r"skill\chillingarmor_off.flac",  False: r"none.flac",                 "path": "data/hd/global/sfx/skill/chillingarmor_off.flac"},
    "shout_off":          {True: r"skill\shout_off.flac",          False: r"none.flac",                 "path": "data/hd/global/sfx/skill/shout_off.flac"},
    "energyshield_off":   {True: r"skill\energyshield_off.flac",   False: r"none.flac",                 "path": "data/hd/global/sfx/skill/energyshield_off.flac"},
    "venom_off":          {True: r"skill\venom_off.flac",          False: r"none.flac",                 "path": "data/hd/global/sfx/skill/venom_off.flac"},
    "battleorders_off":   {True: r"skill\battleorders_off.flac",   False: r"none.flac",                 "path": "data/hd/global/sfx/skill/battleorders_off.flac"},
    "battlecommand_off":  {True: r"skill\battlecommand_off.flac",  False: r"none.flac",                 "path": "data/hd/global/sfx/skill/battlecommand_off.flac"},
    "shiverarmor_off":    {True: r"skill\shiverarmor_off.flac",    False: r"none.flac",                 "path": "data/hd/global/sfx/skill/shiverarmor_off.flac"},
    "holyshield_off":     {True: r"skill\holyshield_off.flac",     False: r"none.flac",                 "path": "data/hd/global/sfx/skill/holyshield_off.flac"},
    "cyclonearmor_off":   {True: r"skill\cyclonearmor_off.flac",   False: r"none.flac",                 "path": "data/hd/global/sfx/skill/cyclonearmor_off.flac"},
    "quickness_off":      {True: r"skill\quickness_off.flac",      False: r"none.flac",                 "path": "data/hd/global/sfx/skill/quickness_off.flac"},
    "bladeshield_off":    {True: r"skill\bladeshield_off",         False: r"none.flac",                 "path": "data/hd/global/sfx/skill/bladeshield_off.flac"},
    "wolf_off":           {True: r"skill\wolf_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/wolf_off.flac"},
    "bear_off":           {True: r"skill\bear_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/bear_off.flac"},
    "frozenarmor_off":    {True: r"skill\frozenarmor_off.flac",    False: r"none.flac",                 "path": "data/hd/global/sfx/skill/frozenarmor_off.flac"},
    "bonearmor_off":      {True: r"skill\bonearmor_off.flac",      False: r"none.flac",                 "path": "data/hd/global/sfx/skill/bonearmor_off.flac"},
    "markwolf_off":       {True: r"skill\markwolf_off.flac",       False: r"none.flac",                 "path": "data/hd/global/sfx/skill/markwolf_off.flac"},
    "markbear_off":       {True: r"skill\markbear_off.flac",       False: r"none.flac",                 "path": "data/hd/global/sfx/skill/markbear_off.flac"},
    "fade_off":           {True: r"skill\fade_off.flac",           False: r"none.flac",                 "path": "data/hd/global/sfx/skill/fade_off.flac"},
    # Mercenaries
    "guard_death_hd1":    {True: r"monster\rogue\death1_hd.flac",  False: r"monster\guard\monster_guard_death_1_hd.flac",                 "path": ""},
    "guard_death_hd2":    {True: r"monster\rogue\death2_hd.flac",  False: r"monster\guard\monster_guard_death_2_hd.flac",                 "path": ""},
    "guard_death_hd3":    {True: r"monster\rogue\death1_hd.flac",  False: r"monster\guard\monster_guard_death_3_hd.flac",                 "path": ""},
    "guard_hit_hd1":      {True: r"monster\rogue\gethit1_hd.flac", False: r"monster\guard\monster_guard_gethit_1_hd.flac",                 "path": ""},
    "guard_hit_hd2":      {True: r"monster\rogue\gethit2_hd.flac", False: r"monster\guard\monster_guard_gethit_2_hd.flac",                 "path": ""},
    "guard_hit_hd3":      {True: r"monster\rogue\gethit3_hd.flac", False: r"monster\guard\monster_guard_gethit_3_hd.flac",                 "path": ""},
    "guard_hit_hd4":      {True: r"monster\rogue\gethit4_hd.flac", False: r"monster\guard\monster_guard_gethit_4_hd.flac",                 "path": ""},
}


# 导出所有需要的符号
__all__ = [
    'MUTEX_NAME',
    'ERROR_ALREADY_EXISTS',
    'WM_SHOW_WINDOW',
    'ZHCN',
    'ZHCN2',
    'ZHTW',
    'ZHTW2',
    'S2T',
    'T2S',
    'ENUS',
    'APP_NAME',
    'APP_VERSION',
    'APP_FULL_NAME',
    'APP_DATE',
    'APP_SIZE',
    'NETEASE_LANGUAGE',
    'BATTLE_NET_LANGUAGE',
    'TERROR_ZONE_SERVER',
    'TERROR_ZONE_LANGUAGE',
    'TERROR_ZONE_NEXT',
    'TERROR_ZONE_TABLE',
    'GAME_SETTING',
    'GAME_SETTING2',
    'GAME_SETTING3',
    'CONTROLS_SETTING',
    'LIGHT_REDIUS',
    'HUD_SIZE',
    'PORTAL_SKIN',
    'CHARACTER_EFFECTS',
    'ARROW',
    'SOR_SETTING',
    'TELEPORT_SKIN',
    'NEC_SETTING',
    'PAL_SETTING',
    'BAR_SETTING',
    'DRU_SETTING',
    'ASN_SETTING',
    'COMMON_SETTING',
    'SKILL_OFF_SOUNDS',
    'MERCENARY',
    'MERCENARY_LOCATION',
    'MERCENARY_100',
    'MERCENARY_85',
    'MERCENARY_75',
    'MERCENARY_65',
    'MONSTER_SETTING',
    'MONSTER_HEALTH',
    'MONSTER_MISSILE',
    'EQIUPMENT_EFFECTS',
    'EQIUPMENT_SETTING',
    'AFFIX_EFFECTS',
    'SETS_EFFECTS',
    'MODEL_EFFECTS',
    'RUNE_SIZE',
    'ITEM_NOTIFICATION',
    'ASSET_PATH',
    'ITEM_ENUS',
    'ITEM_ZHTW',
    'LNG_STRINGS',
    'TORCH_KEY',
    'ITEM_FILTER',
    'DISABLE_EFFECTS',
    'ENABLE_POINTER',
    'RADIO',
    'CHECK',
    'SPIN',
    'LOCATION',
    'SEPARATOR',
    'REGION_DOMAIN_MAP',
    'REGION_NAME_MAP',
    'UE01A',
    'TERROR_ZONE_API',
    'TERROR_ZONE_DICT',
    'TERROR_ZONE_MAP',
    'SETS_INDEX',
    'SET_ITEM_INDEX',
    'CUSTOM_SOUNDS',
    'WAYPOINT_POINTER',
    'MISSION_POINTER',
    'UPSTAIRS_POINTER',
    'DOWNSTAIRS_POINTER',
    'init_global_dict',
    'translate',
]