from ast import Add, Sub, Mult, Div, Mod, LShift, RShift, RShift, BitOr, BitAnd, BitXor
from operator import add, sub, mul, truediv, mod, lshift, rshift, rshift, or_, and_, xor

uiFile = "res/MainWindow.ui"

# format of both lists: ({identifier}, {label widget}, {parameter widget})
paramWidgets = []  # contains every parameter widget
shownWidgets = []  # contains every parameter widget that are currently displayed

actorCatDebugToNormal = {
    "ACTORCAT_SWITCH": "Switch",
    "ACTORCAT_BG": "BG Actor",
    "ACTORCAT_PLAYER": "Player",
    "ACTORCAT_EXPLOSIVE": "Explosive",
    "ACTORCAT_NPC": "NPC",
    "ACTORCAT_ENEMY": "Enemy",
    "ACTORCAT_PROP": "Props",
    "ACTORCAT_ITEMACTION": "Item/Action",
    "ACTORCAT_MISC": "Misc",
    "ACTORCAT_BOSS": "Boss",
    "ACTORCAT_DOOR": "Door",
    "ACTORCAT_CHEST": "Chest",
}

subElemTags = [
    "Enum",
    "Property",
    "Flag",
    "Bool",
    "ChestContent",
    "Collectible",
    "Message",
]

tagToWidget = {
    "Enum": "ComboBox",
    "Property": "LineEdit",
    "Flag": "LineEdit",
    "Bool": "CheckBox",
    "ChestContent": "ComboBox",
    "Collectible": "ComboBox",
    "Message": "ComboBox",
}

# binary operators for the eval function
binOps = {
    Add: add,
    Sub: sub,
    Mult: mul,
    Div: truediv,
    Mod: mod,
    LShift: lshift,
    RShift: rshift,
    RShift: rshift,
    BitOr: or_,
    BitAnd: and_,
    BitXor: xor,
}
