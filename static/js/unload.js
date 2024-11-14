function unLoadEntries() {
    fetch('http://127.0.0.1:5000/unLoadZ/')
        .then(response => {
            // Optionally log the status
            console.log('Request made to  Status:', response.status);
        })
        .catch(error => {
            console.error('There has been a problem with your purge operation:', error);
        });
}

// Run fetchData every 15 seconds
setInterval(unLoadEntries, 1000);

