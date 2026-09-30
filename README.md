# 🌲 Map Trails — Washington Hiking Concierge & Interactive Explorer

Map Trails is an intelligent agentic hiking assistant built with Google Agent Development Kit (ADK) and Gemini on Vertex AI. It helps Pacific Northwest hikers explore 3,600+ Washington Trails Association (WTA) routes, track completed hikes with Firestore, retrieve real-time trailhead weather, and visualize statewide trail networks on an interactive topographic map.

---

## 🌟 Key Features

- **Washington State Trail Database**: Over 3,651 curated WTA trails and statewide GIS trail polylines (including Mount Rainier Skyline Loop, Enchantments, Dirtyface Peak Trail #1500, Mount Si, and more).
- **Interactive Topographic Map (`/map.html`)**:
  - Unhiked trails rendered in sleek black.
  - Completed/hiked trails rendered in vibrant green.
  - Full trail line hover capability displaying trail name, elevation gain, and distance statistics.
  - Click-to-toggle completion status.
  - Completed hike cluster badges when zoomed out.
- **Rich A2UI Display**: Renders interactive cards, lists, elevation badges, and weather forecasts directly in chat.
- **Persistent Hiker Journal**: Backed by Google Cloud Firestore to track user completions, dates, ratings, and trail notes.
- **A2A Protocol & Cloud Run Frontend**: FastAPI proxy communicating over the Agent-to-Agent (A2A) protocol with the deployed Vertex AI Agent Engine reasoning engine.

---

## 🏗️ Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │          Cloud Run Frontend (A2A)            │
                       │   • FastAPI Proxy Server                     │
                       │   • A2UI Card Renderer & Chat UI             │
                       │   • Interactive Leaflet / GIS Trail Map      │
                       └──────────────────────┬───────────────────────┘
                                              │ A2A Protocol (ADC)
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │   Vertex AI Agent Platform (Agent Engine)    │
                       │   • Gemini 2.5 Flash                         │
                       │   • Trail Search & Detail Tools              │
                       │   • Open-Meteo Trailhead Weather Tool        │
                       │   • Cloud Firestore Completion Tracker       │
                       └──────────────────────────────────────────────┘
```

---

## 🚀 Running Locally

### 1. Requirements
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- `google-agents-cli`

### 2. Local Setup
```bash
# Clone the repository
git clone https://github.com/AsLeo/buildwithgemini-map-trails.git
cd buildwithgemini-map-trails

# Install dependencies
uv sync

# Launch local agent playground
agents-cli playground
```

### 3. Frontend Local Server
```bash
cd frontend
pip install -r requirements.txt
export AGENT_ENGINE_RESOURCE_NAME="projects/.../locations/.../reasoningEngines/..."
export AGENT_DIRECTORY="app"
python main.py
```
Open `http://localhost:8080` for the chat interface or `http://localhost:8080/map.html` for the trail map.

---

## 🛠️ Built With

- **Google Agent Development Kit (ADK)**
- **Vertex AI Agent Engine**
- **Gemini 2.5 Flash**
- **Cloud Firestore**
- **Cloud Run**
- **Leaflet.js & Esri ArcGIS Services**
- **Washington Trails Association (WTA) & USFS GIS Data**
