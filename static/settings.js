/* =====================================================
   SMART FARMER - SETTINGS JAVASCRIPT
===================================================== */


/* =====================================================
   SHOW SETTINGS MESSAGE
===================================================== */

function showSettingMessage(message) {

    const messageBox = document.getElementById("settingsMessage");
    const messageText = document.getElementById("settingsMessageText");

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

    const toggle = document.getElementById("notificationToggle");
    const status = document.getElementById("notificationStatus");

    if (!toggle || !status) {
        return;
    }

    if (toggle.checked) {

        status.textContent = "Notifications Enabled";

        localStorage.setItem(
            "notifications",
            "enabled"
        );

    } else {

        status.textContent = "Notifications Disabled";

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

    const toggle = document.getElementById("darkModeToggle");
    const status = document.getElementById("themeStatus");

    if (!toggle || !status) {
        return;
    }


    if (toggle.checked) {

        document.body.classList.add("dark-mode");

        status.textContent = "Dark Mode";

        localStorage.setItem(
            "theme",
            "dark"
        );

    } else {

        document.body.classList.remove("dark-mode");

        status.textContent = "Light Mode";

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
   ACCOUNT
===================================================== */

function manageAccount() {

    showSettingMessage(
        "Account settings are ready to edit."
    );

}



/* =====================================================
   CHANGE PASSWORD
===================================================== */

function changePassword() {

    const newPassword = prompt(
        "Enter your new password:"
    );


    if (newPassword === null) {
        return;
    }


    if (newPassword.trim() === "") {

        alert(
            "Password cannot be empty."
        );

        return;
    }


    if (newPassword.length < 6) {

        alert(
            "Password must contain at least 6 characters."
        );

        return;
    }


    localStorage.setItem(
        "smartFarmerPassword",
        newPassword
    );


    showSettingMessage(
        "Password changed successfully."
    );

}



/* =====================================================
   PRIVACY
===================================================== */

function showPrivacy() {

    showSettingMessage(
        "Your farming information is protected by Smart Farmer."
    );

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