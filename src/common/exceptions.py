from types import ModuleType

from django.core.exceptions import ValidationError


class PrivateChatAlreadyExistsError(ValidationError):
    def __init__(self, message) -> None:
        super().__init__(message=message)


class ModuleObjectNotFoundException(Exception):
    """Класс исключения для случаев когда в модуле(python файле) нету искомого объекта"""

    def __init__(self, module: ModuleType, obj_name: str) -> None:
        message = f"Module {module} has not attribute(object) {obj_name}"
        super().__init__(message)


class ModuleNotFound(Exception):
    """Класс исключения для случаев когда нету возможности найти модуль"""

    def __init__(self, module_path: str) -> None:
        message = f"Module {module_path} not found or not valid python file"
        super().__init__(message)


class InvalidModuleObjectStringPatternException(Exception):
    """Класс исключения для случаев когда переданная строка имеет неправильный формат т.е отличный от <модуль:объект>"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
