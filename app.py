from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Secret key for login sessions
app.secret_key = "smart-farmer-secret-key"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


# ==========================================
# CREATE DATABASE
# ==========================================

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


# ==========================================
# HOME / LOGIN PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# LOGIN
# ==========================================

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


# ==========================================
# LOGIN CHECK
# ==========================================

def check_login():

    if "user_id" not in session:
        return False

    return True


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if not check_login():
        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# ==========================================
# WEATHER
# ==========================================

@app.route("/weather")
def weather():

    if not check_login():
        return redirect("/")

    return render_template(
        "feature.html",
        title="Smart Weather",
        icon="🌦️",
        description="Stay updated with weather conditions for better farming decisions.",
        username=session["username"]
    )


# ==========================================
# CROP ASSISTANCE
# ==========================================

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


# ==========================================
# IRRIGATION PAGE
# ==========================================

@app.route("/irrigation")
def irrigation():

    if not check_login():
        return redirect("/")

    return render_template(
        "irrigation.html",
        username=session["username"]
    )


# ==========================================
# IRRIGATION CALCULATION
# ==========================================

@app.route("/irrigation-calculate", methods=["POST"])
def irrigation_calculate():

    if not check_login():
        return redirect("/")

    crop = request.form.get("crop")
    area = float(request.form.get("area"))
    temperature = float(request.form.get("temperature"))
    moisture = float(request.form.get("moisture"))

    # Basic irrigation calculation

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

        water = water * 1.20

        advice = "High temperature detected. Monitor soil moisture frequently."

    elif temperature >= 30:

        water = water * 1.10

        advice = "Warm conditions detected. Regular soil moisture monitoring is recommended."

    else:

        advice = "Temperature is moderate. Maintain normal irrigation scheduling."

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


# ==========================================
# DISEASE DETECTION
# ==========================================

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
# ==========================================
# DISEASE ANALYSIS
# ==========================================

@app.route("/disease-check", methods=["POST"])
def disease_check():

    if not check_login():

        return {
            "disease": "Login Required",
            "message": "Please login first.",
            "confidence": "--",
            "health": "--",
            "treatment": "Login to use disease detection."
        }


    image = request.files.get("crop_image")


    if not image:

        return {
            "disease": "No Image",
            "message": "Please upload a crop image.",
            "confidence": "--",
            "health": "--",
            "treatment": "Upload an image and try again."
        }


    # --------------------------------------
    # TEMPORARY DEMO RESULT
    # --------------------------------------

    return {
        "disease": "Healthy Crop 🌱",

        "message":
            "The uploaded crop image is ready for analysis.",

        "confidence":
            "92%",

        "health":
            "Healthy",

        "treatment":
            "Continue regular irrigation, monitor the crop regularly and maintain proper nutrition."
    }


# ==========================================
# MARKET PRICES
# ==========================================

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


# ==========================================
# GOVERNMENT SCHEMES
# ==========================================

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


# ==========================================
# MY PROFILE
# ==========================================

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


# ==========================================
# SETTINGS
# ==========================================

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
# ==========================================
# CROP ASSISTANCE
# ==========================================

@app.route("/crop-recommendation", methods=["POST"])
def crop_recommendation():

    if "user_id" not in session:
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


# ==========================================
# CROP RECOMMENDATION LOGIC
# ==========================================

def get_crop_recommendation(crop, soil, season, water):

    crop = crop.lower()
    soil = soil.lower()
    season = season.lower()
    water = water.lower()

    result = {}

    if crop == "rice":

        result["crop"] = "Rice"
        result["fertilizer"] = "Nitrogen, Phosphorus and Potassium based fertilizer"
        result["irrigation"] = "High water requirement"
        result["advice"] = "Maintain adequate water levels and monitor pests regularly."

    elif crop == "wheat":

        result["crop"] = "Wheat"
        result["fertilizer"] = "Nitrogen-rich fertilizer with balanced nutrients"
        result["irrigation"] = "Moderate water requirement"
        result["advice"] = "Avoid excessive irrigation and monitor soil moisture."

    elif crop == "maize":

        result["crop"] = "Maize"
        result["fertilizer"] = "Nitrogen and phosphorus fertilizer"
        result["irrigation"] = "Moderate water requirement"
        result["advice"] = "Maintain proper soil moisture during important growth stages."

    elif crop == "tomato":

        result["crop"] = "Tomato"
        result["fertilizer"] = "Balanced NPK fertilizer"
        result["irrigation"] = "Regular moderate irrigation"
        result["advice"] = "Monitor for fungal diseases and maintain proper drainage."

    elif crop == "cotton":

        result["crop"] = "Cotton"
        result["fertilizer"] = "Nitrogen, phosphorus and potassium fertilizer"
        result["irrigation"] = "Moderate water requirement"
        result["advice"] = "Monitor closely for pests and maintain good soil drainage."

    else:

        result["crop"] = crop.title()
        result["fertilizer"] = "Use a balanced fertilizer based on soil testing."
        result["irrigation"] = "Maintain irrigation according to soil moisture."
        result["advice"] = "Consult local agricultural experts for crop-specific guidance."

    # Soil advice

    if soil == "sandy":

        result["soil_advice"] = "Sandy soil drains quickly. Use organic matter and monitor moisture frequently."

    elif soil == "clay":

        result["soil_advice"] = "Clay soil holds water. Avoid over-irrigation and improve drainage."

    elif soil == "loamy":

        result["soil_advice"] = "Loamy soil is generally suitable for many crops."

    else:

        result["soil_advice"] = "Consider soil testing for better recommendations."

    # Water advice

    if water == "low":

        result["water_advice"] = "Use water-saving irrigation methods such as drip irrigation."

    elif water == "medium":

        result["water_advice"] = "Use scheduled irrigation and regularly monitor soil moisture."

    else:

        result["water_advice"] = "Maintain efficient irrigation and avoid unnecessary water usage."

    return result
# ==========================================
# IRRIGATION
# ==========================================

# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")



# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)