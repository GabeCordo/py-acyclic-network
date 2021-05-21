from typing import Any, Generic
from src.venezia.types import static, dynamic

Result = tuple(dynamic.Any, Exception)
Queue = list[static.Request]
LinkerPath = str

