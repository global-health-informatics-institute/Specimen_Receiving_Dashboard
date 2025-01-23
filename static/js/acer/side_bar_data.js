// Select the elements to update
const registeredTotal = document.getElementById('summaryRegisteredTotal');
const receivedTotal = document.getElementById('summaryReceivedTotal');
const inProgressTotal = document.getElementById('summaryInProgressTotal');
const pendingAuthTotal = document.getElementById('summaryPendingAuthTotal');
const completedTotal = document.getElementById('summaryCompleteTotal');
const rejectedTotal = document.getElementById('summaryRejectedTotal');

// Function to fetch and update sidebar data
function fetchAndUpdateSidebar() {
  fetch('/side_bar_data') // Fetch data from the new JSON endpoint
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json(); // Parse JSON response
    })
    .then(data => {
      // Update the content of the sidebar
      registeredTotal.textContent = data.registered || 0;
      receivedTotal.textContent = data.received || 0;
      inProgressTotal.textContent = data.in_progress || 0;
      pendingAuthTotal.textContent = data.pending_auth || 0;
      completedTotal.textContent = data.completed || 0;
      rejectedTotal.textContent = data.rejected || 0;
    })
    .catch(error => {
      console.error('Error fetching sidebar data:', error);
    });
}

// Fetch and update every 5 seconds
setInterval(fetchAndUpdateSidebar, 5000);
fetchAndUpdateSidebar(); // Initial fetch on page load
