function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const preview = document.getElementById('image-preview');
        preview.style.display = 'block';
        preview.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}
// script.js
document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const resultDiv = document.getElementById('prediction-result');

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.classList.add('show');
        if (data.error) {
            resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `<p>Prediction: ${data.prediction}</p><p>Confidence: ${data.confidence.toFixed(2)}</p>`;
        }
    })
    .catch(error => {
        resultDiv.classList.add('show');
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    });
});
function updateProgressBar(value) {
    document.getElementById('progress-bar-container').style.display = 'block';
    document.getElementById('progress-bar').value = value;
}
// Function to toggle visibility of content
function toggleContent() {
    var content = document.getElementById('hidden-content');
    
    // Check if the content is currently hidden or visible
    if (content.style.display === 'none') {
        content.style.display = 'block'; // Show the content
    } else {
        content.style.display = 'none'; // Hide the content
    }
}
