$(document).ready(function() {
  function fetchSummaryData() {
      $.ajax({
          url: "/summary_data",
          method: "GET",
          success: function(data) {
              $("#summaryRegisteredTotal").text(data.registered);
              $("#summaryReceivedTotal").text(data.received);
              $("#summaryInProgressTotal").text(data.in_progress);
              $("#summaryPendingAuthTotal").text(data.pending_auth);
              $("#summaryCompleteTotal").text(data.completed);
              $("#summaryRejectedTotal").text(data.rejected);
              console.log(data)
              console.log(data.completed)
          }
      });
  }

  fetchSummaryData();
  setInterval(fetchSummaryData, 1300); 
});
