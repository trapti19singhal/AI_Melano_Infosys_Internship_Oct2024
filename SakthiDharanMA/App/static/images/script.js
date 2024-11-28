document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predict-form');
    const loadingIndicator = document.getElementById('loading-indicator');

    form.addEventListener('submit', function() {
        loadingIndicator.style.display = 'block';
    });
});
