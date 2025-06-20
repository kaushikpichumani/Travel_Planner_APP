import requests
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from city_resolver import CityCodeResolver # Assuming city_resolver.py is in the same directory
import config
class SmartHotelSearch:
    """Hotel search with intelligent city code resolution"""

    def __init__(self, amadeus_api_key: str, amadeus_api_secret: str, openai_api_key: str):
        self.amadeus_api_key = amadeus_api_key
        self.amadeus_api_secret = amadeus_api_secret
        self.base_url = "https://test.api.amadeus.com"
        self.access_token = None
        self.token_expires_at = None

        # Initialize city code resolver
        self.city_resolver = CityCodeResolver(openai_api_key)

    def get_access_token(self):
        """Get OAuth access token for Amadeus API"""
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.access_token

        url = f"{self.base_url}/v1/security/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.amadeus_api_key,
            'client_secret': self.amadeus_api_secret
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()

            token_data = response.json()
            self.access_token = token_data['access_token']
            expires_in = token_data['expires_in']
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)

            return self.access_token

        except requests.exceptions.RequestException as e:
            print(f"Error getting access token: {e}")
            return None

    def Google_Hotels_by_city_name(self, city_name: str, checkin_date: str, checkout_date: str,
                                  adults: int = 1, rooms: int = 1, max_results: int = 20):
        """Search hotels by city name (automatically converts to city code)"""

        print(f"🔍 Resolving city code for '{city_name}'...")
        city_code = self.city_resolver.get_city_code(city_name)

        if not city_code:
            print(f"❌ Could not determine city code for '{city_name}'")
            return None

        print(f"✅ Found city code: {city_code}")

        # Validate dates
        try:
            checkin_dt = datetime.strptime(checkin_date, '%Y-%m-%d')
            checkout_dt = datetime.strptime(checkout_date, '%Y-%m-%d')

            if checkin_dt <= datetime.now():
                print("⚠️  Warning: Check-in date should be in the future")
            if checkout_dt <= checkin_dt:
                print("❌ Error: Check-out date must be after check-in date")
                return None
        except ValueError as e:
            print(f"❌ Invalid date format: {e}")
            return None

        return self.Google_Hotels_by_city_code(city_code, checkin_date, checkout_date, adults, rooms, max_results)

    def Google_Hotels_by_city_code(self, city_code: str, checkin_date: str, checkout_date: str,
                                  adults: int = 1, rooms: int = 1, max_results: int = 20):
        """Search hotels by IATA city code"""
        token = self.get_access_token()
        if not token:
            return None

        # Step 1: Get hotels in the city
        url = f"{self.base_url}/v1/reference-data/locations/hotels/by-city"
        headers = {'Authorization': f'Bearer {token}'}
        params = {
            'cityCode': city_code,
            'radius': 20,
            'radiusUnit': 'KM',
            'hotelSource': 'ALL'
        }

        print(f"🏨 Searching hotels in {city_code}...")

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"❌ Hotel search error: {response.text}")
                return None

            hotels_data = response.json()

            if 'data' not in hotels_data or not hotels_data['data']:
                print("❌ No hotels found for the specified city")
                return []

            print(f"✅ Found {len(hotels_data['data'])} hotels")

            # Step 2: Get prices for hotels
            hotel_ids = [hotel['hotelId'] for hotel in hotels_data['data'][:max_results]]
            return self.get_hotel_prices(hotel_ids, checkin_date, checkout_date, adults, rooms)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching hotels: {e}")
            return None

    def get_hotel_prices(self, hotel_ids: List[str], checkin_date: str, checkout_date: str,
                        adults: int = 1, rooms: int = 1):
        """Get prices for specific hotels"""
        token = self.get_access_token()
        if not token:
            return None

        url = f"{self.base_url}/v3/shopping/hotel-offers"
        headers = {'Authorization': f'Bearer {token}'}

        # Limit hotel IDs to avoid URL length issues
        hotel_ids_limited = hotel_ids[:15]  # Reduced further for stability
        hotel_ids_str = ','.join(hotel_ids_limited)

        params = {
            'hotelIds': hotel_ids_str,
            'checkInDate': checkin_date,
            'checkOutDate': checkout_date,
            'adults': adults,
            'roomQuantity': rooms,
            'currency': 'USD',
            'lang': 'EN'
        }

        print(f"💰 Getting prices for {len(hotel_ids_limited)} hotels...")

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"❌ Price error ({response.status_code}): {response.text}")
                return None

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting hotel prices: {e}")
            return None

def parse_hotel_offers(hotel_data):
    """Parse hotel offers into a readable format"""
    if not hotel_data or 'data' not in hotel_data:
        return []

    hotels = []
    for hotel in hotel_data['data']:
        hotel_info = hotel['hotel']

        for offer in hotel['offers']:
            price = offer['price']
            room = offer['room']

            hotels.append({
                'hotel_id': hotel_info['hotelId'],
                'hotel_name': hotel_info.get('name', 'N/A'),
                'address': hotel_info.get('address', {}).get('lines', ['N/A'])[0],
                'city': hotel_info.get('address', {}).get('cityName', 'N/A'),
                'rating': hotel_info.get('rating', 'N/A'),
                'room_type': room.get('type', 'N/A'),
                'room_description': room.get('typeEstimated', {}).get('category', 'N/A'),
                'price_total': float(price['total']),
                'price_base': float(price['base']),
                'currency': price['currency'],
                'cancellation_deadline': offer.get('policies', {}).get('cancellation', {}).get('deadline', 'N/A')
            })

    return hotels