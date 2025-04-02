// weekly
$(document).ready(function() {
    function fetchWeeklySummaryContent() {
        $.ajax({
            url: "/weekly_summary_data",
            method: "GET",
            success: function(data) {
                $("#weeklyRegistered").text(data.weekly_count_registered);
                $("#weeklyRecieved").text(data.weekly_count_received);
                
                $("#weeklyProgress").text(data.weekly_count_progress);

                $("#weeklyPending").text(data.weekly_count_pending);

                $("#weeklyComplete").text(data.weekly_count_complete);

                $("#weeklyRejected").text(data.weekly_count_rejected);
            }
        });
    }

    fetchWeeklySummaryContent();
    setInterval(fetchWeeklySummaryContent, 1300); 
});

// monthly
$(document).ready(function() {
    function fetchMonthlySummaryContent() {
        $.ajax({
            url: "/monthly_summary_data",
            method: "GET",
            success: function(data) {
                $("#monthlyRegistered").text(data.monthly_count_registered);
                $("#monthlyRecieved").text(data.monthly_count_received);
                
                $("#monthlyProgress").text(data.monthly_count_progress);

                $("#monthlyPending").text(data.monthly_count_pending);

                $("#monthlyComplete").text(data.monthly_count_complete);

                $("#monthlyRejected").text(data.monthly_count_rejected);
            }
        });
    }

    fetchMonthlySummaryContent();
    setInterval(fetchMonthlySummaryContent, 1300); 
});