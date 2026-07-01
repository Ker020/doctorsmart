import requests
from flask import current_app

class MapsService:
    @staticmethod
    def find_nearest_doctors(specialty, lat, lng, radius=5000):
        """
        Finds nearest doctors of a specific specialty using Google Places API.
        """
        api_key = current_app.config['GOOGLE_PLACES_KEY']
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "keyword": f"{specialty} doctor",
            "key": api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json().get('results', [])
            
            doctors = []
            for place in results[:5]: # Top 5
                doctors.append({
                    "name": place.get('name'),
                    "address": place.get('vicinity'),
                    "rating": place.get('rating', 'N/A'),
                    "user_ratings_total": place.get('user_ratings_total', 0)
                })
            return doctors
        except Exception as e:
            print(f"Error calling Maps API: {e}")
            return []
