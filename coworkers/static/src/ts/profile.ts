import "../css/profile.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';

document.addEventListener("DOMContentLoaded", () => {
    const url = new URL(window.location.href);
    const sectionName = url.searchParams.get("section");


    // Working with personal attributes section
    if (sectionName == "personal-attributes") {
        document.querySelector(".profile")?.addEventListener("click", (event: Event) => {
            const target = event.target as HTMLElement;

            if (target.classList.contains("slider-info")) {
                const nextElement = target.nextElementSibling as HTMLElement;
        
                if (nextElement) {
                    nextElement.classList.toggle("none"); 
                }
            } else if (target.classList.contains("slider-description")) {
                target.classList.toggle("none");
            }
        })
    }

});