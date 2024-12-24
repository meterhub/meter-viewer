from pydantic import BaseModel


class Point(BaseModel):
  x: float
  y: float


class MeterDataset(BaseModel):
  name: str
  img_path: str
  img_height: int
  img_width: int
  area: list[Point]  # top-left, bottom-right
  value: int
  is_carry: bool
