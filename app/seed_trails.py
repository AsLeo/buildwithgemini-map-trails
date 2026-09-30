"""Seed script for Map Trails Firestore collection.

Project ID is explicitly hardcoded as a string to prevent Agent Platform issues.
"""

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-bf5aaa9ae6a0"
COLLECTION_NAME = "trails"

SEEDED_TRAILS = [
    {
        "id": "rattlesnake-ledge",
        "name": "Rattlesnake Ledge",
        "region": "Snoqualmie Region - North Bend",
        "distance_miles": 4.0,
        "elevation_gain_ft": 1160,
        "highest_point_ft": 2078,
        "difficulty": "Moderate",
        "rating": 4.4,
        "pass_required": "None",
        "dogs_allowed": True,
        "latitude": 47.4348,
        "longitude": -121.7678,
        "description": "Popular hike ascending through dense forest to massive rock ledges overlooking Rattlesnake Lake and the Cedar River watershed.",
        "completed": False,
        "completed_at": None,
        "user_rating": None,
        "notes": ""
    },
    {
        "id": "mount-si",
        "name": "Mount Si",
        "region": "Snoqualmie Region - North Bend",
        "distance_miles": 8.0,
        "elevation_gain_ft": 3150,
        "highest_point_ft": 3900,
        "difficulty": "Strenuous",
        "rating": 4.3,
        "pass_required": "Discover Pass",
        "dogs_allowed": True,
        "latitude": 47.4881,
        "longitude": -121.7231,
        "description": "An iconic Washington workout trail climbing steeply to stunning panoramic views of Mount Rainier and the Snoqualmie Valley.",
        "completed": False,
        "completed_at": None,
        "user_rating": None,
        "notes": ""
    },
    {
        "id": "snow-lake",
        "name": "Snow Lake",
        "region": "Snoqualmie Pass",
        "distance_miles": 7.2,
        "elevation_gain_ft": 1800,
        "highest_point_ft": 4400,
        "difficulty": "Moderate",
        "rating": 4.6,
        "pass_required": "Northwest Forest Pass",
        "dogs_allowed": True,
        "latitude": 47.4447,
        "longitude": -121.4233,
        "description": "The most visited alpine lake in the Alpine Lakes Wilderness, featuring sweeping basin views and crystal turquoise waters.",
        "completed": False,
        "completed_at": None,
        "user_rating": None,
        "notes": ""
    },
    {
        "id": "skyline-trail-rainier",
        "name": "Skyline Trail Loop",
        "region": "Mount Rainier Area - SW",
        "distance_miles": 5.5,
        "elevation_gain_ft": 1450,
        "highest_point_ft": 6800,
        "difficulty": "Moderate/Strenuous",
        "rating": 4.8,
        "pass_required": "National Park Pass",
        "dogs_allowed": False,
        "latitude": 46.7865,
        "longitude": -121.7351,
        "description": "The crown jewel of Paradise at Mount Rainier, boasting close-up glacier views, cascading waterfalls, and vibrant subalpine meadows.",
        "completed": True,
        "completed_at": "2026-08-15",
        "user_rating": 5,
        "notes": "Incredible wildflowers at Panorama Point! Clear view of St. Helens and Adams."
    },
    {
        "id": "colchuck-lake",
        "name": "Colchuck Lake",
        "region": "Central Cascades - Leavenworth",
        "distance_miles": 8.0,
        "elevation_gain_ft": 2280,
        "highest_point_ft": 5570,
        "difficulty": "Strenuous",
        "rating": 4.9,
        "pass_required": "Northwest Forest Pass",
        "dogs_allowed": False,
        "latitude": 47.5349,
        "longitude": -120.8222,
        "description": "Gateway to the Enchantments featuring breathtaking glacial waters beneath the dramatic spires of Dragontail and Colchuck Peaks.",
        "completed": False,
        "completed_at": None,
        "user_rating": None,
        "notes": ""
    },
    {
        "id": "lake-22",
        "name": "Lake 22",
        "region": "Mountain Loop Highway",
        "distance_miles": 5.4,
        "elevation_gain_ft": 1350,
        "highest_point_ft": 2400,
        "difficulty": "Moderate",
        "rating": 4.5,
        "pass_required": "Northwest Forest Pass",
        "dogs_allowed": True,
        "latitude": 48.0678,
        "longitude": -121.7588,
        "description": "A classic alpine wetland and rainforest hike along the Mountain Loop Highway culminating in an awe-inspiring cirque and lake.",
        "completed": False,
        "completed_at": None,
        "user_rating": None,
        "notes": ""
    }
]


def seed_database():
    print(f"Connecting to Firestore using project ID: {PROJECT_ID}")
    db = firestore.Client(project=PROJECT_ID)
    trails_ref = db.collection(COLLECTION_NAME)

    for item in SEEDED_TRAILS:
        doc_id = item["id"]
        trails_ref.document(doc_id).set(item)
        print(f"  ✓ Seeded trail: {item['name']} ({doc_id})")

    print(f"\nSuccessfully seeded {len(SEEDED_TRAILS)} trails into collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    seed_database()
