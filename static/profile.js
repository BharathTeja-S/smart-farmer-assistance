// =====================================================
// SMART FARMER - PROFILE MANAGEMENT
// =====================================================

// OPEN PROFILE
function openProfile() {
    const modal = document.getElementById("profileModal");

    if (!modal) {
        console.error("Profile modal not found!");
        return;
    }

    document.getElementById("farmerName").value =
        localStorage.getItem("farmerName") || "";

    document.getElementById("farmerPhone").value =
        localStorage.getItem("farmerPhone") || "";

    document.getElementById("farmerLocation").value =
        localStorage.getItem("farmerLocation") || "";

    document.getElementById("farmerCrop").value =
        localStorage.getItem("farmerCrop") || "";

    modal.style.display = "flex";
}

// CLOSE PROFILE
function closeProfile() {
    const modal = document.getElementById("profileModal");

    if (modal) {
        modal.style.display = "none";
    }
}

// UPDATE ALL PROFILE DISPLAYS
function updateProfileDisplay() {
    const name = localStorage.getItem("farmerName") || "";
    const phone = localStorage.getItem("farmerPhone") || "";
    const location = localStorage.getItem("farmerLocation") || "";
    const crop = localStorage.getItem("farmerCrop") || "";

    const displayName = document.getElementById("displayName");
    const displayInfo = document.getElementById("displayInfo");
    const topGreeting = document.getElementById("topGreeting");
    const profileName = document.querySelector(".profile strong");

    if (displayName) {
        displayName.textContent = name
            ? "Welcome, " + name
            : "Welcome, Farmer";
    }

    if (topGreeting) {
        topGreeting.textContent = name
            ? "Good Evening, " + name + "! 👋"
            : "Good Evening, Farmer! 👋";
    }

    if (profileName) {
        profileName.textContent = name || "Farmer";
    }

    if (displayInfo) {
        const details = [];

        if (location) details.push("📍 " + location);
        if (crop) details.push("🌾 " + crop);
        if (phone) details.push("📞 " + phone);

        displayInfo.textContent = details.join(" | ");
    }
}

// INITIALIZE PROFILE
function initializeProfile() {
    console.log("PROFILE.JS LOADED");

    const form = document.getElementById("profileForm");
    const dateElement = document.getElementById("currentDate");

    // Display current date
    if (dateElement) {
        dateElement.textContent = new Date()
            .toLocaleDateString("en-US", {
                weekday: "long",
                month: "long",
                day: "numeric",
                year: "numeric"
            })
            .toUpperCase();
    }

    // Show previously saved profile
    updateProfileDisplay();

    if (!form) {
        console.error("Profile form not found!");
        return;
    }

    // Prevent duplicate event listeners
    if (form.dataset.profileHandlerAdded === "true") {
        return;
    }

    form.dataset.profileHandlerAdded = "true";

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const name =
            document.getElementById("farmerName").value.trim();

        const phone =
            document.getElementById("farmerPhone").value.trim();

        const location =
            document.getElementById("farmerLocation").value.trim();

        const crop =
            document.getElementById("farmerCrop").value.trim();

        if (!name || !phone || !location) {
            alert("Please fill all required details.");
            return;
        }

        // Save all profile fields
        localStorage.setItem("farmerName", name);
        localStorage.setItem("farmerPhone", phone);
        localStorage.setItem("farmerLocation", location);
        localStorage.setItem("farmerCrop", crop);

        // Refresh the dashboard
        updateProfileDisplay();

        closeProfile();

        alert("Profile saved successfully!");
    });
}

// RUN AFTER HTML IS READY
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeProfile);
} else {
    initializeProfile();
}

// CLOSE MODAL WHEN CLICKING OUTSIDE
window.addEventListener("click", function (event) {
    const modal = document.getElementById("profileModal");

    if (modal && event.target === modal) {
        closeProfile();
    }
});
