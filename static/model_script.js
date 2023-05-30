function uploadFile() {
    var select = document.getElementById('file-select');
    console.log("select.options[select.options.selectedIndex]: ", select.options[select.options.selectedIndex]);
    var selectedOption = select.options[select.selectedIndex].text;
    
    fetch('/process_file', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ option: selectedOption})
    })
    .then(response => {
        console.log("Server response: ", response);
    })
}

function populateFileSelect(fileNames) {
    var select = document.getElementById('file-select');
    select.innerHTML = ''; // Clear existing options

    fileNames.forEach(fileName => {
        var option = document.createElement('option');
        option.text = fileName;
        select.add(option);
    });
}

function fetchFileNamesFromServer() {
    fetch('/get_file_names')
        .then(response => response.json())
        .then(data => {
            console.log("data = ", data);
            populateFileSelect(data);
        })
        .catch(error => {
            console.error('Error: ', error);
        });
}

fetchFileNamesFromServer();