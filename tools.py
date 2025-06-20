import os
import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict, TypedDict
import pandas as pd
import config

from langchain.chat_models import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

from hotel_search import SmartHotelSearch, parse_hotel_offers # Import from your modularized files
import config # Import API keys from config

# Initialize APIs using keys from config
llm = ChatOpenAI(openai_api_key=config.OPENAI_API_KEY, temperature=0.7)
tavily = TavilySearchResults(api_key=config.TAVILY_API_KEY)


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

@tool
def check_weather_tool(location: str, start_date: str, end_date: str, loop_count: Optional[int] = 0) -> dict:
    """
    Check the weather for a given location and date range.
    If rainy and not already suggested an alternate, trigger alternate date flow.
    """
    print(f"🔎 Running: check_weather_tool | loop_count: {loop_count}")
    if loop_count >= 1:
        print("☀️ Skipping recheck. Proceeding.")
        return {"weather_status": "build_itinerary"}

    query = f"Weather in {location} from {start_date} to {end_date}"
    results = tavily.invoke({"query": query})
    content = " ".join([r.get("content", "").lower() for r in results])
    if any(word in content for word in ["rain", "drizzle", "shower", "thunderstorm", "precipitation", "wet"]):
        print("🌧️ Rain detected.")
        return {"weather_status": "suggest_alternate"}
    print("☀️ Weather is clear.")
    return {"weather_status": "build_itinerary"}


@tool
def suggest_alternate_tool(start_date: str, loop_count: Optional[int] = 0) -> dict:
    """Suggests an alternate start date if weather conditions are not favorable or if looping threshold is met."""

    print("🔁 Running: suggest_alternate_tool")
    original_start = datetime.strptime(start_date, "%Y-%m-%d")
    new_start = (original_start + timedelta(days=3)).strftime("%Y-%m-%d")
    new_end = (original_start + timedelta(days=6)).strftime("%Y-%m-%d")
    print(f"📆 New Dates: {new_start} - {new_end}")
    return {"start_date": new_start, "end_date": new_end, "loop_count": loop_count + 1}

@tool
def build_itinerary_tool(location: str, start_date: str, end_date: str) -> dict:
    """Builds a day-by-day itinerary for the given location and travel start date."""

    print("📝 Running: build_itinerary_tool")
    prompt = f"Create an itinerary for {location} from {start_date} to {end_date}. 3 activities/day: morning, afternoon, evening."
    itinerary = llm.predict(prompt)
    print("✅ Itinerary ready.")
    return {"itinerary": itinerary}

@tool
def calculate_fees_tool(location: str, itinerary: str) -> dict:
    """Calculates the total entrance or activity fees based on the provided itinerary."""

    print("💰 Running: calculate_fees_tool")

    def get_fee(activity):
        query = f"USD entrance ticket cost for {activity} in {location}"
        try:
            result = tavily.invoke({"query": query})
            content = " ".join([r.get("content", "").lower() for r in result])
            if "free" in content:
                return 0.0
            match = re.search(r"\\$?(\\d+(?:\\.\\d{1,2})?)", content)
            return float(match.group(1)) if match else 0.0
        except:
            return 0.0

    activity_lines = [line for line in itinerary.split("\\n") if "|" in line]
    activity_names = [line.split("|")[2].strip() for line in activity_lines]
    fees = [get_fee(a) for a in activity_names]
    print(f"🎟️ Fetched fees for {len(fees)} activities.")
    return {"entrance_fees": fees}

@tool
def fetch_hotel_tool(city_code: str, start_date: str, end_date: str) -> dict:
    """
    Fetch hotel offers in a given city using Amadeus SDK. Returns the first hotel's total cost.
    """
    print("🏨 Running: fetch_hotel_tool")
    
    hotel_search = SmartHotelSearch(config.AMADEUS_API_KEY, config.AMADEUS_API_SECRET, config.OPENAI_API_KEY)

    checkin_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    checkout_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    checkin = checkin_date_obj.strftime('%Y-%m-%d')
    checkout = checkout_date_obj.strftime('%Y-%m-%d')
    adults = 2
    rooms = 1

    print(f"🎯 Smart Hotel Search")
    print(f"📍 City: {city_code}")
    print(f"📅 Dates: {checkin} to {checkout}")
    print(f"👥 Guests: {adults} adults, {rooms} room(s)")
    print("=" * 50)

    hotel_data = hotel_search.Google_Hotels_by_city_name(
        city_code, checkin, checkout, adults, rooms, max_results=10
    )

    if hotel_data:
        hotels = parse_hotel_offers(hotel_data)

        if hotels:
            print(f"🎉 Found {len(hotels)} hotel offers!")
            df = pd.DataFrame(hotels)
            df_sorted = df.sort_values('price_total').head(10)

            print("\\n🏆 Top Hotels (sorted by price):")
            print("-" * 60)

            for idx, hotel in df_sorted.iterrows():
                print(f"\\n🏨 {hotel['hotel_name']}")
                print(f"   📍 {hotel['address']}, {hotel['city']}")
                print(f"   ⭐ Rating: {hotel['rating']}")
                print(f"   🛏️  Room: {hotel['room_description']}")
                print(f"   💵 Total: {hotel['currency']} {hotel['price_total']:.2f}")
                print(f"   💰 Base: {hotel['currency']} {hotel['price_base']:.2f}")

            print(f"\\n💾 Results saved to 'smart_hotel_search_results.csv'")
            return {"hotel_info": {"Hotel Name": hotel['hotel_name'], "Total Cost": hotel['price_total']}}

        else:
            print("❌ No hotel offers found")
            return {"hotel_info": {"Hotel Name": "Fallback Hotel", "Total Cost": 200.0}}
    else:
        print("❌ Failed to retrieve hotel data")
        return {"hotel_info": {"Hotel Name": "Fallback Hotel", "Total Cost": 200.0}}


@tool
def calculate_total_tool(entrance_fees: list, hotel_info: dict) -> dict:
    """Estimates the total trip cost by summing fees and hotel prices."""

    print("📊 Running: calculate_total_tool")
    total = sum(entrance_fees) + hotel_info.get("Total Cost", 0.0)
    return {"total_cost": round(total, 2)}

@tool
def final_summary_tool(location: str, start_date: str, end_date: str, itinerary: str, total_cost: float) -> dict:
    """Gives the final summary of the query from user"""
    print("📋 Running: final_summary_tool")
    summary = f"""
Trip Summary:
Destination: {location}
Dates: {start_date} to {end_date}
Total Cost: ${total_cost}
Itinerary:
{itinerary}
"""
    return {"summary": summary}