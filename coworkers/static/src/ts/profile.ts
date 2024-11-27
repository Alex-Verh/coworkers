import "../css/profile.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal, closeAlert, showAlert } from "./functions";


document.addEventListener("DOMContentLoaded", () => {
    const url = new URL(window.location.href);
    const sectionName = url.searchParams.get("section") as string | null;
    const csrfTokenElem = document.querySelector('meta[name="csrf-token"]') as HTMLElement | null;
    let csrfToken = "";
    if (csrfTokenElem) {csrfToken = csrfTokenElem.getAttribute('content') as string | ""};


    enableModal('contact-form');
    closeAlert();

    // Working with personal data section
    if (sectionName == "personal-data" || sectionName == null) {
        const personalDataForms = [
            "fullname_form",
            "nationality_form",
            "language_form",
            "salary_form",
            "location_form",
            "links_form"
        ];
        
        personalDataForms.forEach(id => enableModal(id));
    }


    // Working with experience timeline
    if (sectionName == "work-timeline" || sectionName == "education-timeline") {
        enableModal("experience_form");
    }

    // Working with personal attributes section
    if (sectionName == "personal-attributes") {

        // sliders info buttons
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


        // sliders changes
        document.querySelectorAll(".personal-slider").forEach((slider: Element) => {
            const rangeInput = slider as HTMLInputElement;
            if (!rangeInput) return;

            const parentDiv = slider.parentElement as HTMLElement;
            if (!parentDiv) return;

            const saveBtn = parentDiv.querySelector(".slider-save") as HTMLElement;
            if (!saveBtn) return;

            let showSave = false;

            slider.addEventListener("change", function onChange() {
                // show the save button
                if (showSave) return;
                saveBtn.classList.remove("none");

                // on button click send the new trait value
                saveBtn.addEventListener("click", function onClick() {
                    fetch(`/worker-trait/`, {
                        method: "POST",
                        body: JSON.stringify({
                            trait_id: rangeInput.getAttribute("id"),
                            trait_score: rangeInput.value,
                        }),
                        headers: {
                            "X-Requested-With": "XMLHttpRequest",
                            "X-CSRFToken": csrfToken,
                        }
                    })
                    .then((response): Promise<String> => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then((data: any) => {
                        showSave = false;
                        saveBtn.classList.add("none");
                        saveBtn.removeEventListener("click", onClick);

                        if (data.messages && Array.isArray(data.messages)) {
                            data.messages.forEach((msg: string) => {
                                showAlert(msg, "success")
                            });
                        }
                    })
                    .catch((error) => {
                        console.error('Error saving data:', error);

                        if (error.messages && Array.isArray(error.messages)) {
                            error.messages.forEach((msg: string) => {
                                showAlert(msg, "error")
                            });
                        }
                    });
                });

                showSave = true;
            });
        });
    }


});