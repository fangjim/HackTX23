document.addEventListener('DOMContentLoaded', function () {
    const surveyForm = document.getElementById('surveyForm');
    const collectedValues = document.getElementById('collectedValues');
    
    surveyForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const exerciseRating = document.getElementById('exercise').value;
        const dietRating = document.getElementById('diet').value;
        const personalCareRating = document.getElementById('personalCare').value;
        const clothesRating = document.getElementById('clothes').value;
        const entertainmentRating = document.getElementById('entertainment').value;
        const electronicsRating = document.getElementById('electronics').value;
        const budget = document.getElementById('budget').value;

        // Update the values in the DOM
        document.getElementById('exerciseRating').textContent = exerciseRating;
        document.getElementById('dietRating').textContent = dietRating;
        document.getElementById('personalCareRating').textContent = personalCareRating;
        document.getElementById('clothesRating').textContent = clothesRating;
        document.getElementById('entertainmentRating').textContent = entertainmentRating;
        document.getElementById('electronicsRating').textContent = electronicsRating;
        document.getElementById('budgetValue').textContent = budget;

        // Hide the survey form
        surveyForm.style.display = 'none';

        // Show the collected values
        collectedValues.style.display = 'block';
    });
});
