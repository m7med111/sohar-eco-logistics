import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import searoute as sr

# 1. PAGE SETUP
st.set_page_config(page_title="Sohar Port Logistics", layout="wide")

SOHAR_PORT = [56.6267, 24.3644] 

def get_live_vessel_data():
    # Added "Target_Delay_Hrs" to simulate real terminal schedules
    vessels = [
        {"Vessel": "MSC Muscat", "Current_Loc": [65.0000, 20.0000], "Type": "Container", "Destination": "Oman Container Terminal (OICT)", "Target_Delay_Hrs": 8.0}, 
        {"Vessel": "OQ Tanker V", "Current_Loc": [59.0000, 23.0000], "Type": "Tanker", "Destination": "Advario Liquid Bulk Terminal", "Target_Delay_Hrs": 0.0},   
        {"Vessel": "Jindal Steel 1", "Current_Loc": [72.8777, 19.0760], "Type": "Bulker", "Destination": "Jindal Shadeed Jetty", "Target_Delay_Hrs": 14.5} 
    ]
    
    data = []
    base_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    
    for v in vessels:
        route = sr.searoute(v["Current_Loc"], SOHAR_PORT)
        distance_nm = route['properties']['length'] 
        
        speed_fast = 18.0
        hours_fast = distance_nm / speed_fast
        emissions_fast = (speed_fast ** 3) * 0.002 * hours_fast 
        
        data.append({
            "Vessel": v["Vessel"],
            "Destination": v["Destination"],
            "Target_Delay_Hrs": v["Target_Delay_Hrs"], # Hidden logic variable
            "Original Hours": hours_fast,              # Needed for math
            "Distance (NM)": round(distance_nm, 1),
            "Original Speed (Knots)": speed_fast,
            "Original ETA": base_time + timedelta(hours=hours_fast),
            "Original Emissions (Tons)": emissions_fast
        })
        
    return pd.DataFrame(data)

df = get_live_vessel_data()

# 3. SIDEBAR CONTROLS
st.sidebar.title("AI Controls")
optimization = st.sidebar.slider("Activate JIT Arrival (%)", 0, 100, 0)

st.title("Sohar Port: Geospatial AI Routing")
st.write("Live API routing calculating exact nautical miles and fuel consumption.")

# 5. THE TRUE DYNAMIC AI LOGIC
df["Optimized Speed (Knots)"] = df["Original Speed (Knots)"]
df["Optimized ETA"] = df["Original ETA"]
df["Action Taken"] = "None"
df["Emissions Saved (Tons)"] = 0.0
df["Final Emissions (Tons)"] = df["Original Emissions (Tons)"]

if optimization > 0:
    factor = optimization / 100
    
    for index, row in df.iterrows():
        # Only optimize if there is actually a delay at the terminal!
        if row["Target_Delay_Hrs"] > 0:
            # Apply the slider percentage to the required delay
            applied_delay = row["Target_Delay_Hrs"] * factor
            new_total_hours = row["Original Hours"] + applied_delay
            
            # MATH: Speed = Distance / Time (Calculate bespoke speed)
            speed_slow = row["Distance (NM)"] / new_total_hours
            
            # Recalculate Emissions with the new exact speed
            emissions_slow = (speed_slow ** 3) * 0.002 * new_total_hours
            saved_co2 = row["Original Emissions (Tons)"] - emissions_slow
            
            new_eta = datetime.now().replace(minute=0, second=0) + timedelta(hours=new_total_hours)
            
            df.at[index, "Optimized Speed (Knots)"] = round(speed_slow, 1)
            df.at[index, "Optimized ETA"] = new_eta
            df.at[index, "Action Taken"] = f"Speed optimized to {speed_slow:.1f} kts."
            df.at[index, "Emissions Saved (Tons)"] = saved_co2
            df.at[index, "Final Emissions (Tons)"] = emissions_slow
        else:
            # The AI is smart enough to know the berth is empty
            df.at[index, "Action Taken"] = "Terminal clear. Maintain 18.0 kts."

df["Original ETA"] = df["Original ETA"].dt.strftime("%d-%b %H:%M")
df["Optimized ETA"] = df["Optimized ETA"].dt.strftime("%d-%b %H:%M")

# 6. METRICS
col1, col2, col3 = st.columns(3)
col1.metric("Total Vessels Tracked", len(df))
col2.metric("Total Route Emissions", f'{df["Final Emissions (Tons)"].sum():.1f} Tons')
col3.metric("Total CO2 Prevented", f'{df["Emissions Saved (Tons)"].sum():.1f} Tons', delta="Green Impact")

st.divider()

# 7. PROOF TABLE
st.subheader("Geospatial Rescheduling Engine")
display_df = df[["Vessel", "Destination", "Distance (NM)", "Original Speed (Knots)", "Optimized Speed (Knots)", "Original ETA", "Optimized ETA", "Action Taken", "Emissions Saved (Tons)"]]
display_df["Emissions Saved (Tons)"] = display_df["Emissions Saved (Tons)"].round(1)
st.dataframe(display_df, use_container_width=True, hide_index=True)

st.divider()

# 8. CHARTS
chart_col1, chart_col2 = st.columns([2, 1])
with chart_col1:
    st.subheader("Emissions by Vessel")
    fig_bar = px.bar(df, x="Vessel", y="Final Emissions (Tons)")
    fig_bar.update_traces(marker_color="#0047AB") 
    fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    st.subheader("EU Compliance")
    status_df = pd.DataFrame({
        "Status": ["Compliant", "Penalty Risk"],
        "Count": [1, 2] if optimization < 90 else [3, 0]
    })
    fig_pie = px.pie(status_df, names="Status", values="Count", hole=0.7)
    fig_pie.update_traces(marker=dict(colors=["#0047AB", "#D3D3D3"]))
    fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pie, use_container_width=True)