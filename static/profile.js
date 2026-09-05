```javascript
// =====================================================
// SMART FARMER - PROFILE POPUP TEST
// =====================================================

function openProfile() {

    const modal = document.getElementById("profileModal");

    if (modal) {

        modal.style.display = "flex";

        console.log("PROFILE OPENED");

    } else {

        alert("❌ profileModal NOT FOUND");

    }
}


function closeProfile() {

    const modal = document.getElementById("profileModal");

    if (modal) {

        modal.style.display = "none";

    }

}


// =====================================================
// SAVE PROFILE
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("profileForm");

    if (!form) {
        return;
    }

    form.addEventListener("submit", function (event) {

        event.preventDefault();

        const name =
            document.getElementById("farmerName").value;

        const phone =
            document.getElementById("farmerPhone").value;

        const location =
            document.getElementById("farmerLocation").value;

        const crop =
            document.getElementById("farmerCrop").value;


        if (!name || !phone || !location) {

            alert("Please fill all required details.");

            return;

        }


        localStorage.setItem("farmerName", name);
        localStorage.setItem("farmerPhone", phone);
        localStorage.setItem("farmerLocation", location);
        localStorage.setItem("farmerCrop", crop);


        const displayName =
            document.getElementById("displayName");

        const displayInfo =
            document.getElementById("displayInfo");


        if (displayName) {

            displayName.textContent =
                "Welcome, " + name;

        }


        if (displayInfo) {

            displayInfo.textContent =
                "Location: " +
                location +
                " • Main Crop: " +
                crop;

        }


        alert("✅ Profile saved successfully!");

        closeProfile();

    });

});
```
