from pydantic import BaseModel


class Item(BaseModel):
  filepath: str
  dataset: str

  xmin: float
  xmax: float
  ymin: float
  ymax: float


class MeterDB(BaseModel):
  data: list[Item]
