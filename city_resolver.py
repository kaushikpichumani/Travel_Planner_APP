import openai
import re
from typing import Optional, List, Dict
import config
class CityCodeResolver:
    """Use LLM to resolve city names to IATA codes"""

    def __init__(self, openai_api_key: str):
        self.client = openai.OpenAI(api_key=openai_api_key)

        # Common city codes cache to reduce API calls
        self.city_code_cache = {
            'new york': 'NYC', 'new york city': 'NYC', 'nyc': 'NYC',
            'london': 'LON', 'paris': 'PAR', 'tokyo': 'TYO',
            'los angeles': 'LAX', 'chicago': 'CHI', 'miami': 'MIA',
            'san francisco': 'SFO', 'las vegas': 'LAS', 'boston': 'BOS',
            'washington': 'WAS', 'seattle': 'SEA', 'denver': 'DEN',
            'orlando': 'ORL', 'atlanta': 'ATL', 'houston': 'HOU',
            'phoenix': 'PHX', 'dallas': 'DFW', 'detroit': 'DTT',
            'minneapolis': 'MSP', 'philadelphia': 'PHL',
            'rome': 'ROM', 'madrid': 'MAD', 'barcelona': 'BCN',
            'amsterdam': 'AMS', 'berlin': 'BER', 'vienna': 'VIE',
            'zurich': 'ZUR', 'munich': 'MUC', 'milan': 'MIL',
            'dubai': 'DXB', 'singapore': 'SIN', 'hong kong': 'HKG',
            'bangkok': 'BKK', 'mumbai': 'BOM', 'delhi': 'DEL',
            'sydney': 'SYD', 'melbourne': 'MEL', 'toronto': 'YTO',
            'vancouver': 'YVR', 'montreal': 'YMQ', 'rio de janeiro': 'RIO',
            'sao paulo': 'SAO', 'buenos aires': 'BUE', 'mexico city': 'MEX'
        }

    def get_city_code(self, city_name: str) -> Optional[str]:
        """Get IATA city code for a given city name"""
        city_lower = city_name.lower().strip()

        # Check cache first
        if city_lower in self.city_code_cache:
            return self.city_code_cache[city_lower]

        # Use LLM to get the code
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a travel expert. Given a city name, return ONLY the 3-letter IATA city code.

Rules:
- Return only the 3-letter code in uppercase
- If multiple airports serve the city, return the main city code (not individual airport codes)
- For cities without IATA codes, return the closest major city code
- If unsure, return 'UNKNOWN'

Examples:
- New York → NYC
- Los Angeles → LAX
- London → LON
- Paris → PAR
- Tokyo → TYO"""
                    },
                    {
                        "role": "user",
                        "content": f"What is the IATA city code for: {city_name}"
                    }
                ],
                max_tokens=10,
                temperature=0
            )

            code = response.choices[0].message.content.strip().upper()

            # Validate the code format
            if re.match(r'^[A-Z]{3}$', code) and code != 'UNKNOWN':
                # Cache the result
                self.city_code_cache[city_lower] = code
                return code
            else:
                print(f"Could not determine city code for '{city_name}'")
                return None

        except Exception as e:
            print(f"Error getting city code for '{city_name}': {e}")
            return None

    def get_multiple_cities(self, city_names: List[str]) -> Dict[str, str]:
        """Get codes for multiple cities at once"""
        try:
            cities_text = ", ".join(city_names)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a travel expert. Given a list of city names, return their IATA city codes in JSON format.

Rules:
- Return a JSON object with city names as keys and 3-letter IATA codes as values
- Use uppercase for codes
- For cities without codes, use the closest major city
- If completely unsure, use null

Example format:
{\"New York\": \"NYC\", \"Los Angeles\": \"LAX\", \"London\": \"LON\"}"""
                    },
                    {
                        "role": "user",
                        "content": f"Get IATA city codes for these cities: {cities_text}"
                    }
                ],
                max_tokens=200,
                temperature=0
            )

            result = json.loads(response.choices[0].message.content.strip())

            # Update cache with results
            for city, code in result.items():
                if code and re.match(r'^[A-Z]{3}$', code):
                    self.city_code_cache[city.lower()] = code

            return result

        except Exception as e:
            print(f"Error getting multiple city codes: {e}")
            return {}