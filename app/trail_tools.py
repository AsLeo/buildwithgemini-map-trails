"""Firestore tools for Map Trails agent.

Hardcodes PROJECT_ID as a string to avoid project number issues on Agent Platform.
"""

from typing import Any, Dict, List, Optional
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-bf5aaa9ae6a0"
COLLECTION_NAME = "trails"


def _get_db() -> firestore.Client:
    return firestore.Client(project=PROJECT_ID)


def list_trails(region: Optional[str] = None, completed_only: Optional[bool] = None) -> List[Dict[str, Any]]:
    """List trails from the Washington State trail catalog with optional filtering.

    Args:
        region: Optional case-insensitive region substring (e.g. 'Snoqualmie', 'Rainier', 'Cascades').
        completed_only: If True, only returns trails marked completed. If False, only uncompleted trails. If None, returns all.

    Returns:
        A list of trail dictionaries with trail info and stats.
    """
    db = _get_db()
    docs = db.collection(COLLECTION_NAME).stream()
    results = []

    for doc in docs:
        data = doc.to_dict()
        if completed_only is not None and data.get("completed", False) != completed_only:
            continue
        if region and region.lower() not in data.get("region", "").lower():
            continue
        results.append(data)

    return results


def get_trail_details(trail_id: str) -> Dict[str, Any]:
    """Retrieve detailed information for a specific hiking trail.

    Args:
        trail_id: The unique ID or slug of the trail (e.g., 'mount-si', 'skyline-trail-rainier').

    Returns:
        The trail's detail record, or an error message if not found.
    """
    db = _get_db()
    doc = db.collection(COLLECTION_NAME).document(trail_id).get()
    if not doc.exists:
        return {"error": f"Trail '{trail_id}' not found."}
    return doc.to_dict()


def mark_trail_completed(
    trail_id: str,
    completed: bool = True,
    completion_date: Optional[str] = None,
    user_rating: Optional[int] = None,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """Mark a hiking trail as completed (or uncompleted) and record user notes/ratings.

    Args:
        trail_id: The ID of the trail to update.
        completed: True to mark completed, False to unmark.
        completion_date: Optional ISO date string (YYYY-MM-DD).
        user_rating: Optional rating from 1 to 5 stars.
        notes: Optional personal trip notes or conditions report.

    Returns:
        A confirmation dictionary with the updated trail details.
    """
    db = _get_db()
    doc_ref = db.collection(COLLECTION_NAME).document(trail_id)
    doc = doc_ref.get()
    if not doc.exists:
        return {"error": f"Trail '{trail_id}' not found."}

    update_payload: Dict[str, Any] = {"completed": completed}
    if completed:
        if completion_date:
            update_payload["completed_at"] = completion_date
        if user_rating is not None:
            update_payload["user_rating"] = user_rating
        if notes is not None:
            update_payload["notes"] = notes
    else:
        update_payload["completed_at"] = None
        update_payload["user_rating"] = None
        update_payload["notes"] = ""

    doc_ref.update(update_payload)
    updated = doc_ref.get().to_dict()
    return {"message": f"Updated trail '{updated.get('name')}' status.", "trail": updated}


def get_hiker_stats() -> Dict[str, Any]:
    """Calculate cumulative stats for all completed hikes in Washington state.

    Returns:
        A dictionary containing total trails completed, total miles hiked, total elevation gain, and completed list.
    """
    db = _get_db()
    docs = db.collection(COLLECTION_NAME).stream()

    total_completed = 0
    total_miles = 0.0
    total_elevation_ft = 0
    completed_trails = []

    for doc in docs:
        data = doc.to_dict()
        if data.get("completed", False):
            total_completed += 1
            total_miles += data.get("distance_miles", 0.0)
            total_elevation_ft += data.get("elevation_gain_ft", 0)
            completed_trails.append({
                "id": data.get("id"),
                "name": data.get("name"),
                "distance_miles": data.get("distance_miles"),
                "elevation_gain_ft": data.get("elevation_gain_ft"),
                "region": data.get("region"),
                "completed_at": data.get("completed_at"),
                "user_rating": data.get("user_rating")
            })

    return {
        "total_completed": total_completed,
        "total_miles_hiked": round(total_miles, 1),
        "total_elevation_gain_ft": total_elevation_ft,
        "completed_trails": completed_trails
    }


def get_trailhead_weather(trail_id: str) -> Dict[str, Any]:
    """Fetch current live weather conditions at a specific trail's coordinates.

    Args:
        trail_id: The ID of the trail (e.g., 'mount-si', 'skyline-trail-rainier', 'snow-lake').

    Returns:
        A dictionary containing temperature in Fahrenheit, wind speed, precipitation, and general conditions.
    """
    import json
    import urllib.request

    trail = get_trail_details(trail_id)
    if "error" in trail:
        return trail

    lat = trail.get("latitude")
    lon = trail.get("longitude")
    if lat is None or lon is None:
        return {"error": f"No GPS coordinates available for trail '{trail.get('name')}'."}

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current=temperature_2m,precipitation,weather_code,wind_speed_10m"
        f"&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
    )

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MapTrails/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            current = data.get("current", {})

            # Weather interpretation code mapping
            wmo_codes = {
                0: "Clear sky",
                1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Foggy", 48: "Depositing rime fog",
                51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
                61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
                71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
                80: "Rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
                85: "Slight snow showers", 86: "Heavy snow showers",
                95: "Thunderstorm"
            }
            code = current.get("weather_code", 0)
            condition_desc = wmo_codes.get(code, "Variable")

            return {
                "trail_name": trail.get("name"),
                "trail_id": trail_id,
                "region": trail.get("region"),
                "elevation_gain_ft": trail.get("elevation_gain_ft"),
                "temperature_f": current.get("temperature_2m"),
                "condition": condition_desc,
                "precipitation_in": current.get("precipitation"),
                "wind_speed_mph": current.get("wind_speed_10m")
            }
    except Exception as e:
        return {"error": f"Failed to fetch weather for {trail.get('name')}: {str(e)}"}

