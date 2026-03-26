from pyparsing import Literal
from app.schemas.ticket_trans_schema import TicketAgenticChatSch
from langgraph.graph import StateGraph
from langgraph.graph import START, END

def inference_ticket_intent(state:TicketAgenticChatSch):
    return state

def route_after_intent(state: TicketAgenticChatSch) -> str:
    return state.ticket_agent_inference.name

def validate_field(state:TicketAgenticChatSch)->bool:
    return state.is_schema_valid

def ticket_creation(state:TicketAgenticChatSch):
    return state

def ticket_field_validator(state:TicketAgenticChatSch):
    return state

def retrieve_ticket(state:TicketAgenticChatSch):
    return state

def final_node(state:TicketAgenticChatSch):
    return state

ticket_graph_builder = StateGraph(TicketAgenticChatSch)
# graph
ticket_graph_builder.add_node("inference_ticket_intent", inference_ticket_intent)
ticket_graph_builder.add_node("ticket_field_validator", ticket_field_validator)
ticket_graph_builder.add_node("retrieve_ticket", retrieve_ticket)
ticket_graph_builder.add_node("ticket_creation", ticket_creation)
ticket_graph_builder.add_node("final_node", final_node)

#add start & end
ticket_graph_builder.add_edge(START, "inference_ticket_intent")
ticket_graph_builder.set_entry_point("inference_ticket_intent")

# add edges logic
ticket_graph_builder.add_conditional_edges(
   'inference_ticket_intent',
    route_after_intent,
    path_map={
        "ticket_creation": "ticket_field_validator",
        "retrieve_ticket": "retrieve_ticket",
        "qna":"final_node",
        "irrelevant":"final_node"
    }
)

ticket_graph_builder.add_conditional_edges(
    'ticket_field_validator',
    validate_field,
    path_map={
        True:"ticket_creation",
        False:"final_node"
    }
)

ticket_graph_builder.add_edge("ticket_creation", "final_node")
ticket_graph_builder.add_edge("retrieve_ticket", "final_node")

# finish point
ticket_graph_builder.add_edge("final_node", END)
ticket_graph_builder.set_finish_point("final_node")

ticket_trans_workflow=ticket_graph_builder.compile()
