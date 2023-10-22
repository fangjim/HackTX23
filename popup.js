document.addEventListener('DOMContentLoaded', function () {
    // Check if the survey has already been completed
    const surveyCompleted = localStorage.getItem('surveyCompleted');

    if (!surveyCompleted) {
        // Survey form code
        const surveyForm = document.getElementById('surveyForm');
        const collectedValues = document.getElementById('collectedValues');

        const randomScore = Math.floor(Math.random() * 5) + 1;
        document.getElementById('score').textContent = `Score: ${randomScore}`;

        surveyForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const exerciseRating = document.getElementById('exercise').value;
            const dietRating = document.getElementById('diet').value;
            const personalCareRating = document.getElementById('personalCare').value;
            const clothesRating = document.getElementById('clothes').value;
            const entertainmentRating = document.getElementById('entertainment').value;
            const electronicsRating = document.getElementById('electronics').value;
            const budget = document.getElementById('budget').value;

            localStorage.setItem('exerciseRating', exerciseRating);
            localStorage.setItem('dietRating', dietRating);
            localStorage.setItem('personalCareRating', personalCareRating);
            localStorage.setItem('clothesRating', clothesRating);
            localStorage.setItem('entertainmentRating', entertainmentRating);
            localStorage.setItem('electronicsRating', electronicsRating);
            localStorage.setItem('budget', budget);

            // Update the values in the DOM
            document.getElementById('exerciseRating').textContent = exerciseRating;
            document.getElementById('dietRating').textContent = dietRating;
            document.getElementById('personalCareRating').textContent = personalCareRating;
            document.getElementById('clothesRating').textContent = clothesRating;
            document.getElementById('entertainmentRating').textContent = entertainmentRating;
            document.getElementById('electronicsRating').textContent = electronicsRating;
            document.getElementById('budgetValue').textContent = budget;

            // Mark the survey as completed
            localStorage.setItem('surveyCompleted', 'true');

            // Hide the survey form
            surveyForm.style.display = 'none';

            // Show the collected values
            collectedValues.style.display = 'block';
        });
    } else {
        // Survey has already been completed, hide the survey form
        const surveyForm = document.getElementById('surveyForm');
        surveyForm.style.display = 'none';

        // Show the collected values
        const collectedValues = document.getElementById('collectedValues');
        collectedValues.style.display = 'block';

        populateCollectedValues();
    }

    function populateCollectedValues() {
        // Retrieve saved survey values from local storage
        const exerciseRating = localStorage.getItem('exerciseRating');
        const dietRating = localStorage.getItem('dietRating');
        const personalCareRating = localStorage.getItem('personalCareRating');
        const clothesRating = localStorage.getItem('clothesRating');
        const entertainmentRating = localStorage.getItem('entertainmentRating');
        const electronicsRating = localStorage.getItem('electronicsRating');
        const budget = localStorage.getItem('budget');

        // Update the values in the DOM
        document.getElementById('exerciseRating').textContent = `Exercise Rating: ${exerciseRating}`;
        document.getElementById('dietRating').textContent = `Diet Rating: ${dietRating}`;
        document.getElementById('personalCareRating').textContent = `Personal Care Rating: ${personalCareRating}`;
        document.getElementById('clothesRating').textContent = `Clothes Rating: ${clothesRating}`;
        document.getElementById('entertainmentRating').textContent = `Entertainment Rating: ${entertainmentRating}`;
        document.getElementById('electronicsRating').textContent = `Electronics Rating: ${electronicsRating}`;
        document.getElementById('budgetValue').textContent = `${budget}`;
    }

    //The following is completely unverfied and probably definitely doesn't work
    // Prepare the message with 9 inputs
    // const message = {
    //     exerciseRating: exerciseRating,
    //     dietRating: dietRating,
    //     personalCareRating: personalCareRating,
    //     clothesRating: clothesRating,
    //     entertainmentRating: entertainmentRating,
    //     electronicsRating: electronicsRating,
    //     budget: budget,
    //     productName: productName,
    //     productPrice: productPrice
    // };

    // // Send the message to the native application (main.py)
    // chrome.runtime.sendNativeMessage('com.example.nativeapp', message, function (response) {
    //     if (chrome.runtime.lastError) {
    //         // Handle any error that occurs during communication
    //     } else {
    //     // Update the score with the result received from the native application
    //         const score = response.score;
    //         document.getElementById('score').textContent = `Score: ${score}`;
    //     }
    // });  
    // ////////////////////////////





    // ... (rest of your code, including the random score, product extraction, etc.)
    // Calculate the score and set the color accordingly
    const randomScore = Math.floor(Math.random() * 10) + 1; // Generate a random score between 1 and 10
    let color;

    if (randomScore <= 4) {
        color = 'red'; // Scores 1-4 are red
    } else if (randomScore <= 7) {
        color = 'yellow'; // Scores 5-7 are yellow
    } else {
        color = 'green'; // Scores 8-10 are green
    }

    // Set the score and its color
    const scoreElement = document.getElementById('score');
    scoreElement.textContent = `Score: ${randomScore}`;
    scoreElement.style.color = color; // Set the color based on the score

    document.getElementById('score').textContent = `Score: ${randomScore}`;

    function addProductToList(productName, productPrice) {
        const productInfo = { name: productName, price: productPrice };
        const productList = JSON.parse(localStorage.getItem('productList')) || [];
        productList.push(productInfo);
        localStorage.setItem('productList', JSON.stringify(productList));
        displayProduct(productInfo);
    }

    // Function to display the added product in the popup
    function displayProduct(productInfo) {
        const productList = document.getElementById('productList');
        const productContainer = document.createElement('div');
        productContainer.textContent = `${productInfo.name} - ${productInfo.price}`;
        productList.appendChild(productContainer);
    }

    // Function to initialize the product list on popup load
    function initializeProductList() {
        const productList = JSON.parse(localStorage.getItem('productList')) || [];
        for (const productInfo of productList) {
            displayProduct(productInfo);
        }
    }
    //event listener for add button
    document.getElementById('addProductButton').addEventListener('click', function () {
        // Call the function to extract and add product information
        extractProductInfo();
    });

    // Add an event listener for the "plus" button
    document.getElementById('addProductButton').addEventListener('click', function () {
        // Call the function to extract and add product information
        extractProductInfo();
    });

    // Initialize the product list when the popup is loaded
    initializeProductList();

    function extractProductInfo() {
        let productName = '';
        let productPrice = '';

        // Request product information from content script
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { from: 'popup', subject: 'getData' }, function (response) {
                if (response) {
                    productName = response.title;
                    productPrice = response.price;

                    // If product information is extracted successfully, add it to the list
                    if (productName && productPrice) {
                        addProductToList(productName, productPrice);
                    }
                }
            });
        });
    }
});

chrome.runtime.sendMessage({
    from: 'content',
    subject: 'getTabId'
});