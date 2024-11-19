import "../css/profile.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal } from "./functions";


document.addEventListener("DOMContentLoaded", () => {
    const url = new URL(window.location.href);
    const sectionName = url.searchParams.get("section") as string | null;


    // Working with personal data section
    if (sectionName == "personal-data" || sectionName == null) {
        enableModal("fullname_form");
        enableModal("nationality_form");
        enableModal("language_form");
        enableModal("salary_form");
        enableModal("location_form");
        enableModal("links_form");
    }


    // Working with experience timeline
    if (sectionName == "work-timeline" || sectionName == "education-timeline") {
        enableModal("experience_form");
    }

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