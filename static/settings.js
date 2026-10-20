/* =====================================================
   SMART FARMER - SETTINGS JAVASCRIPT
===================================================== */


/* =====================================================
   SHOW SETTINGS MESSAGE
===================================================== */

function showSettingMessage(message) {

    const messageBox =
        document.getElementById("settingsMessage");

    const messageText =
        document.getElementById("settingsMessageText");

    if (!messageBox || !messageText) {
        alert(message);
        return;
    }

    messageText.textContent = message;

    messageBox.style.display = "block";

    setTimeout(function () {

        messageBox.style.display = "none";

    }, 3000);
}


/* =====================================================
   NOTIFICATION TOGGLE
===================================================== */

function toggleNotifications() {

    const toggle =
        document.getElementById("notificationToggle");

    const status =
        document.getElementById("notificationStatus");

    if (!toggle || !status) {
        return;
    }

    if (toggle.checked) {

        status.textContent =
            "Notifications Enabled";

        localStorage.setItem(
            "notifications",
            "enabled"
        );

    } else {

        status.textContent =
            "Notifications Disabled";

        localStorage.setItem(
            "notifications",
            "disabled"
        );
    }
}


/* =====================================================
   DARK MODE
===================================================== */

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

        status.textContent =
            "Dark Mode";

        localStorage.setItem(
            "theme",
            "dark"
        );

    } else {

        document.body.classList.remove("dark-mode");

        status.textContent =
            "Light Mode";

        localStorage.setItem(
            "theme",
            "light"
        );
    }
}


/* =====================================================
   LOAD SAVED SETTINGS
===================================================== */

function loadSettings() {

    const notificationToggle =
        document.getElementById("notificationToggle");

    const notificationStatus =
        document.getElementById("notificationStatus");

    const darkModeToggle =
        document.getElementById("darkModeToggle");

    const themeStatus =
        document.getElementById("themeStatus");


    /* ---------- Notifications ---------- */

    const savedNotifications =
        localStorage.getItem("notifications");

    if (savedNotifications === "disabled") {

        if (notificationToggle) {
            notificationToggle.checked = false;
        }

        if (notificationStatus) {
            notificationStatus.textContent =
                "Notifications Disabled";
        }

    } else {

        if (notificationToggle) {
            notificationToggle.checked = true;
        }

        if (notificationStatus) {
            notificationStatus.textContent =
                "Notifications Enabled";
        }
    }


    /* ---------- Theme ---------- */

    const savedTheme =
        localStorage.getItem("theme");

    if (savedTheme === "dark") {

        document.body.classList.add("dark-mode");

        if (darkModeToggle) {
            darkModeToggle.checked = true;
        }

        if (themeStatus) {
            themeStatus.textContent =
                "Dark Mode";
        }

    } else {

        document.body.classList.remove("dark-mode");

        if (darkModeToggle) {
            darkModeToggle.checked = false;
        }

        if (themeStatus) {
            themeStatus.textContent =
                "Light Mode";
        }
    }
}


/* =====================================================
   MANAGE ACCOUNT
===================================================== */
/* =====================================================
   MANAGE ACCOUNT
===================================================== */

function manageAccount() {

    const profileModal =
        document.getElementById("profileModal");

    if (profileModal) {

        profileModal.style.display = "flex";

        return;
    }

    window.location.href = "/profile";
}
/* =====================================================
   CHANGE PASSWORD
===================================================== */

async function changePassword() {

    /* -----------------------------------------------
       CURRENT PASSWORD
    ------------------------------------------------ */

    const currentPassword =
        prompt("Enter your current password:");

    if (currentPassword === null) {
        return;
    }

    if (currentPassword.trim() === "") {

        alert(
            "Current password cannot be empty."
        );

        return;
    }


    /* -----------------------------------------------
       NEW PASSWORD
    ------------------------------------------------ */

    const newPassword =
        prompt("Enter your new password:");

    if (newPassword === null) {
        return;
    }

    if (newPassword.trim() === "") {

        alert(
            "New password cannot be empty."
        );

        return;
    }

    if (newPassword.length < 6) {

        alert(
            "New password must contain at least 6 characters."
        );

        return;
    }


    /* -----------------------------------------------
       CONFIRM PASSWORD
    ------------------------------------------------ */

    const confirmPassword =
        prompt("Confirm your new password:");

    if (confirmPassword === null) {
        return;
    }


    if (newPassword !== confirmPassword) {

        alert(
            "New password and confirm password do not match."
        );

        return;
    }


    /* -----------------------------------------------
       SEND TO FLASK
    ------------------------------------------------ */

    try {

        const response =
            await fetch(
                "/change-password",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        current_password:
                            currentPassword,

                        new_password:
                            newPassword

                    })
                }
            );


        const result =
            await response.json();


        /* -------------------------------------------
           SUCCESS
        -------------------------------------------- */

        if (result.success) {

            showSettingMessage(
                "Password changed successfully! 🔐"
            );

            alert(
                "✅ Password changed successfully.\n\n" +
                "Your new password will be required the next time you login."
            );

        } else {

            alert(
                "❌ " +
                (result.message ||
                    "Unable to change password.")
            );
        }


    } catch (error) {

        console.error(
            "PASSWORD ERROR:",
            error
        );

        alert(
            "❌ Unable to connect to the server."
        );
    }
}


/* =====================================================
   PRIVACY INFORMATION
===================================================== */
/* =====================================================
   DATA & PRIVACY
===================================================== */
function showPrivacy() {
    let modal = document.getElementById("privacyInformationModal");

    if (!modal) {
        modal = document.createElement("div");
        modal.id = "privacyInformationModal";

        modal.innerHTML = `
            <div class="privacy-overlay" onclick="closePrivacy()"></div>

            <div class="privacy-box">

                <button type="button"
                        class="privacy-close"
                        onclick="closePrivacy()">
                    ×
                </button>

                <div class="privacy-icon">🔐</div>

                <h2>Data & Privacy</h2>

                <p class="privacy-intro">
                    Your information is handled securely
                    by the Smart Farmer Assistance system.
                </p>

                <div class="privacy-item">
                    <span>👤</span>
                    <div>
                        <strong>Account Information</strong>
                        <small>
                            Your username is stored securely
                            in the application database.
                        </small>
                    </div>
                </div>

                <div class="privacy-item">
                    <span>🔑</span>
                    <div>
                        <strong>Password Security</strong>
                        <small>
                            Your password is stored as a secure
                            hash and is not stored as plain text.
                        </small>
                    </div>
                </div>

                <div class="privacy-item">
                    <span>🌾</span>
                    <div>
                        <strong>Farming Information</strong>
                        <small>
                            Your crop and location information
                            can be used by Smart Farmer features.
                        </small>
                    </div>
                </div>

                <div class="privacy-item">
                    <span>🛡️</span>
                    <div>
                        <strong>Login Security</strong>
                        <small>
                            Your account is protected using
                            a secure login session.
                        </small>
                    </div>
                </div>

                <button type="button"
                        class="privacy-ok-btn"
                        onclick="closePrivacy()">
                    Got it
                </button>

            </div>
        `;

        document.body.appendChild(modal);
    }

    modal.style.display = "flex";
}


function closePrivacy() {
    const modal =
        document.getElementById("privacyInformationModal");

    if (modal) {
        modal.style.display = "none";
    }
}
/* =====================================================
   CLOSE PRIVACY
===================================================== */

function closePrivacy() {

    const modal =
        document.getElementById(
            "privacyInformationModal"
        );

    if (modal) {

        modal.style.display = "none";

    }
}


/* =====================================================
   START SETTINGS
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadSettings();

    }
);