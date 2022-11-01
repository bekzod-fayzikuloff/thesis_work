import importlib
import os
from typing import Any

from django.conf import settings

from common.exceptions import InvalidModuleObjectStringPatternException, ModuleNotFound


def include_object(namespace: str) -> Any:
    """Интерпретация значение строки которое считаться как модуль
    и получения значение тех переменных которые были в том модуле"""
    if ":" not in namespace:
        module_path = "/".join(namespace.split("."))
        if os.path.isfile(os.path.join(settings.BASE_DIR, f"{module_path}.py")):
            _module__ = importlib.import_module(namespace)
            return _module__

    elif ":" in namespace:
        try:
            module_path, module_object = tuple(namespace.split(":"))
            module_file_path = "/".join(module_path.split("."))
            if os.path.isfile(os.path.join(settings.BASE_DIR, f"{module_file_path}.py")):
                _module__ = importlib.import_module(module_path)
                obj = getattr(_module__, module_object)
                return obj

        except ValueError:
            raise InvalidModuleObjectStringPatternException(
                f"Переданна строка шаблона {namespace} не является валидной"
                f" формат строки должен быть <модуль:объект>"
            )
        except AttributeError:
            raise ModuleObjectNotFoundException(_module__, module_object)  # noqa

    raise ModuleNotFound(namespace)
