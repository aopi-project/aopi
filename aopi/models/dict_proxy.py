from typing import Any, Dict, Optional


class DictProxy:
    def __init__(self, values: Optional[Dict[str, Any]]) -> None:
        self.__init_dict = values
        if values is None:
            return
        obj_dict = dict()
        for key, value in values.items():
            if isinstance(value, Dict):
                value = DictProxy(value)
            obj_dict[key] = value
        self.__obj_dict = obj_dict

    def is_none(self) -> bool:
        return self.__init_dict is None

    def __getattr__(self, item: str) -> Any:
        return self.__obj_dict.get(item)

    def __repr__(self) -> str:
        body = None
        if self.__init_dict:
            body = ",".join([f"{key}:{val}" for key, val in self.__init_dict.items()])
        return f"<Dict proxy {body}>"

    def __str__(self) -> str:
        return self.__repr__()
