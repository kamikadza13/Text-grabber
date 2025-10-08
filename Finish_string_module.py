import copy
import html
import re
from dataclasses import dataclass
from re import match
from typing import Optional

# # from xml import etree as ET
# from xml.etree import ElementTree as ET
from lxml import etree as ET, etree
from lxml.etree import _Element, _Comment

from GlobFunc import error_handler
from GlobVars import Error_log
from Settings_module import SVV as S

tag_endwith_skip = ['\\nodes\\Set\\name', ]
text_startwith_skip = ['RGB', r'\$', ]
ruleFiles_list = {}

debug_print_bool = False




@dataclass
class FolderDefnamePathText:
    folder: str
    defname: str
    path: str
    text: str


@dataclass
class ExitList:
    fdpt: list[FolderDefnamePathText]
    keyed: list


def RulePackDef_def(rulePackDef: _Element):
    global ruleFiles_list
    defName_ET = rulePackDef.find('defName')
    if defName_ET is not None:
        defname = defName_ET.text
    else:
        return
    rulesFiles_ET = list(rulePackDef.iter('rulesFiles'))
    if rulesFiles_ET:
        rulesFiles_ET = rulesFiles_ET[0]
        for li in rulesFiles_ET:
            if isinstance(li, _Comment):
                continue
            a = li.text
            b = a.partition("-")[0]
            if not ruleFiles_list.get(defname):
                ruleFiles_list[defname] = []
            ruleFiles_list[defname].append((b, li))

    include = []
    include_ET = list(rulePackDef.iter('include'))
    if include_ET:
        include_ET = include_ET[0]
        for li in include_ET:
            if isinstance(li, _Comment):
                continue
            include.append(li.text)

    rulesStrings_ET = list(rulePackDef.iter('rulesStrings'))
    if rulesStrings_ET:
        rulesStrings_ET = rulesStrings_ET[0]
    if include:
        if not rulesFiles_ET:
            rulesFiles = etree.Element('rulesFiles')
        else:
            rulesFiles = rulesFiles_ET
        rulePackDef.insert(1, rulesFiles)

        if rulesStrings_ET is not None:
            rulesStrings_ET = ET.SubElement(rulePackDef, 'rulesStrings')
        for defname_ in include:
            if defname_ in ruleFiles_list:
                for line in ruleFiles_list[defname_]:

                    if f'[{line[0]}]'.encode() in ET.tostring(rulesStrings_ET, method='xml'):
                        rulesFiles.append(copy.deepcopy(line[1]))


def BodyDef_rename_li(BodyDef: _Element):
    def parts_li_tag_rename(el: _Element):
        parts = el.find('parts')
        if parts is not None:

            for idx, li in enumerate(parts):
                customLabel = li.find('customLabel')
                if customLabel is not None:
                    if customLabel.text is not None:
                        try:
                            li.tag = customLabel.text.replace(" ", "_").replace("-", "")

                        except ValueError:
                            li.tag = 'LI_REPLACE_NUMBER' + str(idx)

                parts_li_tag_rename(li)



    corePart = BodyDef.find('corePart')
    if corePart is not None:
        parts_li_tag_rename(corePart)


def pawnKind_add_strings(elem: _Element):
    add_elem = []
    a: list[_Element] = []
    b = elem.find('lifeStages')
    orig_label_text = ''

    def get_label(elem_to_get_label: _Element):
        _ = elem_to_get_label.find('label')
        if _ is not None:
            return str(elem.find('label').text)
        return ""

    if b is not None:
        for li in b:
            if isinstance(li, _Comment):
                continue
            if li is not None:
                a.append(li)
    orig_label_text = get_label(elem)
    for els in a:
        label_text = get_label(els)
        if not label_text:
            label_text = orig_label_text
        if label_text:
            for idx_, l_pawn in enumerate(S.get_plural_list()):
                add_elem.append(etree.Element(l_pawn))
                if els.find(l_pawn) is None:
                    els.append(add_elem[idx_])
                    txt = str(l_pawn.partition("label")[2])
                    # print(txt)
                    txt = txt.replace('ePlural', 'e Plural')
                    # print(txt)
                    add_elem[idx_].text = txt + " " + label_text


def ScenarioDef_add_strings(elem: _Element):
    if elem.find('scenario') is not None:
        scenario = elem.find('scenario')
        # print(f"Есть ветка scenario")
        if scenario.find("name") is None:
            label = elem.find("label")
            if label is not None:
                scenario_name = ET.SubElement(scenario, 'name')
                scenario_name.text = label.text

        if scenario.find("description") is None:
            description = elem.find("description")
            if description is not None:
                scenario.append(description)
    else:
        print(f"Нет ветки scenario???")
        label = elem.find("label")
        scenario = ET.SubElement(elem, "scenario")
        if label is not None:
            scenario_name = ET.SubElement(scenario, 'name')
            scenario_name.text = label.text
        description = elem.find("description")
        if description is not None:
            scenario.append(description)


def DamageDef_add_strings(elem: _Element):
    if elem.find("deathMessage") is None:
        deathMessage = ET.SubElement(elem, "deathMessage")
        a_00 = elem.get('ParentName')

        if S.Translate_tools_into_russian:
            match a_00:
                case "Flame":
                    deathMessage.text = "{0} был сожжен до смерти."
                case "CutBase":
                    deathMessage.text = "{0} был зарезан насмерть."
                case "BluntBase":
                    deathMessage.text = "{0} был избит до смерти."
                case "Scratch":
                    deathMessage.text = "{0} был растерзан до смерти."
                case "Bite":
                    deathMessage.text = "{0} был искусан до смерти."
                case "Bomb":
                    deathMessage.text = "{0} погиб при взрыве."
                case "Arrow":
                    deathMessage.text = "{0} был застрелен стрелой."
                case _:
                    deathMessage.text = "{0} был убит."
        else:
            match a_00:
                case "Flame":
                    deathMessage.text = "{0} has burned to death."
                case "CutBase":
                    deathMessage.text = "{0} has been cut to death."
                case "BluntBase":
                    deathMessage.text = "{0} has been beaten to death."
                case "Scratch":
                    deathMessage.text = "{0} has been torn to death."
                case "Bite":
                    deathMessage.text = "{0} has been bitten to death."
                case "Bomb":
                    deathMessage.text = "{0} has died in an explosion."
                case "Arrow":
                    deathMessage.text = "{0} has been shot to death by an arrow."
                case _:
                    deathMessage.text = "{0} has been killed."


# def comps_Li_Class_Replace(Def: _Element):
#     comps = Def.find("comps")
#     if comps is not None:
#         for li in comps:
#             compClass = li.find("compClass")
#             if compClass is not None:
#                 # print(f"{Def.tag}:")
#                 # print(f"Replace <li> by compClass {compClass.text}")
#                 li.tag = compClass.text
#                 if li.get("Class") is not None:
#                     li.set('Class', "Li_Class_Replaced_by_compClass")

def translate_ThingDef_tools(el1: _Element):
    """tools.0"""
    if S.Translate_tools_into_russian:
        tools = el1.find("tools")
        if tools is not None:
            for li in tools:
                if isinstance(li, _Comment):
                    continue
                for t in li:
                    if isinstance(t, _Comment):
                        continue
                    if t.tag == 'label':
                        match t.text.lower():
                            case "stock":
                                t.text = "приклад"
                            case "barrel":
                                t.text = "ствол"
                            case "muzzle":
                                t.text = "дуло"
                            case "grip":
                                t.text = "рукоятка"
                            case "body":
                                t.text = "корпус"
                            case "shaft":
                                t.text = "древко"
                            case "point":
                                t.text = "острие"
                            case "handle":
                                t.text = "рукоять"
                            case "fist":
                                t.text = "кулак"
                            case "teeth":
                                t.text = "зубы"
                            case "claw":
                                t.text = "коготь"
                            case "claws":
                                t.text = "когти"
                            case "drill":
                                t.text = "сверло"
                            case "left claw":
                                t.text = "левый коготь"
                            case "right claw":
                                t.text = "правый коготь"
                            case "jaw":
                                t.text = "челюсть"
                            case "blade":
                                t.text = "лезвие"
                            case "edge":
                                t.text = "кромка"
                            case "leg":
                                t.text = "нога"
                            case "legs":
                                t.text = "ноги"
                            case "arm":
                                t.text = "рука"
                            case "arms":
                                t.text = "руки"
                            case "head":
                                t.text = "голова"
                            case "horn":
                                t.text = "рог"
                            case "left paw":
                                t.text = "левая лапа"
                            case "right paw":
                                t.text = "правая лапа"
                            case "beak":
                                t.text = "клюв"
                            case "left hoof":
                                t.text = "левое копыто"
                            case "right hoof":
                                t.text = "правое копыто"
                            case "antlers":
                                t.text = "рога"
                            case 'left fist':
                                t.text = "левый кулак"
                            case 'right fist':
                                t.text = "правый кулак"
                            case 'right blade':
                                t.text = "правый клинок"
                            case 'left blade':
                                t.text = "левый клинок"
                            case 'body':
                                t.text = "корпус"
                            case 'torso':
                                t.text = "торс"
                            case 'left power claw':
                                t.text = "левый силовой коготь"
                            case 'right power claw':
                                t.text = "правый силовой коготь"
                            case 'mandibles':
                                t.text = "нижняя челюсть"
                            case 'tusk':
                                t.text = "бивень"
                            case 'neck':
                                t.text = "горловина"
                            case 'bayonet':
                                t.text = "штык"
                            case 'fangs':
                                t.text = "клыки"
                            case 'left claws':
                                t.text = "левые когти"
                            case 'right claws':
                                t.text = "правые когти"
                            case 'chain':
                                t.text = "цепь"
                            case 'venom fangs':
                                t.text = "ядовитые клыки"
                            case 'head claw':
                                t.text = "головной коготь"
                            case 'left wing':
                                t.text = "левое крыло"
                            case 'right wing':
                                t.text = "правое крыло"
                            case 'manipulator':
                                t.text = "манипулятор"
                            case 'bodyslam':
                                t.text = "удар корпусом"
                            case 'left hand':
                                t.text = "левая рука"
                            case 'right hand':
                                t.text = "правая рука"
                            case 'spike':
                                t.text = "шип"
                            case 'axe':
                                t.text = "топор"
                            case 'hammer':
                                t.text = "молот"
                            case 'left branch':
                                t.text = "левая ветвь"
                            case 'right branch':
                                t.text = "правая ветвь"
                            case 'left fin':
                                t.text = "левый плавник"
                            case 'right fin':
                                t.text = "правый плавник"
                            case 'tentacle':
                                t.text = "щупальце"
                            case 'left spike':
                                t.text = "левый шип"
                            case 'right spike':
                                t.text = "правый шип"
                            case 'top spike':
                                t.text = "верхний шип"
                            case 'barrels':
                                t.text = "стволы"
                            case 'pickaxe':
                                t.text = "кирка"
                            case 'chainsaw':
                                t.text = "бензопила"
                            case 'spine':
                                t.text = "позвоночник"
                            case 'tail':
                                t.text = "хвост"
                            case 'front left leg':
                                t.text = "передняя левая нога"
                            case 'front right leg':
                                t.text = "передняя правая нога"
                            case 'hooves':
                                t.text = "копыта"
                            case 'left mace':
                                t.text = "левая булава"
                            case 'right mace':
                                t.text = "правая булава"
                            case 'bionic fist':
                                t.text = "бионический кулак"
                            case 'venomous talons':
                                t.text = "ядовитые когти"
                            case 'tail spikes':
                                t.text = "хвостовые шипы"
                            case 'arm blade':
                                t.text = "ручной клинок"
                            case 'tentacles':
                                t.text = "щупальца"
                            case 'wings':
                                t.text = "крылья"
                            case 'maw':
                                t.text = "пасть"
                            case 'needles':
                                t.text = "иглы"
                            case 'left hammer fist':
                                t.text = "левый кулак молот"
                            case 'right hammer fist':
                                t.text = "правый кулак молот"
                            case 'scyther blade':
                                t.text = "клинок косы"
                            case 'acid fangs':
                                t.text = "кислотные клыки"
                            case 'clawed hand':
                                t.text = "когтистая рука"
                            case 'left pincer':
                                t.text = "левая клешня"
                            case 'right pincer':
                                t.text = "правая клешня"
                            case 'eye':
                                t.text = "глаз"
                            case 'venomous spit':
                                t.text = "ядовитый плевок"
                            case 'acid spit':
                                t.text = "кислотный плевок"
                            case 'left hand claws':
                                t.text = "когти левой руки"
                            case 'right hand claws':
                                t.text = "когти правой руки"
                            case 'venom-fangs':
                                t.text = "ядовитые клыки"
                            case 'sharp talons':
                                t.text = "острые когти"
                            case 'tail spear':
                                t.text = "хвостовое копьё"


def add_missing_verbs_if_verbClass(Def: _Element):
    """Verb_Shoot
    VerbClass"""
    verbs = Def.find("verbs")
    if verbs is not None:
        for idx, li in enumerate(verbs):
            if not (li.tag.isdigit() or li.tag == "li"):
                continue

            verb_Class = li.find("verbClass")
            if verb_Class is None:
                return

            li_label = li.find("label")
            if li_label is not None:
                vc_label = verbs.find(verb_Class.text)
                if vc_label is None:
                    """Add QM_String21MHG.verbs.(Verb_Class).label"""
                    verb_verbclass = ET.SubElement(verbs, verb_Class.text)
                    ET.SubElement(verb_verbclass, 'label').text = "ㅤ"  # Пустой символ

            else:
                ET.SubElement(li, 'label').text = "ㅤ"    # Пустой символ

            if idx == 0:
                if li_label is not None:
                    if li_label.text is not None:
                        match li_label.text:
                            case 'ㅤ':
                                ...
                            case 'Gun':
                                li_label.text = ''

                            case s if s.islower():
                                ...

                            case s if ' ' not in s:
                                li_label.text = ''

                            case _:
                                ...





def ThingDef_add_strings(elem: _Element):
    if S.Add_stuffAdjective_and_mark_it:

        stuffProps = elem.find("stuffProps")
        if stuffProps is not None:
            categories = stuffProps.find("categories")
            if categories is not None:
                if elem.find("label") is not None:
                    label = elem.find("label").text
                else:
                    label = "material"
                a = stuffProps.find('stuffAdjective')
                if a is None:
                    stuffAdjective = ET.SubElement(stuffProps, "stuffAdjective")

                    stuffAdjective.text = S.Add_stuffAdjective_and_mark_it_text.replace('~LABEL~', label)
                else:
                    orig_text = a.text
                    a.text = S.Add_stuffAdjective_and_mark_it_text.replace('~LABEL~', orig_text)


def add_title_short(Def: _Element):
    """
    Добавляет недостающие элементы в <Def> и <backstory>,
    используя текст из существующих элементов.
    """
    def get_text_from_element(element: Optional[_Element]) -> Optional[str]:
        """Безопасно получает текст из элемента."""
        return element.text if element is not None and element.text is not None else None

    def ensure_element_with_text(parent: _Element, tag: str, text: Optional[str]):
        """
        Находит дочерний элемент по тегу. Если его нет, создает его.
        Устанавливает текст элемента, если он был предоставлен.
        """
        if text is None:
            return
        if parent.find(tag) is None:
            new_element = ET.SubElement(parent, tag)
            new_element.text = text

    backstory = Def.find("backstory")
    if backstory is None:
        backstory = ET.SubElement(Def, 'backstory')

    title_text = get_text_from_element(Def.find('title'))
    title_short_text = get_text_from_element(Def.find('titleShort'))
    base_desc_text = get_text_from_element(Def.find("baseDesc")) or \
                     get_text_from_element(Def.find("baseDescription"))

    if title_short_text is None and title_text is not None:
        title_short_text = title_text[:12]
        ensure_element_with_text(Def, 'titleShort', title_short_text)

    title_female_text = None
    if S.add_titleFemale:
        ensure_element_with_text(Def, 'titleFemale', title_text)
        title_female_text = get_text_from_element(Def.find('titleFemale'))

    title_short_female_text = None
    if S.add_titleShortFemale:
        title_short_female_text = get_text_from_element(Def.find('titleShortFemale'))
        if title_short_female_text is None:
            source_text = title_short_text or title_text
            if source_text is not None:
                title_short_female_text = source_text[:12]
                ensure_element_with_text(Def, 'titleShortFemale', title_short_female_text)

    ensure_element_with_text(backstory, 'baseDesc', base_desc_text)
    ensure_element_with_text(backstory, 'title', title_text)
    ensure_element_with_text(backstory, 'titleShort', title_short_text)
    ensure_element_with_text(backstory, 'titleFemale', title_female_text)
    ensure_element_with_text(backstory, 'titleShortFemale', title_short_female_text)

def get_index_of_children(Def: _Element,l: _Element):
    children = list(Def)

    try:
        target_index = children.index(l)
    except ValueError:
        # Если целевой элемент не найден, добавляем новый элемент в конец
        target_index = -2
    return target_index



@error_handler(error_text="Error: add_title_short")
def BackstoryDef_add_title_short(Def: _Element):



    @error_handler(error_text="Error: add_titleFemale")
    def add_titleFemale():
        if S.add_titleFemale:
            titleFemale = Def.find('titleFemale')
            if titleFemale is None:
                title = Def.find('title')
                if title is not None:
                    titleFemale = etree.Element('titleFemale')
                    titleFemale.text = title.text
                    Def.insert(get_index_of_children(Def, title) + 1, titleFemale)

    add_titleFemale()


    @error_handler(error_text="Error: add_titleShortFemale")
    def add_titleShortFemale():
        if S.add_titleShortFemale:
            titleShortFemale = Def.find('titleShortFemale')
            if titleShortFemale is None:
                titleShort = Def.find("titleShort")
                if titleShort is not None:
                    titleShortFemale = etree.Element('titleShortFemale')
                    titleShortFemale.text = titleShort.text
                    Def.insert(get_index_of_children(Def, titleShort) + 1, titleShortFemale)


            else:
                title = Def.find('title')
                if title is not None:
                    titleShortFemale = etree.Element('titleShortFemale')
                    if len(title.text) < 13:
                        titleShortFemale.text = title.text
                    else:
                        titleShortFemale.text = title.text[:12]

                    Def.insert(get_index_of_children(Def, title) + 1, titleShortFemale)

    add_titleShortFemale()

@error_handler(error_text="Error: backstoryDef baseDesc")
def backstoryDef_baseDesc_to_description(Def):
    baseDesc = Def.find('baseDesc')
    if baseDesc is None:
        return

    description = Def.find('description')
    if description is not None:
        return

    description = etree.Element('description')
    description.text = baseDesc.text
    Def.insert(get_index_of_children(Def, baseDesc) + 1, description)




def TraitDef_add_strings(elem: _Element):
    if elem.find("degreeDatas") is not None:
        degreeDatas = elem.find('degreeDatas')
        for li in degreeDatas:
            if isinstance(li, _Comment):
                continue

            if li.find("labelFemale") is None:
                if li.find("label") is not None:
                    labelFemale = ET.SubElement(li, "labelFemale")
                    labelFemale.text = li.find("label").text


def Tkey_system_QuestScriptDef(elem: _Element):
    for element in elem.iter():
        if 'TKey' in element.attrib:
            TKey = ET.SubElement(elem, element.attrib['TKey'])
            element_1 = ET.SubElement(TKey, 'slateRef')
            element_1.text = element.text
            element.clear()


def replace_child_li(parent: _Element):
    def zamena_v_li_classe(li_class_name_: str):
        new_tag_ = ""

        for cls in S.Li_Class_Replace:
            start, end = cls.split("=", 1)
            # print(f"Checking {cls[0]} in {li_class_name}")
            if li_class_name_.startswith(start):
                new_tag_ = li_class_name_.replace(start, end)
                # print('new tag =', new_tag_)
                break
            elif li_class_name_.rpartition(".")[2].startswith(start):
                new_tag_ = li_class_name_.rpartition(".")[2].replace(start, end)
                # print('new tag =',new_tag_)
                break
            else:
                # print(f"{start} not in {li_class_name}")
                new_tag_ = "li"
        return new_tag_

    def li_new_tag_by_child(li_: _Element) -> str:
        for child_ in li_:
            if child_.tag == 'def' and child_.text is not None:
                return child_.text.replace(" ", "_")
            if child_.tag == 'compClass':
                if replace_compclass and child_.text is not None:
                    return child_.text.replace(" ", "_")
        return 'li'

    replace_compclass = True if parent.tag == 'comps' else False

    element2 = parent.findall('li')
    if element2:
        # print("Изначальный элемент без земененных <li>")
        # ET.dump(parent)
        for idx3, li in enumerate(element2):
            li: _Element
            new_tag = li_new_tag_by_child(li)

            if new_tag == "li":
                li_class_name = li.get('Class')
                if li_class_name is not None:
                    new_tag = zamena_v_li_classe(li_class_name)
                if new_tag == "li":
                    new_tag = str(idx3)
            new_tag = new_tag.replace(" ", "_").replace("-", "")

            try:
                li.tag = new_tag
            except ValueError:
                li.tag = 'LI_REPLACE_NUMBER' + new_tag
        # print("--Итоговый элемент с заменненными <li>--")
        # ET.dump(parent)


def replace_rulestring(parent: _Element):
    # ET.dump(parent)
    text = "\n"
    a_0 = "\t\t<li>"
    b = "</li>\n"
    for li in parent:
        if isinstance(li, _Comment):
            continue
        if li.tag == "li":
            text += a_0 + li.text + b
    text += S.tags_left_spacing_dict[S.tags_left_spacing]
    parent.clear()
    parent.text = text


def XmlExtensions_SettingsMenuDef(elem: _Element):
    settings = elem.find("settings")
    if settings is not None:
        for element in settings.iter():
            if element.tag == "li":
                tKey = ''
                tKey_text = ''
                tKeyTip = ''
                tKeyTip_text = ''
                tKey_tag_text_el: list[_Element] = []
                tKeyTip_tag_text_el: list[_Element] = []
                for el in element:
                    match el.tag:
                        case 'tKey':
                            tKey = el.text
                            tKey_tag_text_el.append(el)
                        case 'label':
                            tKey_text = el.text
                            tKey_tag_text_el.append(el)

                        case 'text':
                            tKey_text = el.text
                            tKey_tag_text_el.append(el)

                        case 'tKeyTip':
                            tKeyTip = el.text
                            tKeyTip_tag_text_el.append(el)

                        case 'tooltip':
                            tKeyTip_text = el.text
                            tKeyTip_tag_text_el.append(el)

                if tKey and tKey_text:
                    for els in tKey_tag_text_el:
                        els.clear()
                    ExitList.keyed.append((tKey, html.escape(tKey_text)))
                if tKeyTip and tKeyTip_text:
                    for els in tKeyTip_tag_text_el:
                        els.clear()
                    ExitList.keyed.append((tKeyTip, html.escape(tKeyTip_text)))


def ThingDef_MVCF_Comps_CompProperties_VerbProps(elem: _Element):
    comps = elem.find("comps")
    if comps is not None:


        for li in comps:
            if isinstance(li, _Comment):
                continue
            compClass = li.find("compClass")
            if compClass is not None:
                compClass = compClass.text
                if 'Comp_VerbProps' in compClass:
                    verbProps2 = li.find('verbProps')
                    if verbProps2 is not None:
                        verbProps = copy.deepcopy(verbProps2)

                        li.clear()
                        li.tag = 'Comp_VerbProps'
                        li.append(verbProps)


def find_defname(child_: _Element):
    # warning(f"Search Defname in {child.tag}")
    # ET.dump(child_)


    defName_elem = child_.find('defName')
    if defName_elem is None:
        defName_elem = child_.find('Defname')
    if defName_elem is None:
        defName_elem = child_.find('DefName')
    if defName_elem is None or defName_elem.text is None:
        return

    defname_tag = defName_elem.text.replace(" ", "_")
    return defname_tag


def QuestScript_def_(QuestScriptDef: _Element):

    def quest_node_sequence(sequence_elem: _Element):
        @dataclass
        class Elem_count:
            first_elem: _Element
            count: int
            is_modified = False

            def make_zero(self):
                if not self.is_modified:
                    self.first_elem.tag += '-0'
                    self.is_modified = True


        tagname_dict: {str, type(Elem_count)} = {}
        nodes = sequence_elem.find('nodes')
        if nodes is None:
            return
        for idx, li in enumerate(nodes):
            if isinstance(li, _Comment):
                continue
            if 'Class' not in li.attrib:
                try:
                    li.tag = str(idx)
                except ValueError:
                    li.tag = 'LI_REPLACE_NUMBER' + str(idx)

                continue
            class_name = li.attrib['Class']
            match class_name:
                case str(text) if '.' in text:
                    try:
                        li.tag = str(idx)
                    except ValueError:
                        li.tag = 'LI_REPLACE_NUMBER' + str(idx)

                    continue
                case 'QuestNode_SubScript':
                    try:
                        li.tag = str(idx)
                    except ValueError:
                        li.tag = 'LI_REPLACE_NUMBER' + str(idx)

                    continue

                case 'QuestNode_Signal':
                    inSignal = li.find('inSignal')
                    if inSignal is not None:
                        inSignaltext = inSignal.text
                        if inSignaltext is not None and inSignaltext and not inSignaltext.startswith('$'):
                            li.tag = inSignaltext.replace('.', '')
                            continue

                        else:
                            try:
                                li.tag = str(idx)
                            except ValueError:
                                li.tag = 'LI_REPLACE_NUMBER' + str(idx)

                            continue
                    else:
                        try:
                            li.tag = str(idx)
                        except ValueError:
                            li.tag = 'LI_REPLACE_NUMBER' + str(idx)

                        continue

                case 'QuestNode_Set':
                    name = li.find('name')
                    if name is not None:
                        name.clear()
                    value = li.find('value')
                    if value is not None:
                        value.clear()
                    try:
                        li.tag = str(idx)
                    except ValueError:
                        li.tag = 'LI_REPLACE_NUMBER' + str(idx)

                    continue

                case _:
                    ...


            tag_name = class_name.split('QuestNode_')[-1]
            if len(tag_name) < 2:
                try:
                    li.tag = str(idx)
                except ValueError:
                    li.tag = 'LI_REPLACE_NUMBER' + str(idx)

                continue
            if tagname_dict.get(tag_name, None) is not None:
                tagname_dict[tag_name].count += 1
                tagname_dict[tag_name].make_zero()
                li.tag = tag_name + '-' + str(tagname_dict[tag_name].count)

            else:
                tagname_dict[tag_name] = Elem_count(li, 0)

                try:
                    li.tag = tag_name
                except ValueError:
                    li.tag = 'LI_REPLACE_NUMBER' + tag_name



    @error_handler(error_text='QuestScriptDef label/text/customLetterLabel/customLetterText error')
    def makeSlateRef(el: _Element):
        textList = [el.find('label'), el.find('text'), el.find('customLetterLabel'), el.find('customLetterText')]

        for l in textList:

            if l is not None:

                value_elem = etree.Element(l.tag + '.value.slateRef')
                value_elem.text = copy.copy(l.text)
                children = list(el)
                try:
                    target_index = children.index(l)
                except ValueError:
                    # Если целевой элемент не найден, добавляем новый элемент в конец
                    target_index = -2

                el.insert(target_index + 1, value_elem)


                # value_elem = ET.SubElement(el, l.tag + '.value.slateRef')
                # value_elem.text = copy.copy(l.text)

                l.tag = l.tag + '.slateRef'



    # ET.dump(QuestScriptDef)
    for elem in QuestScriptDef.iter():
        if elem.get("Class") == "QuestNode_Sequence":
            quest_node_sequence(elem)
        makeSlateRef(elem)


    # ET.dump(QuestScriptDef)


def CombatExtended_AmmoDef(ThingDef: _Element):
    ...
    #
    # if ThingDef.get('Class') == 'CombatExtended.AmmoDef':
    #     ThingDef.tag = AmmoDef


def compProperties_ALL_Reloadable(elem: _Element):
    cs = elem.find('comps')
    if cs is not None:
        for li in cs:
            if isinstance(li, _Comment):
                continue
            li_class = li.get('Class', '')

            if li_class.startswith('CompProperties_') and li_class.endswith('Reloadable'):

                li.tag = li_class.replace('CompProperties_','Comp',1)
                cooldownGerund = li.find('cooldownGerund')
                if cooldownGerund is None:
                    cooldownGerund = ET.SubElement(li, 'cooldownGerund')
                    if S.Translate_tools_into_russian:
                        cooldownGerund.text = 'на перезарядке'
                    else:
                        cooldownGerund.text = 'on reload'

                chargeNoun = li.find('chargeNoun')
                if chargeNoun is None:
                    chargeNoun = ET.SubElement(li, 'chargeNoun')
                    if S.Translate_tools_into_russian:
                        chargeNoun.text = 'заряд'
                    else:
                        chargeNoun.text = 'charge'


def vEF_Abilities_AbilityDef(elem: _Element):
    try:
        jobReportString = elem.find('jobReportString')
        if jobReportString is None:
            jobReportString = ET.SubElement(elem, 'jobReportString')
            if S.Translate_tools_into_russian:
                jobReportString.text = 'Использование способности: {0}'
            else:
                jobReportString.text = 'Using ability: {0}'
    except Exception as ex:
        print(ex)
    try:

        text_el = elem.find('label')
        if text_el is None:
            return
        text = text_el.text
        verbProperties = elem.find('verbProperties')
        if verbProperties is None:
            verbProperties = ET.SubElement(elem, 'verbProperties')
            label = ET.SubElement(verbProperties, 'label')
            label.text = text
        else:
            label = verbProperties.find('label')
            if label is None:
                label = ET.SubElement(verbProperties, 'label')
                label.text = text
    except Exception as ex:
        print(ex)


def FactionDef_def(elem: _Element):
    try:
        pawnSingular = elem.find('pawnSingular')
        leaderTitle = elem.find('leaderTitle')

        if pawnSingular is None:
            pawnSingular = ET.SubElement(elem, 'pawnSingular')
            if S.Translate_tools_into_russian:
                pawnSingular.text = 'участник'
            else:
                pawnSingular.text = 'member'
        if leaderTitle is None:
            leaderTitle = ET.SubElement(elem, 'leaderTitle')
            if S.Translate_tools_into_russian:
                leaderTitle.text = 'лидер'
            else:
                leaderTitle.text = 'leader'




    except Exception as ex:
        print(ex)
    pass




def elem_tag_check(elem):
    if elem.tag == "AlienRace.ThingDef_AlienRace":
        elem.tag = elem.tag.replace('AlienRace.ThingDef_AlienRace', 'ThingDef')
    elem_tag = elem.tag
    if elem_tag == "RulePackDef":
        RulePackDef_def(elem)
    if elem_tag == "FactionDef":
        FactionDef_def(elem)
    if elem_tag == "VEF.Abilities.AbilityDef":
        vEF_Abilities_AbilityDef(elem)
    if elem_tag == "BodyDef":
        BodyDef_rename_li(elem)
    if elem_tag == "PawnKindDef":
        pawnKind_add_strings(elem)  # Если PawnKindDef, то добавить необходимые labelPlural
    if elem_tag == "ScenarioDef":
        ScenarioDef_add_strings(elem)  # Если ScenarioDef, то добавить ['name', 'description'] в scenario
    if elem_tag == "DamageDef":
        DamageDef_add_strings(elem)
    if elem_tag == "ThingDef":
        CombatExtended_AmmoDef(elem)
        # comps_Li_Class_Replace(elem) # Moved to replace_child_li -> li_new_tag_by_child
        add_missing_verbs_if_verbClass(elem)
        ThingDef_add_strings(elem)
        translate_ThingDef_tools(elem)

        compProperties_ALL_Reloadable(elem)


        comps = elem.find('comps')

        if S.Translate_tools_into_russian:
            if comps is not None:
                for ee in comps:
                    translate_ThingDef_tools(ee)
        ThingDef_MVCF_Comps_CompProperties_VerbProps(elem)

    if elem_tag == "AlienRace.BackstoryDef" or elem_tag == "AlienRace.AlienBackstoryDef":
        add_title_short(elem)
    if elem_tag == "BackstoryDef":
        BackstoryDef_add_title_short(elem)
        backstoryDef_baseDesc_to_description(elem)
    if elem_tag == "TraitDef":
        TraitDef_add_strings(elem)
    if elem_tag == "QuestScriptDef":
        QuestScript_def_(elem)
        if S.Tkey_system_on:
            print("TKEY_ON!!!!!!!!!!!!!!!!!!!!!!!")
            Tkey_system_QuestScriptDef(elem)
    if elem_tag == "XmlExtensions.SettingsMenuDef":
        XmlExtensions_SettingsMenuDef(elem)

def adding_in_string(folder: str, defname: str, path_list: list[str], elem: _Element, print_now: bool = False):


    def debug_print():
        print('folder:', folder, '| defname:', defname)
        print('tag:', elem.tag, '| text:', elem.text)

    if debug_print_bool:
        debug_print()

    elemtag = elem.tag.lower()

    if not path_list:
        print('elem_path Пустой -> defname не найден')

        print('folder', folder)
        print('elem_path_', path_list)
        print('tag', elem.tag)
        print('text1', elem.text)
        return None

    def return_none():



        if defname is None:
            return None

        if match(r"\d", defname):
            print('Skip: Defname start with digit - that cause XML error', defname)

            Error_log.append(f"Defname start with digit - that cause XML error: {folder, defname, path_list}")
            return None


        for tes in tag_endwith_skip:
            if finished_path.endswith(tes):

                print('Skip: endwith path - "', tes, '" in ', tag_endwith_skip)
                return None

        for tss in text_startwith_skip:
            if match(tss, text1):
                print('Skip: startwith path - "', tss, '" in', text_startwith_skip)

                return None

        if elem.text in S.Forbidden_text:
            print('Skip: Forbidden text - "', elem.text, '" in', S.Forbidden_text)

            return None

        return 1


    # print('folder', folder)
    # print('defname', defname)
    # print('elem_path_', elem_path_)
    # print('tag', child_.tag)
    # print('text1', child_.text)


    text1: str = elem.text
    text1 = html.escape(text1, quote=False)
    text1 = text1.replace("li&gt;", "li>")
    text1 = text1.replace("&lt;li", "<li")
    text1 = text1.replace("&lt;/li", "</li")
    text1 = text1.replace("-&gt;", "->")
    text1 = text1.replace(' -- ', ' - ')
    # try:
    finished_path = ".".join(path_list)

    if 'LI_REPLACE_NUMBER' in finished_path:
        # print(finished_path)
        finished_path = finished_path.replace('LI_REPLACE_NUMBER', '')
        # print(finished_path)

    rr = return_none()
    if rr is None:
        return None

    if print_now:
        if text1.isspace():
            return None
        ExitList.fdpt.append(FolderDefnamePathText(folder, defname, finished_path, text1))
        return None

    if elemtag in S.no_text_check_label_list:
        ExitList.fdpt.append(FolderDefnamePathText(folder, defname, finished_path, text1))
        return None

    # print(S.Forbidden_part_of_tag)
    # print(elem.tag)
    for fp in S.Forbidden_part_of_tag:
        if fp in elemtag:

            return None


    if "_" in text1:
        if " " not in text1:
            if elemtag in S.Tags_to_extraction:
                ExitList.fdpt.append(FolderDefnamePathText(folder, defname, finished_path, text1))

            print('Skip: Has "_ underscore" and no spaces "', text1)
            return None




    ExitList.fdpt.append(FolderDefnamePathText(folder, defname, finished_path, text1))



def dollar_variable_replace(elem: _Element):

    root = elem

    # Шаг 1: Поиск всех переменных в текстах элементов
    variables_map = {}
    pattern = re.compile(r'\$(\w+)')

    # Рекурсивная функция для поиска элементов с переменными
    def find_variables(elem):
        # Обрабатываем только текст элементов (не атрибуты и не tail)
        if elem.text and '$' in elem.text:
            # Находим все переменные в тексте
            matches = pattern.findall(elem.text)
            if matches:
                for var_name in matches:
                    if var_name not in variables_map:
                        variables_map[var_name] = []
                    # Сохраняем ссылку на элемент и оригинальный текст
                    variables_map[var_name].append((elem, elem.text))

        # Рекурсивно обрабатываем дочерние элементы
        for child in elem:
            find_variables(child)

    # Первоначальный проход для сбора всех переменных
    find_variables(root)

    # Шаг 2: Поиск значений переменных в QuestNode_Set
    variable_values = {}

    # Ищем все элементы QuestNode_Set
    for node_set in root.findall(".//li[@Class='QuestNode_Set']"):
        name_elem = node_set.find('name')
        if name_elem is None or name_elem.text is None:
            continue

        var_name = name_elem.text.strip()

        # Если эта переменная используется в текстах
        if var_name in variables_map:
            value_elem = node_set.find('value')
            value = value_elem.text.strip() if value_elem is not None and value_elem.text is not None else ""
            variable_values[var_name] = value

    # Шаг 3: Замена переменных в элементах
    for var_name, elements in variables_map.items():
        if var_name not in variable_values:
            continue  # Пропускаем если нет значения

        value = variable_values[var_name]

        for (elem, original_text) in elements:
            # Заменяем все вхождения этой переменной
            new_text = original_text.replace(f'${var_name}', value)

            # Если текст изменился - обновляем элемент
            if new_text != elem.text:
                elem.text = new_text
                if debug_print_bool:
                    print("Replacing variable:", var_name, 'by', value)


def first_launch(root_Def: _Element):
    path_list1 = []

    def has_child(folder, defname, path_list, elem):


        if elem.tag.lower() in S.Tags_before_li:
            replace_rulestring(elem)
            adding_in_string(folder=folder, defname=defname, path_list=path_list, elem=elem, print_now=True)
        else:
            replace_child_li(elem)

        requrs(folder=folder, defname=defname, path_list=path_list.copy(), elem=elem)


    def no_child(folder, defname, path_list, elem):
        """Output elem"""

        if isinstance(elem, etree._Comment):
            return

        if elem.tag.lower() in S.Forbidden_tag:
            return
        if S.Check_at_least_one_letter_in_text and not any(c.isalpha() for c in elem.text):  # Проверка хоть одной буквы
            return

        if elem.tag.lower() in S.Tags_to_extraction:  # Проверка на соответствие Tags_to_extraction
            adding_in_string(folder=folder, defname=defname, path_list=path_list, elem=elem)
        elif any(part_of_tag in elem.tag.lower() for part_of_tag in S.Part_of_tag_to_extraction):  # Проверка на не полный тэг
            adding_in_string(folder=folder, defname=defname, path_list=path_list, elem=elem)
        elif " " in elem.text:
            adding_in_string(folder=folder, defname=defname, path_list=path_list, elem=elem)

    def requrs(folder, defname, path_list, elem):

        dollar_variable_replace(elem)
        elem_tag_check(elem)

        children = list(elem)  # Важно: создать копию перед итерацией

        for elem1 in children:
            new_path = path_list.copy()
            if elem1.tag != folder:
                new_path.append(elem1.tag)

            if not list(elem1) and (elem1.text is not None):
                no_child(folder, defname, new_path, elem1)
            else:
                has_child(folder, defname, new_path, elem1)

    for defFold_elem in root_Def:
        if isinstance(defFold_elem, etree._Comment):
            continue

        if defFold_elem.get('Abstract', 'false').lower() == 'true':
            continue

        folder1 = defFold_elem.tag
        defname1 = find_defname(defFold_elem)
        if defname1 is None:
            continue

        initial_path = path_list1.copy()
        if defFold_elem.tag != folder1:
            initial_path.append(defFold_elem.tag)

        requrs(folder1, defname1, initial_path, defFold_elem)






def finish_string(tree2):

    ExitList.fdpt = []
    ExitList.keyed = []
    root_finish_string = tree2.getroot()
    first_launch(root_finish_string)
    return ExitList.fdpt, ExitList.keyed


