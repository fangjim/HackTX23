// Add this code in popup.js to show the popup page when the survey is submitted
chrome.runtime.onMessage.addListener(function (message, sender, response) {
    if (message.from === 'survey' && message.subject === 'surveySubmitted') {
      // Show the popup page
      document.body.style.display = 'block';
    }
  });
  