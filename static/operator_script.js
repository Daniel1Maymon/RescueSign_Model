// JavaScript code to display one image at a time and provide navigation

// var imageUrls = {{ imageUrls| tojson }}
// var imageUrls = JSON.parse(document.currentScript.dataset.imageUrls);
// console.log(imageUrls);

var imageUrls = null;
// Get the chosen option element by its ID
var chosenOption = document.getElementById('chosen-option');

var waitingMsg = document.getElementById('waiting-msg')

function getImagesUrls() {
    console.log('::: function getImagesUrls():::')

    fetch('/get_images_urls', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        imageUrls = data;
        console.log("imageUrls = ", imageUrls)
    })
    .catch(error => {
        console.log('Error: ', error)
    })

    if (imageUrls !== null)
    {
        console.log("imageUrls = ", imageUrls)
    }
    else {
        console.log("imageUrl is null")
    }
    return imageUrls;
}

function openSocket() {
    waitingMsg.style.display = 'block';

    imageUrls = null
    console.log("::: OpenSocket Button clicked :::")
    fetch(
        '/create_socket_connection', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            console.log('operator.js:: all the frames received')

            imageContainer.style.display = 'block';
            waitingMsg.style.display = 'none'
            // Start displaying the images

            imageUrls = getImagesUrls();
            if (imageUrls !== null) {
                console.log("imageUrls is not null = ", imageUrls)
                updateImage();
            }
            else {
                console.log("imageUrls is null");
            }

        })

}


// Get the image container element by its ID
var imageContainer = document.getElementById('image-container');

// Hide the image container initially
imageContainer.style.display = 'none';
waitingMsg.style.display = 'none'

// Get the current image element by its ID
var currentImage = document.getElementById('current-image');
// Get the previous button element by its ID
var prevButton = document.getElementById('prev-button');
// Get the next button element by its ID
var nextButton = document.getElementById('next-button');

var currentIndex = 0; // Index of the currently displayed image





function isImageBroken(imageSrc) {

    return new Promise((resolve) => {
        const img = new Image();

        img.addEventListener('load', () => {
            resolve(false); // Image loaded successfully
        });

        img.addEventListener('error', () => {
            resolve(true); // Image failed to load
        });
        console.log(":: isImageBroken ::")
        img.src = imageSrc;
    })
}

// Function to update the displayed image
function updateImage() {
    var isBroken = true
    console.log(':: updateImage ::')
    if (imageUrls !== null) {

        isImageBroken(imageUrls[currentIndex]).then((isBroken) => {
            if (isBroken) {
                currentIndex++;
                console.log("currentImage.src is null")
            } else {
                currentImage.src = imageUrls[currentIndex];
                console.log("currentImage.src = ", currentImage.src)
            }
        })

    } else {
        console.log(" updateImage():: imageUrls is null")
    }
    
}

// Function to handle the previous button click
function handlePrevButtonClick() {
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        currentIndex = imageUrls.length - 1;
    }
    updateImage();
}

// Function to handle the next button click
function handleNextButtonClick() {
    if (currentIndex < imageUrls.length - 1) {
        currentIndex++;
    } else {
        currentIndex = 0;
    }
    updateImage();
}



function deleteAllFiles(){
    fetch('/delete_oldest_frames')
    .then(response => response.json())
    .then(data =>{
        console.log('response from /delete_oldest_frames: ', data)
    })
    .catch(error => {
        console.error('Error: ', error)
    })
}


function operatorResponse(response) {
    // Handle operator responses here
    imageContainer.style.display = 'none';
    waitingMsg.style.display = 'none'

    var selectedOption = event.target;
    selectedOption.style.color = "red";

    imageUrls = null;
    deleteAllFiles()

    console.log("Operator response: " + response);

    // Make an HTTP POST request to send the response to the server
    fetch('http://127.0.0.1:4002/response_from_operator', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answer: response })
    })
        .then(response => {
            // Handle the server response here if needed 
            console.log('Server response:', response);
            console.log("delete frames")
            
            // Start displaying the images
            // updateImage();
        })
        .catch(error => {
            // Handle any error that occurs during the request
            console.error('Error:', error);
        });

        

        // Remove the class after a timeout
        setTimeout(
            function() {
                selectedOption.style.color = ""; // Reset to default color (inherit or initial)
            }, 3000) 
}



// Add event listeners to the previous and next buttons
prevButton.addEventListener('click', handlePrevButtonClick);
nextButton.addEventListener('click', handleNextButtonClick);

// Call the openSocket function to establish the socket connection
// openSocket();