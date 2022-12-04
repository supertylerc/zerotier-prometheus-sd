from pydantic import BaseModel


class PromSDItemSchema(BaseModel):
    targets: list[str]
    labels: dict[str, str]
