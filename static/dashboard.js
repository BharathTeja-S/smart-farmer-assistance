

function openScheme(scheme) {

    const modal =
        document.getElementById("schemeModal");

    const content =
        document.getElementById("schemeContent");


    if (scheme === "pmkisan") {

        content.innerHTML = `

            <h2>🇮🇳 PM-KISAN</h2>

            <p>
                <strong>
                Pradhan Mantri Kisan Samman Nidhi
                </strong>
            </p>

            <p>
                PM-KISAN is an income support scheme
                for eligible landholding farmer families.
            </p>

            <p>
                💰 <strong>Benefit:</strong>
                ₹6,000 per year in three equal
                installments of ₹2,000.
            </p>

            <p>
                💳 The amount is transferred directly
                to the beneficiary's bank account
                through Direct Benefit Transfer.
            </p>

            <p>
                🔐 eKYC is mandatory for registered
                PM-KISAN farmers.
            </p>

            <a
                href="https://www.pmkisan.gov.in/"
                target="_blank">

                Visit Official PM-KISAN Website →

            </a>

        `;
    }


    else if (scheme === "pmfby") {

        content.innerHTML = `

            <h2>🛡️ PMFBY</h2>

            <p>
                <strong>
                Pradhan Mantri Fasal Bima Yojana
                </strong>
            </p>

            <p>
                A crop insurance scheme designed
                to provide financial support to
                farmers in case of crop losses.
            </p>

            <p>
                🌾 Farmers can learn about coverage,
                eligibility and enrollment through
                the official government resources.
            </p>

            <a
                href="https://www.myscheme.gov.in/"
                target="_blank">

                Visit myScheme →

            </a>

        `;
    }


    else if (scheme === "kcc") {

        content.innerHTML = `

            <h2>💳 Kisan Credit Card</h2>

            <p>
                Kisan Credit Card (KCC) provides
                agricultural credit facilities
                to eligible farmers.
            </p>

            <p>
                Farmers can use the facility to
                meet agricultural and related
                financial requirements, subject
                to applicable rules.
            </p>

            <a
                href="https://www.myscheme.gov.in/"
                target="_blank">

                Explore Government Schemes →

            </a>

        `;
    }


    modal.style.display = "flex";
}



// =====================================
// CLOSE POPUP
// =====================================

function closeScheme() {

    document.getElementById("schemeModal")
        .style.display = "none";

}


// Close when clicking outside

window.addEventListener("click", function(event) {

    const modal =
        document.getElementById("schemeModal");

    if (event.target === modal) {

        closeScheme();

    }

});



// =====================================
// SIDEBAR ACTIVE ITEM
// =====================================

const menuItems =
    document.querySelectorAll(".menu");


menuItems.forEach(item => {

    item.addEventListener("click", function() {

        menuItems.forEach(menu => {

            menu.classList.remove("active");

        });

        if (
            this.getAttribute("href") !== "index.html"
        ) {

            this.classList.add("active");

        }

    });

});
// =========================================
// CROP DISEASE DETECTION
// =========================================

const diseaseForm = document.getElementById("diseaseForm");

const cropImage = document.getElementById("cropImage");

const imagePreview = document.getElementById("imagePreview");


/* IMAGE PREVIEW */

if (cropImage) {

    cropImage.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) {
            imagePreview.innerHTML = "";
            return;
        }

        const imageURL = URL.createObjectURL(file);

        imagePreview.innerHTML = `
            <img src="${imageURL}" alt="Crop Preview">
        `;

    });

}


/* DISEASE FORM */

if (diseaseForm) {

    diseaseForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const file = cropImage.files[0];

        if (!file) {

            alert("Please upload a crop image.");

            return;
        }


        const formData = new FormData();

        formData.append("crop_image", file);


        document.getElementById("diseaseName").innerText =
            "Analyzing... 🔍";

        document.getElementById("diseaseMessage").innerText =
            "Please wait while we analyze the crop image.";

        document.getElementById("confidence").innerText =
            "...";

        document.getElementById("cropHealth").innerText =
            "...";

        document.getElementById("treatment").innerText =
            "Analyzing crop condition...";


        try {

            const response = await fetch(
                "/disease-check",
                {
                    method: "POST",
                    body: formData
                }
            );


            const data = await response.json();


            document.getElementById("diseaseName").innerText =
                data.disease;

            document.getElementById("diseaseMessage").innerText =
                data.message;

            document.getElementById("confidence").innerText =
                data.confidence;

            document.getElementById("cropHealth").innerText =
                data.health;

            document.getElementById("treatment").innerText =
                data.treatment;


        } catch (error) {

            console.error(error);

            document.getElementById("diseaseName").innerText =
                "Analysis Error";

            document.getElementById("diseaseMessage").innerText =
                "Unable to analyze the image.";

        }

    });

}
// =====================================================
// SETTINGS
// =====================================================


// SHOW SETTINGS MESSAGE

function showSettingMessage(message) {

    const box =
        document.getElementById("settingsMessage");

    const text =
        document.getElementById("settingsMessageText");


    if (!box || !text) {
        return;
    }


    text.innerText = message;

    box.style.display = "block";


    setTimeout(function () {

        box.style.display = "none";

    }, 3000);

}



// =====================================================
// NOTIFICATION TOGGLE
// =====================================================

function toggleNotifications() {

    const toggle =
        document.getElementById("notificationToggle");

    const status =
        document.getElementById("notificationStatus");


    if (!toggle || !status) {
        return;
    }


    if (toggle.checked) {

        status.innerText =
            "Notifications Enabled";

        showSettingMessage(
            "🔔 Notifications have been enabled."
        );

    }

    else {

        status.innerText =
            "Notifications Disabled";

        showSettingMessage(
            "🔕 Notifications have been disabled."
        );

    }

}



// =====================================================
// DARK MODE
// =====================================================

function toggleDarkMode() {

    const toggle =
        document.getElementById("darkModeToggle");

    const status =
        document.getElementById("themeStatus");


    if (!toggle || !status) {
        return;
    }


    if (toggle.checked) {

        document.body.classList.add("dark-mode");

        status.innerText =
            "Dark Mode";

        localStorage.setItem(
            "smartFarmerTheme",
            "dark"
        );

        showSettingMessage(
            "🌙 Dark mode enabled."
        );

    }

    else {

        document.body.classList.remove("dark-mode");

        status.innerText =
            "Light Mode";

        localStorage.setItem(
            "smartFarmerTheme",
            "light"
        );

        showSettingMessage(
            "☀️ Light mode enabled."
        );

    }

}



// =====================================================
// LOAD SAVED THEME
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const savedTheme =
            localStorage.getItem(
                "smartFarmerTheme"
            );


        const toggle =
            document.getElementById(
                "darkModeToggle"
            );


        const status =
            document.getElementById(
                "themeStatus"
            );


        if (
            savedTheme === "dark" &&
            toggle
        ) {

            document.body.classList.add(
                "dark-mode"
            );

            toggle.checked = true;

            if (status) {

                status.innerText =
                    "Dark Mode";

            }

        }

    }
);



// =====================================================
// LANGUAGE
// =====================================================

function changeLanguage() {

    const language =
        document.getElementById(
            "languageSelect"
        ).value;


    if (language === "tamil") {

        showSettingMessage(
            "தமிழ் மொழி தேர்வு செய்யப்பட்டது."
        );

    }

    else if (language === "hindi") {

        showSettingMessage(
            "हिन्दी भाषा चुनी गई है।"
        );

    }

    else {

        showSettingMessage(
            "🇬🇧 English language selected."
        );

    }

}



// =====================================================
// CHANGE PASSWORD
// =====================================================

function changePassword() {

    const newPassword =
        prompt(
            "Enter your new password:"
        );


    if (newPassword === null) {
        return;
    }


    if (newPassword.trim() === "") {

        alert(
            "Please enter a password."
        );

        return;

    }


    if (newPassword.length < 6) {

        alert(
            "Password must contain at least 6 characters."
        );

        return;

    }


    showSettingMessage(
        "🔐 Password change request saved."
    );

}
// =========================================
// PROFILE MANAGEMENT
// =========================================

function openProfile() {

    const modal = document.getElementById("profileModal");

    modal.style.display = "flex";

    // Load saved details
    const savedName = localStorage.getItem("farmerName");
    const savedPhone = localStorage.getItem("farmerPhone");
    const savedLocation = localStorage.getItem("farmerLocation");
    const savedCrop = localStorage.getItem("farmerCrop");

    if (savedName) {
        document.getElementById("farmerName").value = savedName;
    }

    if (savedPhone) {
        document.getElementById("farmerPhone").value = savedPhone;
    }

    if (savedLocation) {
        document.getElementById("farmerLocation").value = savedLocation;
    }

    if (savedCrop) {
        document.getElementById("farmerCrop").value = savedCrop;
    }
}


// CLOSE PROFILE

function closeProfile() {

    document.getElementById("profileModal").style.display = "none";

}


// SAVE PROFILE

const profileForm = document.getElementById("profileForm");

if (profileForm) {

    profileForm.addEventListener("submit", function(event) {

        event.preventDefault();

        const name =
            document.getElementById("farmerName").value;

        const phone =
            document.getElementById("farmerPhone").value;

        const location =
            document.getElementById("farmerLocation").value;

        const crop =
            document.getElementById("farmerCrop").value;


        // Save in browser

        localStorage.setItem("farmerName", name);
        localStorage.setItem("farmerPhone", phone);
        localStorage.setItem("farmerLocation", location);
        localStorage.setItem("farmerCrop", crop);


        // Update dashboard

        document.getElementById("displayName").innerText =
            "Welcome, " + name;


        document.getElementById("displayInfo").innerText =
            crop + " Farmer • " + location;


        closeProfile();


        alert("✅ Profile updated successfully!");

    });

}


// CLOSE WHEN CLICKING OUTSIDE

window.addEventListener("click", function(event) {

    const modal =
        document.getElementById("profileModal");

    if (event.target === modal) {

        closeProfile();

    }

});
// =========================================
// MANAGE PROFILE
// =========================================

function openProfile() {

    const modal = document.getElementById("profileModal");

    if (modal) {
        modal.style.display = "flex";
    }

}


// =========================================
// CLOSE PROFILE
// =========================================

function closeProfile() {

    const modal = document.getElementById("profileModal");

    if (modal) {
        modal.style.display = "none";
    }

}


// =========================================
// SAVE PROFILE
// =========================================

document.addEventListener("DOMContentLoaded", function () {

    const profileForm = document.getElementById("profileForm");

    if (profileForm) {

        profileForm.addEventListener("submit", function (event) {

            event.preventDefault();

            const name =
                document.getElementById("farmerName").value;

            const phone =
                document.getElementById("farmerPhone").value;

            const location =
                document.getElementById("farmerLocation").value;

            const crop =
                document.getElementById("farmerCrop").value;


            // Update profile on dashboard

            const displayName =
                document.getElementById("displayName");

            const displayInfo =
                document.getElementById("displayInfo");


            if (displayName) {

                displayName.innerText =
                    "Welcome, " + name;

            }


            if (displayInfo) {

                displayInfo.innerText =
                    "📍 " + location +
                    "  |  🌾 " + crop +
                    "  |  📞 " + phone;

            }


            // Save data in browser

            localStorage.setItem("farmerName", name);
            localStorage.setItem("farmerPhone", phone);
            localStorage.setItem("farmerLocation", location);
            localStorage.setItem("farmerCrop", crop);


            alert("✅ Profile updated successfully!");


            closeProfile();

        });

    }

});


// =========================================
// LOAD SAVED PROFILE
// =========================================

document.addEventListener("DOMContentLoaded", function () {

    const name =
        localStorage.getItem("farmerName");

    const phone =
        localStorage.getItem("farmerPhone");

    const location =
        localStorage.getItem("farmerLocation");

    const crop =
        localStorage.getItem("farmerCrop");


    if (name) {

        document.getElementById("farmerName").value = name;

        document.getElementById("displayName").innerText =
            "Welcome, " + name;

    }


    if (phone) {

        document.getElementById("farmerPhone").value = phone;

    }


    if (location) {

        document.getElementById("farmerLocation").value = location;

    }


    if (crop) {

        document.getElementById("farmerCrop").value = crop;

    }


    if (name && location && crop) {

        document.getElementById("displayInfo").innerText =
            "📍 " + location +
            "  |  🌾 " + crop +
            "  |  📞 " + phone;

    }

});

