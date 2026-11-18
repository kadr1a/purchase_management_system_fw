"use strict";

// Подставляет актуальный год в подвал сайта.
const yearElement = document.getElementById("current-year");
if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}
