from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
import config

from tools import (
    check_weather_tool,
    suggest_alternate_tool,
    build_itinerary_tool,
    calculate_fees_tool,
    fetch_hotel_tool,
    calculate_total_tool,
    final_summary_tool
)

class TravelState(TypedDict):
    location: str
    start_date: str
    end_date: str
    loop_count: Optional[int]
    weather_status: Optional[str]
    itinerary: Optional[str]
    entrance_fees: Optional[list]
    hotel_info: Optional[dict]
    total_cost: Optional[float]
    summary: Optional[str]

def router(state):
    return state["weather_status"]

# Graph nodes
workflow = StateGraph(TravelState)
workflow.add_node("check_weather", lambda s: check_weather_tool.invoke(s))
workflow.add_node("suggest_alternate", lambda s: suggest_alternate_tool.invoke(s))
workflow.add_node("build_itinerary", lambda s: build_itinerary_tool.invoke(s))
workflow.add_node("calculate_fees", lambda s: calculate_fees_tool.invoke(s))
workflow.add_node("fetch_hotel", lambda s: fetch_hotel_tool.invoke({
    "city_code": s["location"],
    "start_date": s["start_date"],
    "end_date": s["end_date"]
}))
workflow.add_node("calculate_total", lambda s: calculate_total_tool.invoke(s))
workflow.add_node("final_summary", lambda s: final_summary_tool.invoke(s))

# Edges
workflow.set_entry_point("check_weather")
workflow.add_conditional_edges("check_weather", router, {
    "suggest_alternate": "suggest_alternate",
    "build_itinerary": "build_itinerary"
})
workflow.add_edge("suggest_alternate", "check_weather")
workflow.add_edge("build_itinerary", "calculate_fees")
workflow.add_edge("calculate_fees", "fetch_hotel")
workflow.add_edge("fetch_hotel", "calculate_total")
workflow.add_edge("calculate_total", "final_summary")
workflow.add_edge("final_summary", END)

# Compile and run
travel_app = workflow.compile()