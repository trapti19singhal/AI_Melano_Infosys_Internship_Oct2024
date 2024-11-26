document.getElementById("image-upload").addEventListener("change", function () {
    const fileInput = this;
    const uploadedImg = document.getElementById("uploaded-image");

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            uploadedImg.src = e.target.result;
            uploadedImg.style.display = "block";
        };
        reader.readAsDataURL(fileInput.files[0]);
    } else {
        uploadedImg.src = "";
        uploadedImg.style.display = "none";
    }
});

document.getElementById("upload-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const fileInput = document.getElementById("image-upload");
    const resultDiv = document.getElementById("prediction");
    const uploadedImg = document.getElementById("uploaded-image");
    
    resultDiv.innerHTML = "";
    if (!fileInput.files[0]) {
        resultDiv.innerHTML = "<p style='color: red;'>Please select an image file.</p>";
        return;
    }
    
    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            resultDiv.innerHTML = `
                <p><strong>Prediction:</strong> ${data.predicted_class}</p>
                <p><strong>Confidence:</strong> ${data.confidence}%</p>
            `;
            uploadedImg.src = data.image_url;
            uploadedImg.style.display = "block";
        } else {
            const data = await response.json();
            resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: red;">An error occurred. Please try again.</p>`;
    }
});
