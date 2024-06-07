$(document).ready(function() {
    function fetchSummaryData() {
        $.ajax({
            url: "/summary_content",
            method: "GET",
            success: function(data) {
                $("#summaryRegisteredTotal").text(data.summaryRegisteredTotal);
                $("#summaryReceivedTotal").text(data.summaryReceivedTotal);
                $("#summaryInProgressTotal").text(data.summaryInProgressTotal);
                $("#summaryPendingAuthTotal").text(data.summaryPendingAuthTotal);
                $("#summaryCompleteTotal").text(data.summaryCompleteTotal);
            }
        });
    }

    fetchSummaryData();
    setInterval(fetchSummaryData, 30000); // 30000ms = 30 seconds
});



$(document).ready(function() {
    function fetchTestContent1() {
        $.ajax({
            url: "/test_content1",
            method: "GET",
            success: function(data) {
                $("#received1").text(data.received1);
                $("#inProgress1").text(data.inProgress1);
                $("#pendingAuth1").text(data.pendingAuth1);
                $("#complete1").text(data.complete1);
            }
        });
    }

    fetchTestContent1();
    setInterval(fetchTestContent1, 30000); // 30000ms = 30 seconds
});



$(document).ready(function() {
    function fetchTestContent2() {
        $.ajax({
            url: "/test_content2",
            method: "GET",
            success: function(data) {
                $("#received2").text(data.received2);
                $("#inProgress2").text(data.inProgress2);
                $("#pendingAuth2").text(data.pendingAuth2);
                $("#complete2").text(data.complete2);
            }
        });
    }

    fetchTestContent2();
    setInterval(fetchTestContent2, 30000); // 30000ms = 30 seconds
});


$(document).ready(function() {
    function fetchTestContent3() {
        $.ajax({
            url: "/test_content3",
            method: "GET",
            success: function(data) {
                $("#received3").text(data.received3);
                $("#inProgress3").text(data.inProgress3);
                $("#pendingAuth3").text(data.pendingAuth3);
                $("#complete3").text(data.complete3);
            }
        });
    }

    fetchTestContent3();
    setInterval(fetchTestContent3, 30000); // 30000ms = 30 seconds
});


$(document).ready(function() {
    function fetchTestContent4() {
        $.ajax({
            url: "/test_content4",
            method: "GET",
            success: function(data) {
                $("#received4").text(data.received4);
                $("#inProgress4").text(data.inProgress4);
                $("#pendingAuth4").text(data.pendingAuth4);
                $("#complete4").text(data.complete4);
            }
        });
    }

    fetchTestContent4();
    setInterval(fetchTestContent4, 30000); // 30000ms = 30 seconds
});




$(document).ready(function() {
    function fetchWeeklyContent() {
        $.ajax({
            url: "/weekly_content",
            method: "GET",
            success: function(data) {
                $("#weeklyRegistered").text(data.weeklyRegistered);
                $("#weeklyRecieved").text(data.weeklyRecieved);
                $("#weeklyProgress").text(data.weeklyProgress);
                $("#weeklyComplete").text(data.weeklyComplete);
            }
        });
    }

    fetchWeeklyContent();
    setInterval(fetchWeeklyContent, 30000); // 30000ms = 30 seconds
});

$(document).ready(function() {
    function fetchMonthlyContent() {
        $.ajax({
            url: "/monthly_content",
            method: "GET",
            success: function(data) {
                $("#monthlyRegistered").text(data.monthlyRegistered);
                $("#monthlyRecieved").text(data.monthlyRecieved);
                $("#monthlyProgress").text(data.monthlyProgress);
                $("#monthlyComplete").text(data.monthlyComplete);
            }
        });
    }

    fetchMonthlyContent();
    setInterval(fetchMonthlyContent, 30000); // 30000ms = 30 seconds
});

