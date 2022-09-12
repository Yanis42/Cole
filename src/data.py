uiFile = "res/MainWindow.ui"

actorRoot = None

paramWidgets = []

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
