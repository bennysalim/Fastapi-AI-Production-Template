from enum import Enum


class TicketTypeEnum(str, Enum):
    complain="COMPLAIN"
    request="REQUEST"
    report="REPORT"
