from graph import travel_app
from datetime import datetime
import config

def main(city, start_date, end_date):
    """Main function demonstrating smart hotel search"""
    
    # Initial state for the graph
    inputs = {
        "location": city,
        "start_date": start_date,
        "end_date": end_date,
        "loop_count": 0
    }

    # Run the travel planning workflow
    print(f"Initiating travel planning for {city} from {start_date} to {end_date}")
    result = travel_app.invoke(inputs)

    # You can now access the final state or specific outputs
    if result.get("summary"):
        print("\n--- Travel Plan Summary ---")
        print(result["summary"])
        return result["summary"]
    else:
        print("\n--- Travel Plan Failed or Incomplete ---")
        print("Final state:", result)

if __name__ == "__main__":
    # Example usage:
    # Make sure to set your API keys in a .env file as described in config.py
    # Example .env content:
    # AMADEUS_CLIENT_ID="YOUR_AMADEUS_CLIENT_ID"
    # AMADEUS_CLIENT_SECRET="YOUR_AMADEUS_CLIENT_SECRET"
    # OPENAI_API="YOUR_OPENAI_API_KEY"
    # TAVILY_API_KEY="YOUR_TAVILY_API_KEY"

    # Define your desired trip details
    city = "Chennai"
    start_date = "2025-07-20"  # Example future date
    end_date = "2025-07-23"    # Example future date

    main(city, start_date, end_date)