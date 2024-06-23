async function updateEntries() {
    try {
        const response = await fetch("http:127.0.0.1:5000/update/", { method: 'HEAD' });
        if (response.ok) {
            statusElement.textContent = `Website is up! Status: ${response.status}`;
        } else {
            statusElement.textContent = `Website is down. Status: ${response.status}`;
        }
    } catch (error) {
        statusElement.textContent = `Error: ${error.message}`;
    }

}
updateEntries();
// Run fetchData every 15 seconds
setInterval(updateEntries, 15000);

