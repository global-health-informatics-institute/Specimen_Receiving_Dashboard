document.addEventListener("DOMContentLoaded", () => {
    async function fetchSummaryData() {
        try {
            const response = await fetch("/side_bar_data");
            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();

            document.getElementById("summaryRegisteredTotal").textContent = data.registered;
            document.getElementById("summaryReceivedTotal").textContent = data.received;
            document.getElementById("summaryInProgressTotal").textContent = data.in_progress;
            document.getElementById("summaryPendingAuthTotal").textContent = data.pending_auth;
            document.getElementById("summaryCompleteTotal").textContent = data.completed;
            document.getElementById("summaryRejectedTotal").textContent = data.rejected;

        } catch (err) {
            console.error("Error fetching summary data:", err);
        }
    }

    // run immediately
    fetchSummaryData();
    // refresh every 1.3s
    setInterval(fetchSummaryData, 1300);
});



document.addEventListener("DOMContentLoaded", () => {
    async function fetchTestContent1() {
        try {
            const response = await fetch("/test_data_1");
            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();
            console.log("Fetched:", data);

            document.getElementById("received1").textContent = data.received_1;
            document.getElementById("inProgress1").textContent = data.in_progress_1;
            document.getElementById("pendingAuth1").textContent = data.pending_auth_1;
            document.getElementById("complete1").textContent = data.completed_1;

        } catch (err) {
            console.error("Error fetching test content 1:", err);
        }
    }

    // Run immediately
    fetchTestContent1();
    // Refresh every 1.3s
    setInterval(fetchTestContent1, 1300);
});


document.addEventListener("DOMContentLoaded", () => {
    async function fetchTestContent2() {
        try {
            const response = await fetch("/test_data_2");
            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();

            document.getElementById("received2").textContent = data.received_2;
            document.getElementById("inProgress2").textContent = data.in_progress_2;
            document.getElementById("pendingAuth2").textContent = data.pending_auth_2;
            document.getElementById("complete2").textContent = data.completed_2;

        } catch (err) {
            console.error("Error fetching test content 2:", err);
        }
    }

    // Run immediately
    fetchTestContent2();
    // Refresh every 1.3s
    setInterval(fetchTestContent2, 1300);
});



document.addEventListener("DOMContentLoaded", () => {
    async function fetchTestContent3() {
        try {
            const response = await fetch("/test_data_3");
            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();

            document.getElementById("received3").textContent = data.received_3;
            document.getElementById("inProgress3").textContent = data.in_progress_3;
            document.getElementById("pendingAuth3").textContent = data.pending_auth_3;
            document.getElementById("complete3").textContent = data.completed_3;

        } catch (err) {
            console.error("Error fetching test content 3:", err);
        }
    }

    // Run immediately
    fetchTestContent3();
    // Refresh every 1.3s
    setInterval(fetchTestContent3, 1300);
});



document.addEventListener("DOMContentLoaded", () => {
    async function fetchTestContent4() {
        try {
            const response = await fetch("/test_data_4");
            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();

            document.getElementById("received4").textContent = data.received_4;
            document.getElementById("inProgress4").textContent = data.in_progress_4;
            document.getElementById("pendingAuth4").textContent = data.pending_auth_4;
            document.getElementById("complete4").textContent = data.completed_4;

        } catch (err) {
            console.error("Error fetching test content 4:", err);
        }
    }

    // Run immediately
    fetchTestContent4();
    // Refresh every 1.3s
    setInterval(fetchTestContent4, 1300);
});



// weekly
document.addEventListener("DOMContentLoaded", () => {
    async function fetchWeeklySummaryContent() {
        try {
            const response = await fetch("/weekly_summary_data");
            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();

            document.getElementById("weeklyRegistered").textContent = data.weekly_count_registered;
            document.getElementById("weeklyRecieved").textContent = data.weekly_count_received;
            document.getElementById("weeklyProgress").textContent = data.weekly_count_progress;
            document.getElementById("weeklyPending").textContent = data.weekly_count_pending;
            document.getElementById("weeklyComplete").textContent = data.weekly_count_complete;
            document.getElementById("weeklyRejected").textContent = data.weekly_count_rejected;

        } catch (err) {
            console.error("Error fetching weekly summary data:", err);
        }
    }

    // Run immediately
    fetchWeeklySummaryContent();
    // Refresh every 1.3s
    setInterval(fetchWeeklySummaryContent, 1300);
});


// monthly
document.addEventListener("DOMContentLoaded", () => {
    async function fetchMonthlySummaryContent() {
        try {
            const response = await fetch("/monthly_summary_data");
            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();

            document.getElementById("monthlyRegistered").textContent = data.monthly_count_registered;
            document.getElementById("monthlyRecieved").textContent = data.monthly_count_received;
            document.getElementById("monthlyProgress").textContent = data.monthly_count_progress;
            document.getElementById("monthlyPending").textContent = data.monthly_count_pending;
            document.getElementById("monthlyComplete").textContent = data.monthly_count_complete;
            document.getElementById("monthlyRejected").textContent = data.monthly_count_rejected;

        } catch (err) {
            console.error("Error fetching monthly summary data:", err);
        }
    }

    // Run immediately
    fetchMonthlySummaryContent();
    // Refresh every 1.3s
    setInterval(fetchMonthlySummaryContent, 1300);
});


document.addEventListener("DOMContentLoaded", () => {
    async function fetchTatCurrent() {
        try {
            const response = await fetch("/tat_current");
            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();

            document.getElementById("current1").textContent = data.current_1;
            document.getElementById("current2").textContent = data.current_2;
            document.getElementById("current3").textContent = data.current_3;
            document.getElementById("current4").textContent = data.current_4;

        } catch (err) {
            console.error("Error fetching TAT current data:", err);
        }
    }

    // Run immediately
    fetchTatCurrent();
    // Refresh every 1.3s
    setInterval(fetchTatCurrent, 1300);
});


document.addEventListener("DOMContentLoaded", () => {
    async function fetchTatAverage() {
        try {
            const response = await fetch("/tat_average");
            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();

            document.getElementById("average1").textContent = data.average_1;
            document.getElementById("average2").textContent = data.average_2;
            document.getElementById("average3").textContent = data.average_3;
            document.getElementById("average4").textContent = data.average_4;

        } catch (err) {
            console.error("Error fetching TAT average data:", err);
        }
    }

    // Run immediately
    fetchTatAverage();
    // Refresh every 1.3s
    setInterval(fetchTatAverage, 1300);
});
