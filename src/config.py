import re
from dataclasses import dataclass

@dataclass
class Config:
    datetime_format: str = "%Y-%m-%dT%H:%M:%S%Z"
    timeZone: str = "IST"
    imageRegex = re.compile(r'\[!\[[^\]]+\]\([^\)]+\)\]\((http://journal.dcbeatty.com/wp-content/uploads/\d{4}/\d{2}/([\w\-]+\.\w{2,4}))\)')