import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

logo_url = "Images/LCY3 Logo.png"


# ---- Setup Page ----
st.set_page_config(
    layout="wide",
    page_title="LCY3 Stow Cart Runner DashBoard",
)
# Set the favicon (tab icon)
favicon_html = f"""
<link rel="shortcut icon" href={logo_url}>
"""

# Add the favicon to the page
components.html(favicon_html, height=0)
cols1, cols2, cols3 = st.columns(
    [3, 4, 3], vertical_alignment="center", gap="small"
)  # This creates a 10% and 80% split
with cols1:
    st.image(logo_url, width=200)
with cols2:
    # Vertically center title
    title_html = """
    <div style="justify-content:bottom; align-items:center;">
        <h1 style='font-size: 40px; margin-left: 10%;'>
            <span style='color: #6CB4EE;'>Amazon LCY3</span> 
            <span style='color: #7D4551;'>Cart Runner Dashboard</span>
        </h1>
    </div>
    """
    st.markdown(title_html, unsafe_allow_html=True)

with cols3:
    # Display the last updated timestamp
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"Last Updated: {last_updated}")


# ---- Google Sheets Setup ----
@st.cache_data(ttl=120)
def load_data():
    # Use credentials to create a client to interact with the Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Directly access Streamlit secrets and parse them as JSON
    credentials_dict = st.secrets["gcp"] 
    
    # Authenticate using the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)

    # Open your sheets (ensure the sheets are shared with your service account)
    sheet_qty = client.open("Online Dashboard").worksheet("stations_qty")
    sheet_totes = client.open("Online Dashboard").worksheet("stations_totes")

    # Convert to pandas DataFrames
    data_qty = pd.DataFrame(sheet_qty.get_all_records())
    data_totes = pd.DataFrame(sheet_totes.get_all_records())

    if not data_qty.empty:
        data_qty.set_index("Station", inplace=True)
    if not data_totes.empty:
        data_totes.set_index("Station", inplace=True)

    return data_qty, data_totes


# Fetch live values from cached data
def fetch_live_value(station_id, retrieved_df):
    try:
        return float(retrieved_df.loc[(station_id), "Current Value"])
    except KeyError:
        return "N/A"


# ---- Auto Refresh every 60 seconds ----
st_autorefresh(interval=60 * 1000 * 2, limit=None, key="data_refresh")

# ---- Load Data ----
retrieved_df, retrieved_df_totes = load_data()
colss1, cols2 = st.columns(2)
# ---- Floor and Side Selection ----
with colss1:
    floor = st.selectbox("Select a floor", [2, 3, 4])
with cols2:
    side = st.selectbox("Select a side", ["North", "South"])

# ---- Stations Dictionary (you must define it somewhere) ----
# Example dummy structure if not already defined
stations = {
    2: {
        "North": [
            2137,
            2138,
            2139,
            2143,
            2145,
            2149,
            2100,
            2155,
            2157,
            2161,
            2162,
            2163,
            2167,
            2170,
            2171,
            2172,
            2173,
            2174,
            2176,
            2177,
            2178,
        ],
        "South": [
            2322,
            2323,
            2324,
            2330,
            2331,
            2333,
            2339,
            2344,
            2345,
            2351,
            2352,
            2353,
            2359,
            2360,
            2365,
            2371,
            2372,
            2373,
            2374,
            2380,
            2385,
        ],
        "West": [
            2223,
            2227,
            2229,
            2232,
            2235,
            2238,
            2241,
            2243,
            2247,
            2251,
            2254,
            2257,
            2259,
            2263,
            2265,
            2269,
        ],
    },
    3: {
        "North": [
            3137,
            3138,
            3139,
            3143,
            3145,
            3100,
            3151,
            3155,
            3157,
            3162,
            3163,
            3164,
            3168,
            3171,
            3172,
            3173,
            3174,
            3175,
            3177,
            3178,
            3179,
        ],
        "South": [
            3320,
            3321,
            3322,
            3328,
            3330,
            3331,
            3337,
            3342,
            3343,
            3349,
            3350,
            3352,
            3358,
            3359,
            3364,
            3370,
            3372,
            3373,
            3374,
            3380,
            3385,
        ],
        "West": [
            3232,
            3235,
            3236,
            3239,
            3241,
            3244,
            3246,
            3249,
            3253,
            3254,
            3256,
            3258,
            3260,
            3263,
            3265,
            3268,
        ],
    },
    4: {
        "North": [
            4140,
            4141,
            4142,
            4146,
            4148,
            4152,
            4153,
            4158,
            4160,
            4165,
            4166,
            4167,
            4171,
            4174,
            4175,
            4176,
            4177,
            4178,
            4180,
            4181,
            4182,
        ],
        "South": [
            4323,
            4324,
            4325,
            4331,
            4332,
            4333,
            4339,
            4344,
            4345,
            4351,
            4352,
            4353,
            4360,
            4361,
            4366,
            4372,
            4373,
            4374,
            4375,
            4382,
            4387,
        ],
        "West": [
            4229,
            4231,
            4233,
            4235,
            4238,
            4240,
            4242,
            4243,
            4247,
            4249,
            4251,
            4254,
            4256,
            4258,
            4260,
            4263,
        ],
    },
}


def render_station_card(station_id, value, bg_color):
    return f"""
        <div style='background-color:{bg_color}; padding:40px; border:2px solid black;
        font-size:24px; width:100px; height:100px; text-align:center;
        display:flex; align-items:center; justify-content:center;'>
            {station_id}<br>{value}
        </div>
    """


def get_station_color(station, qty_df, totes_df):
    try:
        qty = float(fetch_live_value(station, qty_df))
        totes = float(fetch_live_value(station, totes_df))
        ratio = qty / totes if totes != 0 else 0
        if ratio > 6:
            return "green"
        elif ratio > 2:
            return "orange"
        elif ratio == 0:
            return "blue"
        else:
            return "red"
    except:
        return "blue"  # for 'N/A', 'Error', or other issues


# ---- Display Logic ----
if floor in stations and side in stations[floor]:
    side_stations = stations[floor][side].copy()
    west_stations = stations[floor]["West"].copy()

    if side == "North":
        side_stations.reverse()
        side_stations.insert(0, "")  # Empty card at the start

        # Display North side stations
        st.markdown(
            "<div style='display:flex; gap:20px;'>"
            + "".join(
                [
                    (
                        f"<div style='background-color:{get_station_color(s, retrieved_df, retrieved_df_totes)}; padding:40px; border:2px solid black; font-size:30px; width:250px; height:200px; text-align:center; display:flex; align-items:center; justify-content:center;'>{s}<br>{fetch_live_value(s, retrieved_df)}<br>{fetch_live_value(s, retrieved_df_totes)}</div>"
                        if s
                        else f"<div style='background-color:{get_station_color(s, retrieved_df, retrieved_df_totes)}; padding:40px; border:2px solid black; font-size:30px; width:200px; height:150px; text-align:center; display:flex; align-items:center; justify-content:center;'>&nbsp;</div>"
                    )
                    for s in side_stations
                ]
            )
            + "</div>",
            unsafe_allow_html=True,
        )

        # Display West side stations (first half)
        half = len(west_stations) // 2
        for s in west_stations[:half]:
            st.markdown(
                "<div style='display:flex; gap:20px;'>"
                + f"<div style='background-color: {get_station_color(s, retrieved_df, retrieved_df_totes)}; padding:40px; border:2px solid black; font-size:24px; width:200px; height:150px; text-align:center; display:flex; align-items:center; justify-content:center;margin-top:20px;'>{s}<br>{fetch_live_value(s, retrieved_df)}<br>{fetch_live_value(s, retrieved_df_totes)}</div>"
                + "</div>",
                unsafe_allow_html=True,
            )

    elif side == "South":
        side_stations.insert(0, "")  # Empty card at the start

        half = len(west_stations) // 2
        # Display West side stations (second half)
        for s in west_stations[half:]:
            st.markdown(
                "<div style='display:flex; gap:20px;'>"
                + f"<div style='background-color:{get_station_color(s, retrieved_df, retrieved_df_totes)}; padding:20px; border:2px solid black; font-size:30px; width:200px; height:150px; text-align:center; display:flex; align-items:center; justify-content:center;margin-bottom:20px;'>{s}<br>{fetch_live_value(s, retrieved_df)}<br>{fetch_live_value(s, retrieved_df_totes)}</div>"
                + "</div>",
                unsafe_allow_html=True,
            )

        # Display South side stations
        st.markdown(
            "<div style='display:flex; gap:20px;'>"
            + "".join(
                [
                    (
                        f"<div style= 'background-color: {get_station_color(s, retrieved_df, retrieved_df_totes)}; padding:40px; border:2px solid black; font-size:30px; width:200px; height:150px; text-align:center; display:flex; align-items:center; justify-content:center;'>{s}<br>{fetch_live_value(s, retrieved_df)}<br>{fetch_live_value(s, retrieved_df_totes)}</div>"
                        if s
                        else f"<div style='background-color: {get_station_color(s, retrieved_df, retrieved_df_totes)}; padding:40px; border:2px solid black; font-size:30px; width:200px; height:150px; text-align:center; display:flex; align-items:center; justify-content:center;'>&nbsp;</div>"
                    )
                    for s in side_stations
                ]
            )
            + "</div>",
            unsafe_allow_html=True,
        )

else:
    st.error("Invalid selection. Please choose a valid floor and side.")
