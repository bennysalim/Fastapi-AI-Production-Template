from enum import Enum

class TicketInferenceEnum(str, Enum):
    ticket_creation="TICKET_CREATION",
    retrieve_ticket="RETRIEVE_TICKET",
    qna="QNA",
    irrelevant="IRRELEVANT",
