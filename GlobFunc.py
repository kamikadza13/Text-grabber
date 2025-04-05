from lxml import etree

def xml_get_text(element: etree.Element, child_name: str, default=""):
    """Возвращает текст дочернего элемента"""
    ''', если он существует и его текст не None.
    Иначе возвращает default.

    :param element: Родительский элемент, в котором ищем дочерний элемент.
    :param child_name: Имя дочернего элемента.
    :param default: Значение по умолчанию, если элемент не найден или его текст None.
    :return: Текст элемента или default.
    '''
    child = element.find(child_name)
    return child.text if child is not None and child.text is not None else default


