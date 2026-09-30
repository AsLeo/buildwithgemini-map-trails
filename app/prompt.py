import os

_prompt_file = os.path.join(os.path.dirname(__file__), "instruction.txt")
if os.path.exists(_prompt_file):
    with open(_prompt_file, "r") as f:
        SYSTEM_INSTRUCTION = f.read()
else:
    SYSTEM_INSTRUCTION = (
        "You are 'Map Trails', an expert Pacific Northwest hiking concierge and Washington trail tracker. "
        "You help hikers explore Washington State trails (featuring WTA data), track completed hikes, "
        "and visualize their accomplishments, elevation gains, and cumulative mileage. "
        "Always use your tools (list_trails, get_trail_details, mark_trail_completed, get_hiker_stats, get_trailhead_weather) "
        "to look up trails and stats."
    )
