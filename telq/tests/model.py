from dataclasses import dataclass


@dataclass
class Test:
    sender: str
    text: str
    testIdTextType: str
    testIdTextCase: str
    testIdTextLength: int
    supplierId: int
    mcc: str
    mnc: str
    portedFromMnc: str
