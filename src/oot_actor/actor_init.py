from cole.getters import getCategories
from cole.data import OoTActorProperty, objNameToTarget, paramPrefixList
from .actor_getters import getActorIDFromName
from .actor_widgets import stringProperty, enumProperty, boolProperty


def initActorConnections(self):
    """Initialises the actor callbacks"""
    self.searchBox.textChanged.connect(self.searchBoxOnUpdate)
    self.actorCategoryList.currentTextChanged.connect(self.searchBoxOnUpdate)
    self.actorFoundBox.currentTextChanged.connect(self.foundBoxOnUpdate)
    self.actorTypeList.currentTextChanged.connect(self.typeBoxOnUpdate)
    self.ignoreTiedBox.stateChanged.connect(self.typeBoxOnUpdate)
    self.openActorFileBtn.clicked.connect(self.openActorFile)
    self.saveActorFileBtn.clicked.connect(self.saveActorFile)
    # self.addActorBtn.clicked.connect()
    self.deleteActorBtn.clicked.connect(self.deleteActor)
    self.evalParamBox.stateChanged.connect(self.paramOnUpdate)
    self.deleteAllBtn.clicked.connect(self.deleteAll)
    for prefix in paramPrefixList:
        for suffix in ["Box", "Label"]:
            widget = getattr(self, f"{prefix}{suffix}")
            if widget is not None:
                if suffix == "Box":
                    widget.editingFinished.connect(self.setParams)
                elif suffix == "Label":
                    widget.clicked.connect(self.copyParam)


def initActorComponents(self):
    """Initialises the actor tab components"""
    self.actorCategoryList.clear()
    self.actorCategoryList.addItems(getCategories(self.actorRoot))
    self.searchBoxOnUpdate()
    self.paramLayout.setHorizontalSpacing(30)
    self.ignoreTiedBox.setHidden(True)
    initOoTActorProperties(self)


def initOoTActorProperties(self):
    """This function is used to edit the OoTActorProperty class"""
    propAnnotations = getattr(OoTActorProperty, "__annotations__", None)
    if propAnnotations is None:
        OoTActorProperty.__annotations__ = propAnnotations = {}

    # Lists of the different enums, with the identifier, name and value
    itemDrops = [
        (elem.get("Key"), elem.get("Name"), elem.get("Value"))
        for listNode in self.actorRoot
        for elem in listNode
        if listNode.tag == "List" and listNode.get("Name") == "Collectibles"
    ]

    chestContent = [
        (elem.get("Key"), elem.get("Name"), elem.get("Value"))
        for listNode in self.actorRoot
        for elem in listNode
        if listNode.tag == "List" and listNode.get("Name") == "Chest Content"
    ]

    messageID = [
        (elem.get("Key"), elem.get("Name"), elem.get("Value"))
        for listNode in self.actorRoot
        for elem in listNode
        if listNode.tag == "List" and listNode.get("Name") == "Elf_Msg Message ID"
    ]

    # for each element and sub-element in the XML
    # which is an actor, generate the corresponding props
    for actorNode in self.actorRoot:
        actorTypes = []
        actorEnums = []
        actorEnumNames = []
        actorKey = actorNode.get("Key")

        for elem in actorNode:
            index = int(elem.get("Index", "1"), base=10)
            if elem.tag == "Property":
                objName = actorKey + f".props{index}"
                strProp, label = stringProperty(self, objName, name=elem.get("Name"), default="0x0")
                propAnnotations[objName] = strProp
                propAnnotations[f"{objName}.label"] = label
            elif elem.tag == "Flag":
                flagType = elem.get("Type")
                if flagType == "Chest":
                    objName = actorKey + f".chestFlag{index}"
                    strProp, label = stringProperty(self, objName, name="Chest Flag", default="0x0")
                    propAnnotations[objName] = strProp
                    propAnnotations[f"{objName}.label"] = label
                elif flagType == "Collectible":
                    objName = actorKey + f".collectibleFlag{index}"
                    strProp, label = stringProperty(self, objName, name="Collectible Flag", default="0x0")
                    propAnnotations[objName] = strProp
                    propAnnotations[f"{objName}.label"] = label
                elif flagType == "Switch":
                    objName = actorKey + f".switchFlag{index}"
                    strProp, label = stringProperty(self, objName, name="Switch Flag", default="0x0")
                    propAnnotations[objName] = strProp
                    propAnnotations[f"{objName}.label"] = label
            elif elem.tag == "Collectible":
                objName = actorKey + f".collectibleDrop{index}"
                enumProp, label = enumProperty(self, objName, name="Collectible Drop", items=itemDrops)
                propAnnotations[objName] = enumProp
                propAnnotations[f"{objName}.label"] = label
                propAnnotations[f"{objName}.list"] = itemDrops
            elif elem.tag == "ChestContent":
                objName = actorKey + f".itemChest{index}"
                enumProp, label = enumProperty(self, objName, name="Chest Content", items=chestContent)
                propAnnotations[objName] = enumProp
                propAnnotations[f"{objName}.label"] = label
                propAnnotations[f"{objName}.list"] = chestContent
            elif elem.tag == "Message":
                objName = actorKey + f".msgID{index}"
                enumProp, label = enumProperty(self, objName, name="Message ID", items=messageID)
                propAnnotations[objName] = enumProp
                propAnnotations[f"{objName}.label"] = label
                propAnnotations[f"{objName}.list"] = messageID
            elif elem.tag == "Type":
                actorTypes.append([(item.get("Params"), item.text, item.get("Params")) for item in elem])
            elif elem.tag == "Bool":
                objName = actorKey + f".bool{index}"
                propAnnotations[objName] = boolProperty(self, objName, elem.get("Name"), default=False)
                propAnnotations[f"{objName}.label"] = None
            elif elem.tag == "Enum":
                actorEnums.append([(item.get("Value"), item.get("Name"), item.get("Value")) for item in elem])
                actorEnumNames.append(elem.get("Name"))
        if actorNode.tag == "Actor":
            for index, elem in enumerate(actorTypes, 1):
                propAnnotations[(actorKey + f".type{index}")] = elem
                propAnnotations[(actorKey + f".type{index}.index")] = 0
            for index, elem in enumerate(actorEnums, 1):
                objName = actorKey + f".enum{index}"
                enumProp, label = enumProperty(self, objName, name=actorEnumNames[index - 1], items=elem)
                propAnnotations[objName] = enumProp
                propAnnotations[f"{objName}.label"] = label
                propAnnotations[f"{objName}.list"] = elem


def initActorTypeBox(self):
    """Adds items to the type combo box"""
    self.actorTypeList.setEnabled(False)
    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        actorID = getActorIDFromName(self.actorRoot, selectedItem.text())
        self.actorTypeList.clear()
        for actor in self.actorRoot:
            if actor.get("ID") == actorID:
                for elem in actor:
                    if elem.tag == "Type":
                        objName = actor.get("Key") + f".type{elem.get('Index', '1')}"
                        typeList = OoTActorProperty.__annotations__[objName]
                        items = [type[1] for type in typeList]
                        if items is not None and (len(items) > 0):
                            self.actorTypeList.addItems(items)
                            self.actorTypeList.setEnabled(True)
                            self.actorTypeList.setCurrentIndex(OoTActorProperty.__annotations__[f"{objName}.index"])
                        return


def initParamBox(self):
    """Enables the label and the line edit if the actor has the corresponding target"""
    targetList = []

    selectedItem = self.actorFoundBox.currentItem()
    if selectedItem is not None:
        actorID = getActorIDFromName(self.actorRoot, selectedItem.text())
        for actor in self.actorRoot:
            if actor.get("ID") == actorID:
                for elem in actor:
                    targetList.append(elem.get("Target", "Params"))

    for prefix in paramPrefixList:
        for suffix in ["Box", "Label"]:
            objName = f"{prefix}{suffix}"
            isEnabled = True if objNameToTarget[objName] in targetList and not self.ignoreTiedBox.isChecked() else False
            widget = getattr(self, objName)
            widget.setEnabled(isEnabled)
