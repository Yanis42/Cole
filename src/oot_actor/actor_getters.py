from xml.etree import ElementTree as ET
from ast import parse, Expression, Num, UnaryOp, USub, Invert, BinOp
from cole.data import OoTActorProperty, actorCatDebugToNormal, binOps
from cole.getters import getShiftFromMask


def getActors(actorRoot: ET.Element, searchInput: str, categoryInput: str):
    """Returns every actor that contains the value from ``searchInput`` and ``categoryInput``"""
    # using lowercase for every string
    searchInput = searchInput.lower()

    # search results list
    results = []

    # going through the XML data
    for actor in actorRoot:
        if actor is not None and actor.tag == "Actor":
            # search by ID, key, category and name
            actorID = actor.get("ID", "").lower()
            actorKey = actor.get("Key", "").lower()
            actorCategory = actor.get("Category")
            actorName = actor.get("Name", "")

            isInputInName = (
                searchInput in actorName.lower()
                or searchInput in actorKey
                or searchInput in actorID
                or (searchInput == "")
                or searchInput in actorID.replace("_", " ")
                or searchInput in actorKey.replace("_", " ")
            ) and (categoryInput in actorCatDebugToNormal[actorCategory] or (categoryInput == "All"))

            # add the actor if we have a match, else remove it,
            # check if the actor is already in the list for both case
            if isInputInName:
                if not actorName in results:
                    results.append(actorName)
            else:
                if actorName in results:
                    results.remove(actorName)
    return results


def getActorIDFromName(actorRoot: ET.Element, actorName: str):
    """Returns an actor's ID from its name"""
    for actor in actorRoot:
        if actor.tag == "Actor" and actorName == actor.get("Name"):
            return actor.get("ID")
    return


def getActorTypeValue(self, actor: ET.Element, selectedIndex: int, actorID: str):
    """Returns an actor's type list value"""
    if not self.actorTypeList.isEnabled():
        return "0000"
    elif actor.get("ID") == actorID:
        for elem in actor:
            if elem.tag == "Type":
                objName = actor.get("Key") + f".type{elem.get('Index', '1')}"
                return getEnumValueFromObjName(objName, selectedIndex)
    return


def getActorEnumValue(actor: ET.Element, elem: ET.Element, selectedIndex: int, actorID: str, elemTag: str):
    """Returns an actor's enum param value"""
    if actor.get("ID") == actorID:
        actorKey = actor.get("Key")
        index = elem.get("Index", "1")
        objName = getListObjName(elem, elemTag, actorKey, index)
        if objName is not None:
            return getEnumValueFromObjName(objName, selectedIndex)
    return


def getListObjName(elem: ET.Element, elemTag: str, actorKey: str, index: str):
    """Returns the name of the list containing the ComboBox items"""
    if elem.tag == elemTag == "Enum":
        return actorKey + f".enum{index}.list"
    elif elem.tag == elemTag == "ChestContent":
        return actorKey + f".itemChest{index}.list"
    elif elem.tag == elemTag == "Message":
        return actorKey + f".msgID{index}.list"
    elif elem.tag == elemTag == "Collectible":
        return actorKey + f".collectibleDrop{index}.list"
    return


def getEnumValueFromObjName(objName: str, index: int):
    """Returns the value using the object name"""
    # see ``initOoTActorProperties`` for list format
    enumList = OoTActorProperty.__annotations__[objName]
    if enumList is not None:
        return enumList[index][2]
    return


def getEvalParams(params: str):
    """
    Evaluate the params string argument to an integer
    Raises ValueError if something goes wrong
    """

    if params is None or "None" in params:
        return "0x0"

    if not "0x" in params and not ("<<" in params or "&" in params):
        params = f"0x{params}"

    # remove spaces
    params = params.strip()

    try:
        node = parse(params, mode="eval")
    except Exception as e:
        raise ValueError(f"Could not parse params {params} as an AST.") from e

    def _eval(node):
        if isinstance(node, Expression):
            return _eval(node.body)
        elif isinstance(node, Num):
            return node.n
        elif isinstance(node, UnaryOp):
            if isinstance(node.op, USub):
                return -_eval(node.operand)
            elif isinstance(node.op, Invert):
                return ~_eval(node.operand)
            else:
                raise ValueError(f"Unsupported unary operator {node.op}")
        elif isinstance(node, BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise ValueError(f"Unsupported AST node {node}")

    return f"0x{_eval(node.body):X}"


def getFormattedParams(mask: int, value: str, isBool: bool):
    """Returns the parameter with the correct format"""
    shift = getShiftFromMask(mask) if mask is not None else 0

    if not int(getEvalParams(value), base=16):
        return
    elif not isBool:
        if shift > 0:
            return f"(({value} << {shift}) & 0x{mask:04X})"
        else:
            return f"({value} & 0x{mask:04X})"
    else:
        return f"({value} << {shift})"


def getParamValue(self, actor: ET.Element, target: str):
    """Returns a list of the parameters for a specific target for widgets which are displayed"""
    # this function should be called when we know for sure it's the right actor
    params = []
    actorID = actor.get("ID")
    typeParam = getActorTypeValue(self, actor, self.actorTypeList.currentIndex(), actorID)

    # iterates through the sub-elements of the actor
    for elem in actor:
        objName = getObjName(actor, elem)
        tiedTypeList = elem.get("TiedActorTypes")
        # we don't want <Type> and <Notes>, also look for tied params
        if (
            objName is not None
            and not (elem.tag == "Type")
            and not (elem.tag == "Notes")
            and getTiedParams(tiedTypeList, typeParam)
        ):
            widget = OoTActorProperty.__annotations__[objName]

            # get the value for each widget on screen
            if elem.get("Target", "Params") == target:
                # get the param value of this widget then add it to the list
                value = None
                mask = int(elem.get("Mask", "0x0"), base=16)
                if (
                    elem.tag == "Enum"
                    or elem.tag == "ChestContent"
                    or elem.tag == "Collectible"
                    or elem.tag == "Message"
                ):
                    enumParam = getActorEnumValue(actor, elem, widget.currentIndex(), actor.get("ID"), elem.tag)
                    value = enumParam if enumParam is not None else "0x0"
                elif (elem.tag == "Property") or (elem.tag == "Flag"):
                    value = widget.text()
                elif elem.tag == "Bool":
                    value = "1" if widget.isChecked() else "0"

                if not (value == "0" or value == "1"):
                    value = getFormattedParams(mask, value, False)
                else:
                    value = getFormattedParams(mask, value, True)

                if value is not None and not value in params:
                    params.append(value)
    return params


def getObjName(actor: ET.Element, elem: ET.Element):
    """Returns the object name from the current actor's informations"""
    actorKey = actor.get("Key")
    index = int(elem.get("Index", "1"), base=10)

    if elem.tag == "Property":
        return actorKey + f".props{index}"
    elif elem.tag == "Flag":
        flagType = elem.get("Type")
        if flagType == "Chest":
            return actorKey + f".chestFlag{index}"
        elif flagType == "Collectible":
            return actorKey + f".collectibleFlag{index}"
        elif flagType == "Switch":
            return actorKey + f".switchFlag{index}"
    elif elem.tag == "Collectible":
        return actorKey + f".collectibleDrop{index}"
    elif elem.tag == "ChestContent":
        return actorKey + f".itemChest{index}"
    elif elem.tag == "Message":
        return actorKey + f".msgID{index}"
    elif elem.tag == "Bool":
        return actorKey + f".bool{index}"
    elif elem.tag == "Enum":
        return actorKey + f".enum{index}"
    return


def getTiedParams(tiedTypeList: str, typeParam: str):
    return tiedTypeList is None or (
        tiedTypeList is not None and typeParam is not None and typeParam in tiedTypeList.split(",")
    )


def getFinalParams(self, actor: ET.Element, target: str, params: str):
    typeParam = getActorTypeValue(self, actor, self.actorTypeList.currentIndex(), actor.get("ID"))
    params = getParamValue(self, actor, target) if params is None else params
    paramValue = " | ".join(params) if len(params) > 0 else "0x0"
    if target == "Params":
        evalType = int(getEvalParams(f"0x{typeParam}"), base=16)
        evalParamValue = int(getEvalParams(paramValue), base=16)
        if evalType and evalParamValue:
            paramValue = f"(0x{typeParam} | ({paramValue}))"
        elif evalType and not evalParamValue:
            paramValue = f"0x{typeParam}"
        elif not evalType and evalParamValue:
            paramValue = f"({paramValue})"
        else:
            paramValue = "0x0"
    return paramValue
