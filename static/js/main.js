// ==========================================
// Gym Management System - Front-end JavaScript Interactions
// ==========================================

document.addEventListener("DOMContentLoaded", function() {
    // 1. Sidebar Toggle Button
    const menuToggle = document.getElementById("menu-toggle");
    const wrapper = document.getElementById("wrapper");

    if (menuToggle && wrapper) {
        menuToggle.addEventListener("click", function(e) {
            e.preventDefault();
            wrapper.classList.toggle("toggled");
        });
    }

    // 2. Dark/Light Theme Handler
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = themeToggle ? themeToggle.querySelector("i") : null;

    function applyTheme(theme) {
        if (theme === "dark") {
            document.body.classList.add("dark-mode");
            if (themeIcon) {
                themeIcon.className = "fa-solid fa-sun text-warning";
            }
        } else {
            document.body.classList.remove("dark-mode");
            if (themeIcon) {
                themeIcon.className = "fa-solid fa-moon";
            }
        }
    }

    if (themeToggle) {
        themeToggle.addEventListener("click", function() {
            const currentTheme = document.body.classList.contains("dark-mode") ? "dark" : "light";
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            localStorage.setItem("gym-theme", newTheme);
            applyTheme(newTheme);
        });
    }

    // Initialize Theme Choice from localStorage
    const savedTheme = localStorage.getItem("gym-theme") || "light";
    applyTheme(savedTheme);
});
