document.addEventListener("DOMContentLoaded", function() {
    const user = JSON.parse(localStorage.getItem("user"));
    const departmentName = localStorage.getItem("department_name");

    if (!user) {
        alert("You are not logged in!");
        window.location.href = "/login/";
        return;
    }

    const usernameElement = document.getElementById("header-username");
    const departmentElement = document.getElementById("departments");

    if (usernameElement) usernameElement.textContent = user.username || "N/A";
    if (departmentElement) departmentElement.textContent = departmentName || "N/A";
});

    function logout() {
        localStorage.removeItem("user");
        localStorage.removeItem("department");
        localStorage.removeItem("department_name");
        window.location.href = "/login/";
    }