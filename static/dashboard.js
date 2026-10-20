
/* =========================================
   PROFILE MANAGEMENT
========================================= */

function openProfile() {
    const modal = document.getElementById("profileModal");

    if (!modal) {
        console.error("Profile modal not found!");
        return;
    }

    // Load saved profile details into the form
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

function closeProfile() {
    const modal = document.getElementById("profileModal");

    if (modal) {
        modal.style.display = "none";
    }
}

/* =========================================
   UPDATE DASHBOARD FROM SAVED PROFILE
========================================= */

function updateProfileDisplay() {
    const name = localStorage.getItem("farmerName") || "";
    const phone = localStorage.getItem("farmerPhone") || "";
    const location = localStorage.getItem("farmerLocation") || "";
    const crop = localStorage.getItem("farmerCrop") || "";

    const displayName = document.getElementById("displayName");
    const displayInfo = document.getElementById("displayInfo");

    if (displayName) {
        displayName.textContent = name
            ? "Welcome, " + name
            : "Welcome, Farmer";
    }

    if (displayInfo) {
        const details = [];

        if (location) details.push("📍 " + location);
        if (crop) details.push("🌾 " + crop);
        if (phone) details.push("📞 " + phone);

        displayInfo.textContent = details.join(" | ");
    }

    // Also update the profile form, if it exists
    const nameInput = document.getElementById("farmerName");

    if (nameInput && name) {
        nameInput.value = name;
    }
}

/* =========================================
   SAVE PROFILE
========================================= */

function initializeProfile() {
    const profileForm = document.getElementById("profileForm");

    if (profileForm && !profileForm.dataset.profileHandlerAdded) {
        profileForm.dataset.profileHandlerAdded = "true";

        profileForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const name =
                document.getElementById("farmerName").value.trim();

            const phone =
                document.getElementById("farmerPhone").value.trim();

            const location =
                document.getElementById("farmerLocation").value.trim();

            const crop =
                document.getElementById("farmerCrop").value.trim();

            if (!name) {
                alert("Please enter your name.");
                return;
            }

            // Save the values entered in the profile form
            localStorage.setItem("farmerName", name);
            localStorage.setItem("farmerPhone", phone);
            localStorage.setItem("farmerLocation", location);
            localStorage.setItem("farmerCrop", crop);

            // Immediately refresh the dashboard display
            updateProfileDisplay();

            closeProfile();

            alert("Profile updated successfully!");
        });
    }

    // Display the saved profile when the page opens
    updateProfileDisplay();
}

// Run whether this script loads before or after page initialization
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeProfile);
} else {
    initializeProfile();
}

/* =========================================
   CLOSE PROFILE WHEN CLICKING OUTSIDE
========================================= */

window.addEventListener("click", function (event) {
    const modal = document.getElementById("profileModal");

    if (modal && event.target === modal) {
        closeProfile();
    }
});
