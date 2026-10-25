import logging
import sys
from dataclasses import dataclass, field
from logger_formatter import JSONFormatter

logger = logging.getLogger("TestCase")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(JSONFormatter())
file_handler = logging.FileHandler("test.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.addHandler(file_handler)
# DataClass
@dataclass
class TestCase:
    name: str
    steps: list[str] = field(default_factory=list)
    expected: str = ""

    def add_step(self, step: str):
        logger.debug(f"use method add_step()")
        logger.info(f"Add step: {step}, logger", extra={"user_id": 222})
        self.steps.append(step)


t = TestCase("login_flow")
t.add_step("open url")
t.add_step("enter credentials")
t.add_step("close url")
print(t.__repr__())

t2 = TestCase("login_flow")
print(t == t2)

t2.expected = "success"
print(t.expected)
