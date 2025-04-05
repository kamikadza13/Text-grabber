import re

from lxml import etree


def add_patch_value(root: etree.Element, values:etree.Element):
    for value in values:
        root.append(value)

def ensure_xpath(root, xpath, value_to_add):
    current = [root]
    parts: list[str] = [p for p in xpath.strip("/").split("/") if p]

    for part in parts:
        new_current = []
        for node in current:
            # Парсим часть пути (например, "ThingDef[defName='...']")
            if "[" in part:
                tag, predicate = part.split("[", 1)
                predicate = predicate.rstrip("]").strip()
            else:
                tag = part
                predicate = None

            # Обработка текстовых узлов (например, text())
            is_text_node = False
            if tag == "text()":
                is_text_node = True
                tag = None  # Текстовый узел не имеет тега

            # Обработка предикатов
            elements = []
            if predicate:
                # Разбиваем условия через "or"
                conditions = re.split(r'\s+or\s+', predicate, flags=re.IGNORECASE)
                for condition in conditions:
                    # Обрабатываем разные типы условий
                    if condition.startswith("@"):
                        # Атрибут: @defName='VWE_Gun_Musket'
                        attr_match = re.match(r'@([a-zA-Z_]+)\s*=\s*["\'](.*?)["\']', condition)
                        if not attr_match:
                            raise ValueError(f"Invalid condition: {condition}")
                        attr_name, attr_value = attr_match.groups()
                        found = node.find(f".//{tag}[@{attr_name}='{attr_value}']")
                        if found is None:
                            elem = etree.SubElement(node, tag, **{attr_name: attr_value})
                            elements.append(elem)
                        else:
                            elements.append(found)
                    elif "text()" in condition:
                        # Текстовое значение: text()='NeolithicRangedChief'
                        text_match = re.match(r'text\(\)\s*=\s*["\'](.*?)["\']', condition)
                        if not text_match:
                            raise ValueError(f"Invalid text condition: {condition}")
                        text_value = text_match.group(1)
                        # Ищем элемент с нужным текстом
                        for child in node.findall(tag):
                            if child.text == text_value:
                                elements.append(child)
                                break
                        else:
                            elem = etree.SubElement(node, tag)
                            elem.text = text_value
                            elements.append(elem)
                    else:
                        # Дочерний элемент: defName='VWE_Gun_Musket'
                        elem_match = re.match(r'([a-zA-Z_]+)\s*=\s*["\'](.*?)["\']', condition)
                        if not elem_match:
                            raise ValueError(f"Invalid element condition: {condition}")
                        elem_name, elem_value = elem_match.groups()
                        # Ищем элемент с дочерним элементом <elem_name>
                        for child in node.findall(tag):
                            defname_elem = child.find(elem_name)
                            if defname_elem is not None and defname_elem.text == elem_value:
                                elements.append(child)
                                break
                        else:
                            elem = etree.SubElement(node, tag)
                            defname_elem = etree.SubElement(elem, elem_name)
                            defname_elem.text = elem_value
                            elements.append(elem)
            else:
                # Без предикатов
                if tag:
                    elem = node.find(tag)
                    if elem is None:
                        elem = etree.SubElement(node, tag)
                    elements.append(elem)
                else:
                    elements.append(node)  # Для текстовых узлов

            # Обработка текстовых узлов
            if is_text_node and not part.startswith("text()"):
                for elem in elements:
                    if elem.text is None:
                        elem.text = ""
                    new_current.append(elem)  # Возвращаем сам элемент, а не текстовый узел
            else:
                new_current.extend(elements)

        current = new_current


    for a in current:

        add_patch_value(a, value_to_add)


    return current
# Пример использования:
root = etree.Element("Defs")
xpath = 'ThingDef[defName="lala" or defName="bebe"]/modExtensions/li[@Class="GeneExtension"]'
xpath = 'Defs/BodyDef[defName="AG_ScorpionLike" or defName="AG_ScorpionLike2" or]/corePart/parts/li[def="AG_InsectTail"]/parts/li[def="AG_InsectSting"]/groups'
# xpath = '/Defs/ThingDef[defName="VWE_Gun_Musket" or defName="VWE_Gun_Flintlock"]/weaponTags/li[text()="NeolithicRangedChief"]'

values = etree.fromstring("""					<value>
						<li>RG_RawRaspberries</li>
					</value>""")

# Создаем структуру
ensure_xpath(root, xpath, values)

# Печатаем результат
print(etree.tostring(root, pretty_print=True).decode())