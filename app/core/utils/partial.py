from copy import deepcopy
from dataclasses import asdict
from typing import Any, Callable, Optional, Type, TypeVar, ClassVar

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

Model = TypeVar("Model", bound=Type[BaseModel])


def partial_model(
    without_fields: Optional[list[str]] = None,
) -> Callable[[Model], Model]:
    """A decorator that create a partial model.

    Args:
        model (Type[BaseModel]): BaseModel model.

    Returns:
        Type[BaseModel]: ModelBase partial model.
    """
    if without_fields is None:
        without_fields = []

    def wrapper(model: Type[Model]) -> Type[Model]:
        def make_field_optional(
            field: FieldInfo, default: Any = None, omit: bool = False
        ) -> tuple[Any, FieldInfo]:
            new = deepcopy(field)
            new.default = default
            new.annotation = Optional[field.annotation]
            # Wrap annotation in ClassVar if field in without_fields
            return ClassVar[new.annotation] if omit else new.annotation, new

        model_copy = deepcopy(model)

        # Pydantic will error if validators are present without the field
        # so we set check_fields to false on all validators
        for dec_group_label, decs in asdict(model_copy.__pydantic_decorators__).items():
            for validator in decs.keys():
                decorator_info = getattr(
                    getattr(model.__pydantic_decorators__, dec_group_label)[validator],
                    "info",
                )
                if hasattr(decorator_info, "check_fields"):
                    setattr(
                        decorator_info,
                        "check_fields",
                        False,
                    )

        return create_model(
            model.__name__,
            __base__=model,
            __module__=model.__module__,
            **{
                field_name: make_field_optional(
                    field_info, omit=(field_name in without_fields)
                )
                for field_name, field_info in model.model_fields.items()
            },
        )

    return wrapper
