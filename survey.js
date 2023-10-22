document.addEventListener('DOMContentLoaded', function () {
    const surveyForm = document.getElementById('surveyForm');
    surveyForm.addEventListener('submit', function (event) {
        event.preventDefault();

        // Collect user ratings and budget allocation
        const exerciseRating = document.getElementById('exercise').value;
        // Repeat for other categories
        const budget = document.getElementById('budget').value;

        // Send the data to the main extension page
        chrome.runtime.sendMessage({
            from: 'survey',
            subject: 'surveyData',
            exercise: exerciseRating,
            // Include ratings for other categories
            budget: budget,
        });

        // Close the survey page
        window.close();
    });
});
