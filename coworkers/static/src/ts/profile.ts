import "../css/profile.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal, closeAlert, initializeEntityModal, renderNationality, renderLanguage } from "./functions";
import { fetchWorkerTrait, 
    fetchAddLanguage, fetchOwnLanguage, fetchDeleteLanguage, fetchSearchLanguage, 
    fetchSearchNationality, fetchAddNationality, fetchOwnNationality, fetchDeleteNationality } from "./api";


document.addEventListener("DOMContentLoaded", () => {
    const url = new URL(window.location.href);
    const sectionName = url.searchParams.get("section") as string | null;

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



        const languageSearch = document.getElementById("search_language") as HTMLInputElement;
        const nationalitySearch = document.getElementById("search_nationality") as HTMLInputElement;


        initializeEntityModal(
            languageSearch,
            fetchOwnLanguage,
            fetchSearchLanguage,
            fetchAddLanguage,
            fetchDeleteLanguage,
            renderLanguage,
            "language",
            "language"
        );
        
        initializeEntityModal(
            nationalitySearch,
            fetchOwnNationality,
            fetchSearchNationality,
            fetchAddNationality,
            fetchDeleteNationality,
            renderNationality,
            "nationality",
            "nationality"
        );

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
                

                // on button click save the new trait value
                saveBtn.addEventListener("click", function onClick() {
                    const traitId = rangeInput.getAttribute("id") as string | "";
                    const traitScore = rangeInput.value as string | "";

                    function onSuccess() {
                        showSave = false;
                        saveBtn.classList.add("none");
                        saveBtn.removeEventListener("click", onClick);
                    }

                    fetchWorkerTrait(traitId, traitScore, onSuccess);
                });

                showSave = true;
            });
        });
    }


});