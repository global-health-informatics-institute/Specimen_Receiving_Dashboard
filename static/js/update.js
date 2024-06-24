function fetchData() {
    fetch('http://127.0.0.1:5000/update/')
        .then(response => {
            // Optionally log the status
            console.log('Request made to http://127.0.0.1:5000. Status:', response.status);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

// Run fetchData every 15 seconds
setInterval(fetchData, 15000);


