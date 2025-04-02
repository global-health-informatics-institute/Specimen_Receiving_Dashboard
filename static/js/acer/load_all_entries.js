// test 1
$(document).ready(function() {
    function fetchTestContent1() {
        $.ajax({
            url: "/test_data_1",
            method: "GET",
            success: function(data) {
                $("#received1").text(data.received_1);
                $("#inProgress1").text(data.in_progress_1);
                $("#pendingAuth1").text(data.pending_auth_1);
                $("#complete1").text(data.completed_1);
            }
        });
    }

    fetchTestContent1();
    setInterval(fetchTestContent1, 1300); 
});

// test 2
$(document).ready(function() {
    function fetchTestContent2() {
        $.ajax({
            url: "/test_data_2",
            method: "GET",
            success: function(data) {
                $("#received2").text(data.received_2);
                $("#inProgress2").text(data.in_progress_2);
                $("#pendingAuth2").text(data.pending_auth_2);
                $("#complete2").text(data.completed_2);
            }
        });
    }

    fetchTestContent2();
    setInterval(fetchTestContent2, 1300); 
});

// test 3
$(document).ready(function() {
    function fetchTestContent3() {
        $.ajax({
            url: "/test_data_3",
            method: "GET",
            success: function(data) {
                $("#received3").text(data.received_3);
                $("#inProgress3").text(data.in_progress_3);
                $("#pendingAuth3").text(data.pending_auth_3);
                $("#complete3").text(data.completed_3);
            }
        });
    }

    fetchTestContent3();
    setInterval(fetchTestContent3, 1300); 
});


// test 4
$(document).ready(function() {
    function fetchTestContent4() {
        $.ajax({
            url: "/test_data_4",
            method: "GET",
            success: function(data) {
                $("#received4").text(data.received_4);
                $("#inProgress4").text(data.in_progress_4);
                $("#pendingAuth4").text(data.pending_auth_4);
                $("#complete4").text(data.completed_4);
            }
        });
    }

    fetchTestContent4();
    setInterval(fetchTestContent4, 1300); 
});