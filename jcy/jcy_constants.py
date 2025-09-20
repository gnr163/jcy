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
ZHTW = 'zhTW'
LANG = None

# 控制器名称
APP_NAME = "jcy控制器"

# MOD版本
APP_VERSION = "v1.2.0B"

# 发布日期
APP_DATE = "20250920"

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

# 恐怖区域API
TERROR_ZONE_API = {
    "default" : ["https://asia.d2tz.info/terror_zone?mode=online", "https://api.d2tz.info/terror_zone?mode=online"],
    "1": ["https://api.aws.d2-trade.com/api/query/tz_online"]
}
    

# 恐怖地带
TERROR_ZONE_DICT = {
  "1-1": {
    "zhCN": "鲜血荒地、 邪恶洞穴",
    "zhTW": "鮮血荒地、 邪惡洞窟",
    "enUS": "Blood Moor and Den of Evil"
  },
  "1-2": {
    "zhCN": "冰冷之原、洞穴",
    "zhTW": "冰冷之原、洞穴",
    "enUS": "Cold Plains and The Cave"
  },
  "1-3": {
    "zhCN": "埋骨之地、墓穴、寝陵",
    "zhTW": "埋骨之地、墓穴、大陵墓",
    "enUS": "Burial Grounds, The Crypt and The Mausoleum"
  },
  "1-4": {
    "zhCN": "石块旷野",
    "zhTW": "亂石曠野",
    "enUS": "Stony Field"
  },
  "1-5": {
    "zhCN": "崔斯特姆",
    "zhTW": "崔斯特姆",
    "enUS": "Tristram"
  },
  "1-6": {
    "zhCN": "黑暗森林、地下通道",
    "zhTW": "黑暗森林、地底通道",
    "enUS": "Dark Wood and Underground Passage"
  },
  "1-7": {
    "zhCN": "黑色沼泽、 洞坑",
    "zhTW": "黑色荒地、 地洞",
    "enUS": "Black Marsh and The Hole"
  },
  "1-8": {
    "zhCN": "被遗忘的高塔",
    "zhTW": "遺忘之塔",
    "enUS": "The Forgotten Tower"
  },
  "1-9": {
    "zhCN": "深坑",
    "zhTW": "地穴",
    "enUS": "The Pit"
  },
  "1-10": {
    "zhCN": "监牢、营房",
    "zhTW": "監牢、兵營",
    "enUS": "Jail and Barracks"
  },
  "1-11": {
    "zhCN": "大教堂、地下墓穴",
    "zhTW": "大教堂、地下墓穴",
    "enUS": "Cathedral and Catacombs"
  },
  "1-12": {
    "zhCN": "哞哞农场",
    "zhTW": "哞哞農場",
    "enUS": "Moo Moo Farm"
  },
  "2-1": {
    "zhCN": "下水道",
    "zhTW": "鲁高因下水道",
    "enUS": "Lut Gholein Sewers"
  },
  "2-2": {
    "zhCN": "碎石荒野、碎石古墓",
    "zhTW": "碎石荒地、古老石墓",
    "enUS": "Rocky Waste and Stony Tomb"
  },
  "2-3": {
    "zhCN": "干燥高地、亡者大殿",
    "zhTW": "乾土高地、死亡之殿",
    "enUS": "Dry Hills and Halls of the Dead"
  },
  "2-4": {
    "zhCN": "偏远绿洲",
    "zhTW": "遙遠的綠洲",
    "enUS": "Far Oasis"
  },
  "2-5": {
    "zhCN": "古代水道",
    "zhTW": "古代通道",
    "enUS": "Ancient Tunnels"
  },
  "2-6": {
    "zhCN": "失落之城、群蛇峡谷、利爪腹蛇神殿",
    "zhTW": "失落古城、群蛇峽谷、利爪蛇魔神殿",
    "enUS": "Lost City, Valley of Snakes and Claw Viper Temple"
  },
  "2-7": {
    "zhCN": "神秘避难所",
    "zhTW": "秘法聖殿",
    "enUS": "Arcane Sanctuary"
  },
  "2-8": {
    "zhCN": "塔•拉夏之墓、塔•拉夏的墓室",
    "zhTW": "塔拉夏的古墓、塔拉夏的密室",
    "enUS": "Tal Rasha's Tombs and Tal Rasha's Chamber"
  },
  "3-1": {
    "zhCN": "蜘蛛森林、蜘蛛洞穴",
    "zhTW": "蜘蛛森林、蜘蛛洞窟",
    "enUS": "Spider Forest and Spider Cavern"
  },
  "3-2": {
    "zhCN": "剥皮魔丛林、剥皮魔监牢",
    "zhTW": "剝皮叢林、剝皮地牢",
    "enUS": "Flayer Jungle and Flayer Dungeon"
  },
  "3-3": {
    "zhCN": "庞大湿地",
    "zhTW": "大沼澤",
    "enUS": "Great Marsh"
  },
  "3-4": {
    "zhCN": "库拉斯特集市、毁灭的神庙、废弃的礼拜堂",
    "zhTW": "庫拉斯特市集、荒廢的神殿、廢棄的寺院",
    "enUS": "Kurast Bazaar, Ruined Temple and Disused Fane"
  },
  "3-5": {
    "zhCN": "崔凡克",
    "zhTW": "崔凡克",
    "enUS": "Travincal"
  },
  "3-6": {
    "zhCN": "憎恨囚牢",
    "zhTW": "憎恨的囚牢",
    "enUS": "Durance of Hate"
  },
  "4-1": {
    "zhCN": "外围荒原、绝望平原",
    "zhTW": "外圍荒原、絕望平原",
    "enUS": "Outer Steppes and Plains of Despair"
  },
  "4-2": {
    "zhCN": "火焰之河、神罚之城",
    "zhTW": "火焰之河、罪罰之城",
    "enUS": "River of Flame and City of the Damned"
  },
  "4-3": {
    "zhCN": "混沌避难所",
    "zhTW": "混沌庇難所",
    "enUS": "Chaos Sanctuary"
  },
  "5-1": {
    "zhCN": "血腥丘陵、冰冻高地、亚巴顿",
    "zhTW": "血腥丘陵、冰凍高地、亞巴頓",
    "enUS": "Bloody Foothills, Frigid Highlands and Abaddon"
  },
  "5-2": {
    "zhCN": "冰川小径、漂流洞窟",
    "zhTW": "冰河小径、漂泊者洞窟",
    "enUS": "Glacial Trail and Drifter Cavern"
  },
  "5-3": {
    "zhCN": "先祖之路、寒冰地窖",
    "zhTW": "先祖之路、冰窖",
    "enUS": "Ancient's Way and Icy Cellar"
  },
  "5-4": {
    "zhCN": "亚瑞特高原、阿克隆深渊",
    "zhTW": "亞瑞特高原、冥河地穴",
    "enUS": "Arreat Plateau and Pit of Acheron"
  },
  "5-5": {
    "zhCN": "水晶通道、冰冻之河",
    "zhTW": "水晶通道、冰凍之河",
    "enUS": "Crystalline Passage and Frozen River"
  },
  "5-6": {
    "zhCN": "尼拉塞克的神殿、痛楚大厅、苦痛大厅、沃特大厅",
    "zhTW": "尼拉塞克神殿、怨慟之廳、苦痛之廳、沃特之廳",
    "enUS": "Nihlathak's Temple and Temple Halls"
  },
  "5-7": {
    "zhCN": "世界之石要塞、毁灭王座、世界之石大殿",
    "zhTW": "世界之石要塞、毀滅王座、世界之石大殿",
    "enUS": "Worldstone Keep, Throne of Destruction and Worldstone Chamber"
  }
}

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

# 导出所有需要的符号
__all__ = [
    'MUTEX_NAME',
    'ERROR_ALREADY_EXISTS',
    'WM_SHOW_WINDOW',
    'ENUS',
    'ZHCN',
    'ZHTW',
    'APP_NAME',
    'APP_VERSION',
    'APP_FULL_NAME',
    'APP_DATE',
    'APP_SIZE',
    'REGION_DOMAIN_MAP',
    'REGION_NAME_MAP',
    'UE01A',
    'TERROR_ZONE_API',
    'TERROR_ZONE_DICT',
    'SET_ITEM_INDEX',
    'initLanguage',
    'getLanguage'
]

def initLanguage(language):
    global LANG
    if "default" == language:
        LANG = ZHTW
    elif "1" == language:
        LANG = ZHCN
    else:
        LANG = ENUS

def getLanguage():
    return LANG