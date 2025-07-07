from enum import Enum


class AgentInferenceEnum(str, Enum):
    ticket_creation="TICKET_CREATION",
    retrieve_ticket="RETRIEVE_TICKET",
    close_ticket="CLOSE_TICKET",
    irrelevant="IRRELEVANT"