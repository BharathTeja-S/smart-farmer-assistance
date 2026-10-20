from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

app.secret_key = "smart-farmer-secret-key"


# =========================================================
# DATABASE
# =========================================================

def get_db():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_database():

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# LOGIN CHECK
# =========================================================

def check_login():

    return "user_id" in session


# =========================================================
# HOME / LOGIN PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    connection = get_db()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    connection.close()

    if user and check_password_hash(
        user["password"],
        password
    ):

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect("/dashboard")

    return render_template(
        "index.html",
        error="Invalid username or password"
    )


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if len(username) < 3:
        return render_template("register.html", error="Username must contain at least 3 characters.")

    if len(password) < 6:
        return render_template("register.html", error="Password must contain at least 6 characters.")

    if password != confirm_password:
        return render_template("register.html", error="Passwords do not match.")

    connection = get_db()

    try:
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        connection.commit()
    except sqlite3.IntegrityError:
        connection.close()
        return render_template("register.html", error="That username is already registered.")

    connection.close()
    return redirect("/")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if not check_login():
        return redirect("/")

    month = datetime.now().month
    if month in (6, 7, 8, 9, 10):
        current_season = "kharif"
        seasonal_names = ["rice", "maize", "groundnut", "cotton", "soybean"]
    elif month in (11, 12, 1, 2):
        current_season = "rabi"
        seasonal_names = ["wheat", "chickpea", "potato", "onion", "groundnut"]
    else:
        current_season = "zaid"
        seasonal_names = ["tomato", "sugarcane", "banana", "onion", "maize"]

    recommended_crops = [
        {
            "name": name.replace("_", " ").title(),
            "key": name,
            "icon": {"rice": "🌾", "maize": "🌽", "groundnut": "🥜", "cotton": "🌿", "soybean": "🫘", "wheat": "🌾", "chickpea": "🫘", "potato": "🥔", "onion": "🧅", "tomato": "🍅", "sugarcane": "🎋", "banana": "🍌"}.get(name, "🌱"),
            "irrigation": recommendation["irrigation"],
            "advice": recommendation["advice"],
            "season": current_season.title(),
        }
        for name in seasonal_names[:3]
        for recommendation in [get_crop_recommendation(name, "loamy", current_season, "medium")]
    ]

    return render_template(
        "dashboard.html",
        username=session["username"],
        current_season=current_season.title(),
        recommended_crops=recommended_crops,
        all_crops=seasonal_names
    )


# =========================================================
# WEATHER API
# =========================================================

@app.route("/api/weather")
def api_weather():

    city = request.args.get(
        "city",
        "Chennai"
    )

    try:

        # -------------------------------
        # FIND CITY
        # -------------------------------

        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
        )

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_data = geo_response.json()

        if not geo_data.get("results"):

            return jsonify({
                "error": "City not found"
            }), 404

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        city_name = location["name"]
        country = location.get("country", "")
        state = location.get("admin1", "")

        # -------------------------------
        # WEATHER
        # -------------------------------

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )

        weather_params = {

            "latitude": latitude,

            "longitude": longitude,

            "current": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "rain",
                "weather_code",
                "wind_speed_10m",
                "wind_direction_10m"
            ]),

            "hourly": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation_probability",
                "precipitation",
                "weather_code",
                "wind_speed_10m"
            ]),

            "daily": ",".join([
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "precipitation_sum"
            ]),

            "timezone": "auto",
            "forecast_days": 5
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_data = weather_response.json()

        return jsonify({

            "location": {
                "city": city_name,
                "state": state,
                "country": country,
                "latitude": latitude,
                "longitude": longitude
            },

            "current": weather_data.get(
                "current",
                {}
            ),

            "daily": weather_data.get(
                "daily",
                {}
            ),

            "hourly": weather_data.get(
                "hourly",
                {}
            )

        })

    except Exception as e:

        print(
            "WEATHER ERROR:",
            str(e)
        )

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# WEATHER PAGE
# =========================================================

@app.route("/weather")
def weather():

    if not check_login():
        return redirect("/")

    latitude = 13.0827
    longitude = 80.2707

    try:

        weather_data = get_weather_data(
            latitude,
            longitude
        )

        current = weather_data.get(
            "current",
            {}
        )

        daily = weather_data.get(
            "daily",
            {}
        )

        advice = generate_weather_advice(
            current,
            daily
        )

        return render_template(
            "weather.html",
            username=session["username"],
            current=current,
            daily=daily,
            advice=advice,
            latitude=latitude,
            longitude=longitude
        )

    except Exception as e:

        print(
            "WEATHER PAGE ERROR:",
            str(e)
        )

        return render_template(
            "weather.html",
            username=session["username"],
            error="Unable to fetch weather data."
        )


# =========================================================
# WEATHER DATA FUNCTION
# =========================================================

def get_weather_data(
    latitude,
    longitude
):

    url = (
        "https://api.open-meteo.com/v1/forecast"
    )

    params = {

        "latitude": latitude,

        "longitude": longitude,

        "current":
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "precipitation",

        "daily":
            "precipitation_probability_max",

        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# WEATHER ADVICE
# =========================================================

def generate_weather_advice(
    current,
    daily
):

    advice = []

    temperature = current.get(
        "temperature_2m"
    )

    humidity = current.get(
        "relative_humidity_2m"
    )

    wind_speed = current.get(
        "wind_speed_10m"
    )

    rain_probability = 0

    if daily.get(
        "precipitation_probability_max"
    ):

        rain_probability = daily[
            "precipitation_probability_max"
        ][0]

    # Rain

    if rain_probability >= 70:

        advice.append(
            "🌧️ High chance of rain. Consider postponing irrigation."
        )

    elif rain_probability >= 40:

        advice.append(
            "🌦️ Moderate chance of rain. Monitor weather before irrigation."
        )

    else:

        advice.append(
            "☀️ Low chance of rain. Check soil moisture and plan irrigation if required."
        )

    # Temperature

    if temperature is not None:

        if temperature >= 35:

            advice.append(
                "🌡️ High temperature detected. Monitor crops for heat stress."
            )

        elif temperature <= 15:

            advice.append(
                "🥶 Low temperature detected. Monitor temperature-sensitive crops."
            )

    # Wind

    if wind_speed is not None:

        if wind_speed >= 30:

            advice.append(
                "💨 Strong winds detected. Avoid spraying pesticides or fertilizers."
            )

    # Humidity

    if humidity is not None:

        if humidity >= 80:

            advice.append(
                "💧 High humidity detected. Monitor crops for fungal diseases."
            )

    return advice


# =========================================================
# CROP ASSISTANCE
# =========================================================

@app.route("/crop-assistance")
def crop_assistance():

    if not check_login():
        return redirect("/")

    return render_template(
        "feature.html",
        title="Crop Assistance",
        icon="🌾",
        description="Get intelligent crop recommendations based on farming conditions.",
        username=session["username"]
    )


# =========================================================
# CROP RECOMMENDATION
# =========================================================

@app.route(
    "/crop-recommendation",
    methods=["POST"]
)
def crop_recommendation():

    if not check_login():
        return redirect("/")

    crop = request.form.get("crop")
    soil = request.form.get("soil")
    season = request.form.get("season")
    water = request.form.get("water")

    recommendation = get_crop_recommendation(
        crop,
        soil,
        season,
        water
    )

    return render_template(
        "crop_result.html",
        username=session["username"],
        crop=crop,
        soil=soil,
        season=season,
        water=water,
        recommendation=recommendation
    )


# =========================================================
# CROP RECOMMENDATION LOGIC
# =========================================================

# =========================================================
# FINAL PREFERENCE-BASED CROP RECOMMENDATION
# =========================================================

def get_crop_recommendation(crop, soil, season, water):

    crop = (crop or "").lower()
    soil = (soil or "").lower()
    season = (season or "").lower()
    water = (water or "").lower()

    crop_catalog = {
        "rice": ("Nitrogen, phosphorus and potassium fertilizer", "High water requirement", "Maintain standing water carefully and monitor pests.", ["clay", "loamy"], ["kharif"], ["high"]),
        "wheat": ("Nitrogen-rich fertilizer with balanced nutrients", "Moderate water requirement", "Avoid excessive irrigation and monitor soil moisture.", ["loamy", "clay"], ["rabi"], ["medium"]),
        "maize": ("Nitrogen and phosphorus fertilizer", "Moderate water requirement", "Maintain moisture during flowering and grain formation.", ["loamy", "sandy"], ["kharif", "rabi"], ["medium"]),
        "tomato": ("Balanced NPK fertilizer with compost", "Regular moderate irrigation", "Use good drainage and monitor for fungal disease.", ["loamy", "sandy"], ["kharif", "rabi", "zaid"], ["medium"]),
        "cotton": ("Nitrogen, phosphorus and potassium fertilizer", "Moderate water requirement", "Monitor pests and keep the root zone well drained.", ["black", "loamy"], ["kharif"], ["medium"]),
        "groundnut": ("Phosphorus, calcium and gypsum based nutrition", "Low to moderate water requirement", "Avoid waterlogging and keep soil loose for pods.", ["sandy", "loamy"], ["kharif", "rabi"], ["low", "medium"]),
        "millet": ("Balanced fertilizer with organic matter", "Low water requirement", "A drought-tolerant choice for low rainfall areas.", ["sandy", "loamy"], ["kharif"], ["low"]),
        "chickpea": ("Phosphorus-rich fertilizer with inoculated seed", "Low water requirement", "Avoid excess irrigation during flowering and pod filling.", ["sandy", "loamy"], ["rabi"], ["low"]),
        "pigeon_pea": ("Balanced fertilizer with phosphorus", "Low to moderate water requirement", "Use well-drained soil and control weeds early.", ["loamy", "black"], ["kharif"], ["low", "medium"]),
        "sorghum": ("Nitrogen and phosphorus fertilizer", "Low to moderate water requirement", "Suitable for warm areas with uncertain rainfall.", ["sandy", "loamy"], ["kharif", "rabi"], ["low", "medium"]),
        "sugarcane": ("Nitrogen-rich fertilizer with potassium", "High water requirement", "Plan irrigation and drainage because this is a long-duration crop.", ["loamy", "clay"], ["kharif", "zaid"], ["high"]),
        "potato": ("Balanced NPK fertilizer with potassium", "Moderate water requirement", "Use loose soil and avoid irrigation immediately before harvest.", ["sandy", "loamy"], ["rabi"], ["medium"]),
        "onion": ("Nitrogen and potassium fertilizer", "Moderate water requirement", "Keep irrigation uniform and stop watering before harvest.", ["sandy", "loamy"], ["rabi", "zaid"], ["medium"]),
        "soybean": ("Phosphorus and potassium with inoculated seed", "Moderate water requirement", "Avoid standing water and use disease-free seed.", ["loamy", "black"], ["kharif"], ["medium"]),
        "banana": ("Nitrogen and potassium-rich fertilizer", "High water requirement", "Provide regular irrigation, mulch and wind protection.", ["loamy", "clay"], ["kharif", "zaid"], ["high"]),
    }

    scored = []
    for name, details in crop_catalog.items():
        fertilizer, irrigation, advice, soils, seasons, waters = details
        score = (3 if soil in soils else 0) + (3 if season in seasons else 0) + (3 if water in waters else 0)
        score += 2 if crop and crop == name else 0
        scored.append((score, name, fertilizer, irrigation, advice))

    scored.sort(reverse=True)
    _, selected, fertilizer, irrigation, advice = scored[0]

    if soil == "sandy":
        soil_advice = "Sandy soil drains quickly. Add organic matter and monitor moisture frequently."
    elif soil == "clay":
        soil_advice = "Clay soil holds water. Avoid over-irrigation and improve drainage."
    elif soil == "loamy":
        soil_advice = "Loamy soil is generally suitable for many crops."
    else:
        soil_advice = "Consider soil testing for a more accurate recommendation."

    water_advice = {
        "low": "Use water-saving irrigation such as drip irrigation.",
        "medium": "Use scheduled irrigation and monitor soil moisture.",
        "high": "Maintain efficient irrigation and avoid unnecessary water use.",
    }.get(water, "Maintain efficient irrigation and avoid unnecessary water use.")

    return {
        "crop": selected.replace("_", " ").title(),
        "fertilizer": fertilizer,
        "irrigation": irrigation,
        "soil_advice": soil_advice,
        "water_advice": water_advice,
        "advice": advice,
        "alternatives": ", ".join(item[1].replace("_", " ").title() for item in scored[1:4]),
    }


# =========================================================
# IRRIGATION PAGE
# =========================================================

@app.route("/irrigation")
def irrigation():

    if not check_login():
        return redirect("/")

    return render_template(
        "irrigation.html",
        username=session["username"]
    )


# =========================================================
# IRRIGATION CALCULATION
# =========================================================

@app.route(
    "/irrigation-calculate",
    methods=["POST"]
)
def irrigation_calculate():

    if not check_login():
        return redirect("/")

    crop = request.form.get("crop")

    area = float(
        request.form.get(
            "area",
            0
        )
    )

    temperature = float(
        request.form.get(
            "temperature",
            0
        )
    )

    moisture = float(
        request.form.get(
            "moisture",
            0
        )
    )

    if moisture < 30:

        status = "Irrigation Required"

        water = area * 2500

    elif moisture < 50:

        status = "Moderate Irrigation Required"

        water = area * 1500

    else:

        status = "No Immediate Irrigation Required"

        water = 0

    # Temperature adjustment

    if temperature >= 35:

        water *= 1.20

        advice = (
            "High temperature detected. Monitor soil moisture frequently."
        )

    elif temperature >= 30:

        water *= 1.10

        advice = (
            "Warm conditions detected. Regular soil moisture monitoring is recommended."
        )

    else:

        advice = (
            "Temperature is moderate. Maintain normal irrigation scheduling."
        )

    return render_template(
        "irrigation_result.html",
        username=session["username"],
        crop=crop,
        area=area,
        temperature=temperature,
        moisture=moisture,
        status=status,
        water=round(water, 2),
        advice=advice
    )


# =========================================================
# DISEASE DETECTION PAGE
# =========================================================

@app.route("/disease-detection")
def disease_detection():

    if not check_login():
        return redirect("/")

    return render_template(
        "feature.html",
        title="Crop Disease Detection",
        icon="🦠",
        description="Identify possible crop diseases and get farming guidance.",
        username=session["username"]
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

# IMPORTANT:
# Replace YOUR_GEMINI_API_KEY with your Gemini API key.
# DO NOT SHARE YOUR REAL KEY IN CHAT.

# =========================================================
# GEMINI CLIENT
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured in .env")

ai_client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# DISEASE CHECK
# =========================================================

@app.route(
    "/disease-check",
    methods=["POST"]
)
def disease_check():

    if not check_login():

        return {

            "disease":
                "Login Required",

            "message":
                "Please login first.",

            "confidence":
                "--",

            "health":
                "--",

            "treatment":
                "Login to use disease detection."
        }

    image = request.files.get(
        "crop_image"
    )

    if not image:

        return {

            "disease":
                "No Image",

            "message":
                "Please upload an image.",

            "confidence":
                "--",

            "health":
                "--",

            "treatment":
                "Upload an image and try again."
        }

    try:

        image_bytes = image.read()

        mime_type = (
            image.content_type
            or "image/jpeg"
        )

        prompt = (

            "Analyze this image for an agricultural app. "

            "First determine whether the image clearly shows a plant, "
            "leaf, fruit, crop or agricultural plant. "

            "If the image is NOT a plant, return exactly: "

            "Disease: Not a Plant ❌ | "
            "Confidence: 100% | "
            "Health: Invalid | "
            "Message: The uploaded image is not a plant. | "
            "Treatment: Please upload a valid crop image. "

            "If it is a plant, identify whether it appears healthy "
            "or affected by a disease. "

            "Return strictly using this format: "

            "Disease: [Disease name or Healthy Crop 🌱] | "
            "Confidence: [percentage] | "
            "Health: [Healthy / Diseased] | "
            "Message: [Short summary] | "
            "Treatment: [Recommended action]"
        )

        response = ai_client.models.generate_content(

            model="gemini-3.6-flash",

            contents=[

                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type
                ),

                prompt
            ]
        )

        ai_text = response.text

        parts = ai_text.split("|")

        disease_val = (

            parts[0]
            .replace(
                "Disease:",
                ""
            )
            .strip()

            if len(parts) > 0

            else "Analysis Complete"
        )

        conf_val = (

            parts[1]
            .replace(
                "Confidence:",
                ""
            )
            .strip()

            if len(parts) > 1

            else "90%"
        )

        health_val = (

            parts[2]
            .replace(
                "Health:",
                ""
            )
            .strip()

            if len(parts) > 2

            else "Unknown"
        )

        msg_val = (

            parts[3]
            .replace(
                "Message:",
                ""
            )
            .strip()

            if len(parts) > 3

            else "Image processed successfully."
        )

        treat_val = (

            parts[4]
            .replace(
                "Treatment:",
                ""
            )
            .strip()

            if len(parts) > 4

            else "Please upload a valid crop image."
        )

        return {

            "disease":
                disease_val,

            "message":
                msg_val,

            "confidence":
                conf_val,

            "health":
                health_val,

            "treatment":
                treat_val
        }

    except Exception as e:

        print(
            "DISEASE ERROR:",
            str(e)
        )

        return {

            "disease":
                "Analysis Error",

            "message":
                f"Could not process image: {str(e)}",

            "confidence":
                "0%",

            "health":
                "Error",

            "treatment":
                "Please upload a valid crop image."
        }


# =========================================================
# MARKET PRICES PAGE
# =========================================================

@app.route("/market-prices")
def market_prices():

    if not check_login():
        return redirect("/")

    return render_template(
        "feature.html",
        title="Market Prices",
        icon="📈",
        description="Check crop market information and make better selling decisions.",
        username=session["username"]
    )


# =========================================================
# MARKET PRICES API
# =========================================================
#
# IMPORTANT:
#
# The function below MUST be called:
#
#     api_market_prices
#
# NOT market_prices
#
# Otherwise Flask gives:
#
# AssertionError:
# View function mapping is overwriting an existing endpoint
#
# =========================================================
@app.route("/api/market-prices")
def api_market_prices():
    import os

    # --------------------------------------------------
    # DEMO DATA
    # --------------------------------------------------
    # These are ONLY for project demonstration.
    # They are NOT Government of India prices.
    # --------------------------------------------------

    demo_data = {
        "rice": [
            {
                "market": "Chennai",
                "min_price": 2100,
                "max_price": 2400,
                "modal_price": 2250,
                "date": ""
            }
        ],
        "wheat": [
            {
                "market": "Chennai",
                "min_price": 2300,
                "max_price": 2600,
                "modal_price": 2450,
                "date": ""
            }
        ],
        "maize": [
            {
                "market": "Chennai",
                "min_price": 1800,
                "max_price": 2200,
                "modal_price": 2000,
                "date": ""
            }
        ],
        "tomato": [
            {
                "market": "Chennai",
                "min_price": 1200,
                "max_price": 1800,
                "modal_price": 1500,
                "date": ""
            }
        ],
        "cotton": [
            {
                "market": "Chennai",
                "min_price": 6200,
                "max_price": 7200,
                "modal_price": 6700,
                "date": ""
            }
        ],
        "groundnut": [
            {
                "market": "Chennai",
                "min_price": 5000,
                "max_price": 5600,
                "modal_price": 5300,
                "date": ""
            }
        ]
    }

    try:
        # --------------------------------------------------
        # GET GOVERNMENT API KEY
        # --------------------------------------------------

        api_key = os.environ.get("DATA_GOV_IN_API_KEY", "").strip()

        if not api_key:
            print("WARNING: DATA_GOV_IN_API_KEY not found.")
            print("USING DEMO MARKET DATA.")
            return jsonify({
                "success": True,
                "demo": True,
                "source": "Sample fallback data",
                "message": (
                    "Government API key not configured. "
                    "Showing sample fallback data. Add DATA_GOV_IN_API_KEY for live prices."
                ),
                "data": demo_data
            })

        # --------------------------------------------------
        # GOVERNMENT OF INDIA DATASET
        # --------------------------------------------------

        resource_id = "35985678-0d79-46b4-9ed6-6f13308a1d24"
        url = "https://api.data.gov.in/resource/" + resource_id

        params = {
            "api-key": api_key,
            "format": "json",
            "limit": 1000
        }

        print("REQUESTING GOVERNMENT MARKET DATA...")

        response = requests.get(url, params=params, timeout=30)
        print("DATA.GOV.IN STATUS:", response.status_code)

        if response.status_code != 200:
            print("Government API failed.")
            print("USING DEMO MARKET DATA.")
            return jsonify({
                "success": True,
                "demo": True,
                "source": "Demo Data",
                "message": (
                    "Government market service is temporarily unavailable. "
                    "Showing demo data."
                ),
                "data": demo_data
            })

        # --------------------------------------------------
        # READ GOVERNMENT RESPONSE
        # --------------------------------------------------

        result = response.json()
        records = result.get("records", [])
        print("TOTAL GOVERNMENT RECORDS:", len(records))

        # --------------------------------------------------
        # PREPARE CROP DATA
        # --------------------------------------------------

        market_data = {
            "rice": [],
            "wheat": [],
            "maize": [],
            "tomato": [],
            "cotton": [],
            "groundnut": []
        }

        # --------------------------------------------------
        # PROCESS RECORDS
        # --------------------------------------------------

        for record in records:
            commodity = str(record.get("commodity", "")).strip().lower()

            item = {
                "market": record.get("market", "--"),
                "min_price": record.get("min_price", "--"),
                "max_price": record.get("max_price", "--"),
                "modal_price": record.get("modal_price", "--"),
                "date": record.get("arrival_date", "--")
            }

            if "rice" in commodity or "paddy" in commodity:
                market_data["rice"].append(item)
            elif "wheat" in commodity:
                market_data["wheat"].append(item)
            elif "maize" in commodity or "corn" in commodity:
                market_data["maize"].append(item)
            elif "tomato" in commodity:
                market_data["tomato"].append(item)
            elif "cotton" in commodity:
                market_data["cotton"].append(item)
            elif "groundnut" in commodity or "peanut" in commodity:
                market_data["groundnut"].append(item)

        def market_date_key(item):
            value = str(item.get("date", ""))
            for date_format in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, date_format)
                except ValueError:
                    continue
            return datetime.min

        for crop, items in market_data.items():
            items.sort(key=market_date_key, reverse=True)
            if not items:
                continue

            latest = items[0]
            latest_date = latest.get("date")
            previous = next(
                (item for item in items if item.get("date") != latest_date),
                None
            )

            try:
                current_price = float(str(latest.get("modal_price", "")).replace(",", ""))
                previous_price = float(str(previous.get("modal_price", "")).replace(",", "")) if previous else None
            except (TypeError, ValueError):
                current_price = None
                previous_price = None

            latest["previous_modal_price"] = previous_price
            latest["change_percent"] = (
                round(((current_price - previous_price) / previous_price) * 100, 2)
                if current_price is not None and previous_price not in (None, 0)
                else None
            )

        print("RICE RECORDS:", len(market_data["rice"]))
        print("WHEAT RECORDS:", len(market_data["wheat"]))
        print("MAIZE RECORDS:", len(market_data["maize"]))
        print("TOMATO RECORDS:", len(market_data["tomato"]))
        print("COTTON RECORDS:", len(market_data["cotton"]))
        print("GROUNDNUT RECORDS:", len(market_data["groundnut"]))

        total_records = sum(len(items) for items in market_data.values())

        if total_records == 0:
            print("Government API returned no matching crop records.")
            print("USING DEMO MARKET DATA.")
            return jsonify({
                "success": True,
                "demo": True,
                "source": "Demo Data",
                "message": (
                    "No matching Government market records were returned. "
                    "Showing demo data."
                ),
                "data": demo_data
            })

        # --------------------------------------------------
        # FILL MISSING CROPS WITH DEMO DATA
        # --------------------------------------------------

        missing_crops = []

        for crop in market_data:
            if len(market_data[crop]) == 0:
                market_data[crop] = demo_data.get(crop, [])
                missing_crops.append(crop)
                print(crop.upper(), "NOT AVAILABLE FROM GOVERNMENT API.")
                print("USING DEMO DATA FOR", crop.upper())

        if missing_crops:
            print("SOME CROPS WERE NOT AVAILABLE.")
            print("USING DEMO DATA FOR:", missing_crops)
            return jsonify({
                "success": True,
                "demo": True,
                "source": "Government of India + Demo Data",
                "message": (
                    "Government data loaded where available. "
                    "Demo data used for unavailable crops."
                ),
                "data": market_data
            })

        print("USING REAL GOVERNMENT MARKET DATA.")
        return jsonify({
            "success": True,
            "demo": False,
            "source": "Government of India - Agmarknet",
            "message": (
                "Market data successfully loaded from Government of India."
            ),
            "data": market_data
        })

    # ------------------------------------------------------
    # TIMEOUT
    # ------------------------------------------------------

    except requests.exceptions.Timeout:
        print("ERROR: DATA.GOV.IN REQUEST TIMED OUT")
        print("USING DEMO MARKET DATA.")
        return jsonify({
            "success": True,
            "demo": True,
            "source": "Demo Data",
            "message": "Government market API timed out. Showing demo data.",
            "data": demo_data
        })

    # ------------------------------------------------------
    # CONNECTION ERROR
    # ------------------------------------------------------

    except requests.exceptions.RequestException as e:
        print("REQUEST ERROR:", str(e))
        print("USING DEMO MARKET DATA.")
        return jsonify({
            "success": True,
            "demo": True,
            "source": "Demo Data",
            "message": (
                "Government market service could not be reached. Showing demo data."
            ),
            "data": demo_data
        })

    # ------------------------------------------------------
    # JSON ERROR
    # ------------------------------------------------------

    except ValueError as e:
        print("JSON ERROR:", str(e))
        return jsonify({
            "success": True,
            "demo": True,
            "source": "Demo Data",
            "message": "Government API returned invalid data. Showing demo data.",
            "data": demo_data
        })

    # ------------------------------------------------------
    # UNEXPECTED ERROR
    # ------------------------------------------------------

    except Exception as e:
        print("MARKET ERROR:", str(e))
        print("USING DEMO MARKET DATA.")
        return jsonify({
            "success": True,
            "demo": True,
            "source": "Demo Data",
            "message": "Market service is temporarily unavailable. Showing demo data.",
            "data": demo_data
        })
# =========================================================
# GOVERNMENT SCHEMES
# =========================================================

@app.route("/government-schemes")
def government_schemes():

    if not check_login():
        return redirect("/")

    return render_template(
        "feature.html",
        title="Government Schemes",
        icon="🏛️",
        description="Find useful government schemes and financial support available for farmers.",
        username=session["username"]
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if not check_login():
        return redirect("/")

    return render_template(
        "feature.html",
        title="My Profile",
        icon="👨‍🌾",
        description="View and manage your Smart Farmer profile.",
        username=session["username"]
    )


# =========================================================
# SETTINGS
# =========================================================

@app.route("/settings")
def settings():

    if not check_login():
        return redirect("/")

    return render_template(
        "feature.html",
        title="Settings",
        icon="⚙️",
        description="Manage your Smart Farmer Assistance settings.",
        username=session["username"]
    )


# =========================================================
# CHANGE PASSWORD
# =========================================================
# =========================================================
# CHANGE PASSWORD
# =========================================================

@app.route(
    "/change-password",
    methods=["POST"]
)
def change_password():

    if not check_login():

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    try:

        # -------------------------------------------------
        # GET PASSWORD DATA
        # -------------------------------------------------

        if request.is_json:

            data = request.get_json()

            current_password = data.get(
                "current_password",
                ""
            )

            new_password = data.get(
                "new_password",
                ""
            )

        else:

            current_password = request.form.get(
                "current_password",
                ""
            )

            new_password = request.form.get(
                "new_password",
                ""
            )


        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not current_password:

            return jsonify({
                "success": False,
                "message": "Current password is required."
            }), 400


        if not new_password:

            return jsonify({
                "success": False,
                "message": "New password is required."
            }), 400


        if len(new_password) < 6:

            return jsonify({
                "success": False,
                "message": (
                    "New password must contain "
                    "at least 6 characters."
                )
            }), 400


        if current_password == new_password:

            return jsonify({
                "success": False,
                "message": (
                    "New password must be different "
                    "from your current password."
                )
            }), 400


        # -------------------------------------------------
        # GET LOGGED-IN USER
        # -------------------------------------------------

        connection = get_db()

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE id = ?
            """,
            (session["user_id"],)
        ).fetchone()


        if not user:

            connection.close()

            return jsonify({
                "success": False,
                "message": "User account not found."
            }), 404


        # -------------------------------------------------
        # CHECK CURRENT PASSWORD
        # -------------------------------------------------

        if not check_password_hash(
            user["password"],
            current_password
        ):

            connection.close()

            return jsonify({
                "success": False,
                "message": "Incorrect current password."
            }), 401


        # -------------------------------------------------
        # CREATE NEW PASSWORD HASH
        # -------------------------------------------------

        new_hashed_password = (
            generate_password_hash(
                new_password
            )
        )


        # -------------------------------------------------
        # UPDATE SQLITE DATABASE
        # -------------------------------------------------

        connection.execute(
            """
            UPDATE users
            SET password = ?
            WHERE id = ?
            """,
            (
                new_hashed_password,
                session["user_id"]
            )
        )

        connection.commit()
        connection.close()


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        print(
            "PASSWORD UPDATED FOR USER:",
            session["username"]
        )

        return jsonify({

            "success": True,

            "message":
                "Password changed successfully."

        })


    except Exception as e:

        print(
            "CHANGE PASSWORD ERROR:",
            str(e)
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to change password."

        }), 500

# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    create_database()

    app.run(
        debug=True
    )