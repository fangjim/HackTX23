document.addEventListener('DOMContentLoaded', function () {
    console.log('initial console log');
    
    const surveyForm = document.getElementById('surveyForm');
    
    // Check if survey data is already saved
    chrome.storage.sync.get(['surveyData'], function (result) {
        if (result.surveyData) {
            // Survey data is already saved, close the survey
            window.close();
        } else {
            // Survey data is not saved, show the survey form
            surveyForm.style.display = 'block';
        }
    });

    surveyForm.addEventListener('submit', function (event) {
        //prevent default form behavior
        event.preventDefault();
    
        // Collect user ratings and budget allocation
        const exerciseRating = document.getElementById('exercise').value;
        const dietRating = document.getElementById('diet').value;
        const personalCareRating = document.getElementById('personalCare').value;
        const clothesRating = document.getElementById('clothes').value;
        const entertainmentRating = document.getElementById('entertainment').value;
        const electronicsRating = document.getElementById('electronics').value;
        const budget = document.getElementById('budget').value;
    
        // Save the survey data to Chrome storage
        console.log('Before adding submit event listener');

        surveyForm.addEventListener('submit', function (event) {
            console.log('Submit button clicked');  // Ensure this message is logged
            event.preventDefault();
        
            // Collect user ratings and budget allocation
            const exerciseRating = document.getElementById('exercise').value;
            // ...
        
            // Save the survey data to Chrome storage
            chrome.storage.sync.set({ surveyData: { exercise: exerciseRating, budget } }, function () {
                console.log('Data saved');
                // Data saved, close the survey form
                window.close();
                console.log('Window closed');  // Ensure this message is logged
                // Send a message to the popup to display it
                chrome.runtime.sendMessage({ from: 'survey', subject: 'surveySubmitted' });
            });
        });
        
          
    });
});

