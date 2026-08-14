  
    document.addEventListener("DOMContentLoaded", () => { const navLinks =
    document.querySelectorAll(".nav-links a"); const currentPage =
    window.location.pathname.split("/").pop() || "index.html";
    navLinks.forEach(link => { const linkPage =
    link.getAttribute("href").split("/").pop(); if (linkPage === currentPage) {
    // Give REGISTRATION-style pages the pill, everyone else the plain gold text
    if (linkPage === "registration.html") { link.classList.add("active-pill"); }
    else { link.classList.add("active-text"); } } }); });
  