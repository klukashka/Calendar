from typing import Any, Type, Callable


def singleton(class_: Type) -> Callable[..., Any]:
    """
    Singleton decorator allows to have only one instance of a class.
    Otherwise, ValueError is raised.
    """
    instances: dict[Type: any] = {}

    def get_instance(*args, **kwargs) -> Any:
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
            return instances[class_]
        raise ValueError(f"Instance of class {class_} already exists")

    return get_instance
