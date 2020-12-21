import inspect
from typing import Any, Dict, Type

from fastapi import File, Form
from pydantic import BaseModel
from pydantic.fields import ModelField


def as_form(cls: Type[BaseModel]) -> Type[BaseModel]:
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        def_val = None
        if model_field.required:
            def_val = model_field.default or ...

        form_default = Form(def_val, alias=model_field.alias)
        if model_field.default.__class__ is File:
            form_default = model_field.default

        new_parameters.append(
            inspect.Parameter(
                model_field.name,
                inspect.Parameter.POSITIONAL_ONLY,
                default=form_default,
                annotation=model_field.outer_type_,
            )
        )

    async def as_form_func(**data: Dict[str, Any]) -> BaseModel:
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, "as_form", as_form_func)
    return cls
