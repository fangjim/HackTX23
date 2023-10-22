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
    }

    // ... (rest of your code, including the random score, product extraction, etc.)
    const randomScore = Math.floor(Math.random() * 5) + 1;
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