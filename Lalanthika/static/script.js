document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.upload-form');
    const fileInput = document.getElementById('file-upload');
    const submitBtn = document.getElementById('submit-btn');
    const uploadButton = document.getElementById('upload-button');
    const fileChosenText = document.getElementById("file-chosen");

    // Trigger file input click when upload button is clicked
    uploadButton.addEventListener('click', function () {
        fileInput.click(); // Simulate a click on the hidden file input
    });

    // Enable submit button after a file is selected
    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            submitBtn.disabled = false; // Enable the submit button
            displayFileName(); // Display the selected file name
        } else {
            submitBtn.disabled = true; // Disable if no file selected
        }
    });

    // Add animation to the submit button when clicked
    submitBtn.addEventListener('click', function (e) {
        e.preventDefault();  // Prevent form submission initially
        submitBtn.innerHTML = 'Uploading...'; // Change button text to indicate upload
        submitBtn.disabled = true;  // Disable button during upload process

        // Simulate uploading by resetting the file input
        setTimeout(function () {
            // Submit the form
            form.submit(); 

            // Reset file input for the next upload
            fileInput.value = ''; // Clear the file input
            fileChosenText.textContent = 'No file chosen'; // Reset the file name display

            // Reset button to allow re-uploading
            submitBtn.innerHTML = 'Submit';
            submitBtn.disabled = true; // Disable submit button until next file is selected
        }, 1500); // Wait for 1.5 seconds to simulate upload time
    });
});

function displayFileName() {
    const fileInput = document.getElementById('file-upload');
    const fileName = fileInput.files[0].name;
    document.getElementById('file-chosen').textContent = fileName;
    document.getElementById('submit-btn').disabled = false; // Enable submit button after file selection
}
