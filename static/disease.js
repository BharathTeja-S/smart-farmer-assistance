// ============================================================
// SMART FARMER
// CROP DISEASE DETECTION
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const diseaseForm =
        document.getElementById("diseaseForm");

    const cropImage =
        document.getElementById("cropImage");

    const imagePreview =
        document.getElementById("imagePreview");

    const diseaseName =
        document.getElementById("diseaseName");

    const diseaseMessage =
        document.getElementById("diseaseMessage");

    const confidence =
        document.getElementById("confidence");

    const cropHealth =
        document.getElementById("cropHealth");

    const treatment =
        document.getElementById("treatment");


    // ========================================================
    // IMAGE PREVIEW
    // ========================================================

    cropImage.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) {
            imagePreview.innerHTML = "";
            return;
        }


        if (!file.type.startsWith("image/")) {

            alert("Please select a valid image.");

            this.value = "";

            return;
        }


        const reader = new FileReader();


        reader.onload = function (event) {

            imagePreview.innerHTML = `
                <img
                    src="${event.target.result}"
                    alt="Crop Preview"
                    style="
                        max-width:100%;
                        max-height:250px;
                        border-radius:15px;
                        margin-top:15px;
                    "
                >
            `;

        };


        reader.readAsDataURL(file);

    });



    // ========================================================
    // DISEASE ANALYSIS
    // ========================================================

    diseaseForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const file =
                cropImage.files[0];


            if (!file) {

                alert("Please upload a crop image.");

                return;

            }


            // ------------------------------------------------
            // SHOW ANALYZING MESSAGE
            // ------------------------------------------------

            diseaseName.textContent =
                "Analyzing Crop...";

            diseaseMessage.textContent =
                "Please wait while Smart Farmer analyzes the image.";

            confidence.textContent =
                "--";

            cropHealth.textContent =
                "--";

            treatment.textContent =
                "AI analysis is in progress...";


            // ------------------------------------------------
            // SEND IMAGE TO FLASK
            // ------------------------------------------------

            const formData =
                new FormData();

            formData.append(
                "crop_image",
                file
            );


            try {

                const response =
                    await fetch(
                        "/disease-check",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const result =
                    await response.json();


                console.log("Disease Result:", result);


                // ------------------------------------------------
                // DISPLAY RESULT
                // ------------------------------------------------

                diseaseName.textContent =
                    result.disease;

                diseaseMessage.textContent =
                    result.message;

                confidence.textContent =
                    result.confidence;

                cropHealth.textContent =
                    result.health;

                treatment.textContent =
                    result.treatment;


            }

            catch (error) {

                console.error(
                    "Disease Detection Error:",
                    error
                );


                diseaseName.textContent =
                    "Analysis Failed";

                diseaseMessage.textContent =
                    "Unable to connect to the disease detection server.";

                confidence.textContent =
                    "--";

                cropHealth.textContent =
                    "--";

                treatment.textContent =
                    "Please make sure your Flask server is running.";

            }

        }
    );

});