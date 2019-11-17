"""mywsgi - type hints module."""
from typing import ByteString, Callable, Dict, List, Tuple

BodyType = List[ByteString]
EnvType = Dict
HeadersType = List[Tuple[str, str]]
StartRespType = Callable[[str, HeadersType], BodyType]
