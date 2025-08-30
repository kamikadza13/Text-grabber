from functools import wraps

from lxml import etree
from printy import escape as printy_escape
from printy import printy

from GlobVars import state


def escape_printy_string(string) -> str:
    return printy_escape(str(string))


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

def error_handler(*exceptions, default=None, error_text:str = None, add_in_log:bool = True):
    """
    @error_handler(ValueError, KeyError, default=0)
    """
    exceptions = exceptions if exceptions else (Exception,)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                if error_text:
                    printy(f"\t\t{escape_printy_string(error_text)}", predefined='r')
                else:
                    print(f"Error: {e}")
                if add_in_log:
                    state.error_log.append(e)
                return default
        return wrapper
    return decorator

