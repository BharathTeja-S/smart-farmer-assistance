// =====================================================
// SMART FARMER - GOVERNMENT SCHEMES
// =====================================================

const schemes = {

    pmkisan: {

        title: "PM-KISAN 🇮🇳",

        subtitle: "Pradhan Mantri Kisan Samman Nidhi",

        icon: "🇮🇳",

        description:
            "PM-KISAN provides income support to eligible landholding farmer families.",

        benefits: [
            "₹6,000 financial support per year",
            "Amount is provided in three installments",
            "₹2,000 is provided in each installment",
            "Direct benefit transfer to eligible farmers"
        ],

        eligibility: [
            "Farmer should be an eligible landholding farmer",
            "Farmer should have valid land records",
            "Bank account should be linked for receiving benefits",
            "Other exclusion criteria may apply"
        ],

        website: "https://pmkisan.gov.in/"
    },


    pmfby: {

        title: "PMFBY 🛡️",

        subtitle: "Pradhan Mantri Fasal Bima Yojana",

        icon: "🛡️",

        description:
            "PMFBY provides crop insurance protection against losses caused by natural risks and other covered events.",

        benefits: [
            "Protection against eligible crop losses",
            "Financial support after covered crop damage",
            "Helps farmers manage agricultural risks",
            "Crop insurance coverage"
        ],

        eligibility: [
            "Farmers growing notified crops may be eligible",
            "Coverage depends on the notified area and crop",
            "Farmers should follow applicable enrollment requirements",
            "Insurance terms depend on current scheme guidelines"
        ],

        website: "https://pmfby.gov.in/"
    },


    kcc: {

        title: "Kisan Credit Card 💳",

        subtitle: "Kisan Credit Card (KCC)",

        icon: "💳",

        description:
            "Kisan Credit Card provides farmers with access to credit for agricultural and related expenses.",

        benefits: [
            "Credit support for agricultural activities",
            "Helps meet cultivation expenses",
            "Can support purchase of agricultural inputs",
            "Credit is provided through eligible financial institutions"
        ],

        eligibility: [
            "Eligible farmers can apply",
            "Eligibility is assessed by the lending institution",
            "Required documents may include identity and land-related documents",
            "Terms and limits depend on the lender"
        ],

        website: "https://www.myscheme.gov.in/"
    }

};


// =====================================================
// OPEN GOVERNMENT SCHEME
// =====================================================

function openScheme(schemeId) {

    console.log("openScheme called:", schemeId);

    const scheme = schemes[schemeId];

    if (!scheme) {

        alert("Scheme information not found.");

        return;
    }


    const modal = document.getElementById("schemeModal");

    const content = document.getElementById("schemeContent");


    if (!modal) {

        alert("ERROR: schemeModal is missing from dashboard.html");

        return;
    }


    if (!content) {

        alert("ERROR: schemeContent is missing from dashboard.html");

        return;
    }


    content.innerHTML = `

        <div class="scheme-popup">

            <button
                type="button"
                class="scheme-popup-x"
                onclick="closeScheme()">

                ×

            </button>


            <div class="scheme-popup-icon">

                ${scheme.icon}

            </div>


            <h2>

                ${scheme.title}

            </h2>


            <p class="scheme-popup-subtitle">

                ${scheme.subtitle}

            </p>


            <p class="scheme-popup-description">

                ${scheme.description}

            </p>


            <div class="scheme-popup-section">

                <h3>

                    🌱 Benefits

                </h3>


                <ul>

                    ${scheme.benefits
                        .map(item => `<li>${item}</li>`)
                        .join("")}

                </ul>

            </div>


            <div class="scheme-popup-section">

                <h3>

                    ✅ Eligibility

                </h3>


                <ul>

                    ${scheme.eligibility
                        .map(item => `<li>${item}</li>`)
                        .join("")}

                </ul>

            </div>


            <div class="scheme-popup-actions">

                <a
                    href="${scheme.website}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="scheme-popup-btn">

                    🌐 Visit Official Website

                </a>


                <button
                    type="button"
                    class="scheme-popup-close-btn"
                    onclick="closeScheme()">

                    Close

                </button>

            </div>

        </div>

    `;


    modal.classList.add("show");

    document.body.classList.add("modal-open");

}


// =====================================================
// CLOSE GOVERNMENT SCHEME
// =====================================================

function closeScheme() {

    const modal = document.getElementById("schemeModal");

    if (!modal) {

        return;
    }

    modal.classList.remove("show");

    document.body.classList.remove("modal-open");

}


// =====================================================
// CLICK OUTSIDE MODAL TO CLOSE
// =====================================================

document.addEventListener("click", function(event) {

    const modal = document.getElementById("schemeModal");

    if (!modal) {

        return;
    }


    if (event.target === modal) {

        closeScheme();

    }

});


// =====================================================
// ESC KEY TO CLOSE
// =====================================================

document.addEventListener("keydown", function(event) {

    if (event.key === "Escape") {

        closeScheme();

    }

});


// =====================================================
// TEST
// =====================================================

console.log("✅ Smart Farmer schemes.js loaded successfully");