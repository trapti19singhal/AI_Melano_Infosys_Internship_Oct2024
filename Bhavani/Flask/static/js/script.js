document.getElementById("get-started-btn").addEventListener("click", () => {
    document.getElementById("intro-dialog").style.display = "none";
    document.getElementById("project-dialog").style.display = "block";
});

document.getElementById("back-to-intro").addEventListener("click", () => {
    document.getElementById("project-dialog").style.display = "none";
    document.getElementById("intro-dialog").style.display = "block";
});

document.getElementById("back-to-project").addEventListener("click", () => {
    document.getElementById("result-dialog").style.display = "none";
    document.getElementById("project-dialog").style.display = "block";
});

document.getElementById("predict-btn").addEventListener("click", () => {
    const fileInput = document.getElementById("file-upload");
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append("file", file);

        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.class && data.confidence) {
                document.getElementById("prediction-class").innerText = "Class: " + data.class;
                document.getElementById("confidence").innerText = "Confidence: " + data.confidence;
            }

            const reader = new FileReader();
            reader.onload = e => document.getElementById("result-img").src = e.target.result;
            reader.readAsDataURL(file);

            document.getElementById("project-dialog").style.display = "none";
            document.getElementById("result-dialog").style.display = "block";
        })
        .catch(error => alert("Error: " + error));
    }
});
