from dataclasses import dataclass
from datetime import datetime

@dataclass
class TrafficOffence:
  postal_code: str
  detection: str 
  datetime: datetime