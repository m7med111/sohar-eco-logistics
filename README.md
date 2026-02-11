# 🚢 Sohar Port: AI Geospatial Routing & Decarbonization

An intelligent, proactive Just-In-Time (JIT) arrival dashboard built for the Sohar Port hackathon. This application uses live geospatial tracking and maritime physics to eliminate vessel idle time, reduce fuel consumption, and automatically generate EU-CBAM compliant Scope 3 emissions certificates.

## ⚠️ The Problem
Currently, vessels arriving at Sohar Port operate on a "hurry up and wait" model. Ships sail at maximum speed to reach the port, only to find the terminal congested. They drop anchor and run their massive auxiliary diesel engines for hours (or days), creating a massive **Scope 3 Carbon Emission** problem for the port and its tenants.

## 💡 The AI Solution
Instead of reacting to delays, our algorithm acts proactively:
1. It ingests live GPS coordinates of incoming vessels.
2. It cross-references the ship's specific destination (e.g., Oman Container Terminal, Advario Liquid Bulk Terminal) with real-time berth availability.
3. If a delay is predicted, the AI calculates a custom speed reduction command, instructing the vessel to slow down in the ocean and arrive *exactly* when the berth opens.

### 📐 The Math (The Cube Rule)
The system calculates fuel savings using the maritime "Cube Rule" ($Fuel \propto Speed^3$). By slowing a ship down by just 10-20% in the ocean, fuel consumption drops exponentially. The ship saves money on transit fuel, and the port completely eliminates idle emissions at the dock.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Python)
* **Data Manipulation:** Pandas
* **Data Visualization:** Plotly
* **Geospatial Routing:** `searoute` (Calculates accurate maritime nautical miles avoiding landmasses)

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/m7med111/sohar-eco-logistics.git](https://github.com/m7med111/sohar-eco-logistics.git)
   cd sohar-eco-logistics

   "for Linux/Mac:"
   python3 -m streamlit run app.py --theme.base="light"

   "for windows"
   python -m streamlit run app.py --theme.base="light"