import "../css/profile.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal, closeAlert, applySearchListener } from "./functions";
import { fetchWorkerTrait, fetchLanguage, fetchNationality } from "./api";
import { Language, Nationality } from "./interfaces";


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


        if (languageSearch) {
            const resultDiv = document.querySelector(".language_result") as HTMLElement;

            if (!resultDiv) return;

            applySearchListener(languageSearch, fetchLanguage, (results) => {
                resultDiv.innerHTML = '';
                
                results.forEach((result: Language) => {
                    resultDiv.insertAdjacentHTML("afterbegin", `
                        <div class="row language d-flex align-items-center" data-id="${result.language_id}">
                            <div class="col-md-4 d-flex justify-content-start">${result.language_name}</div>
                            <div class="col-md-2 pmodal_level">Beginner</div>
                            <div class="col-md-2 pmodal_level">Professional</div>
                            <div class="col-md-2 pmodal_level pmodal_level_active">Native</div>
                            <div class="col-md-2 pmodal_remove">Remove</div>
                        </div>
                    `);
                });
            });
           
        }


        if (nationalitySearch) {
            const parentDiv = document.querySelector(".nationality_result") as HTMLElement;
            const resultDiv = parentDiv?.firstElementChild as HTMLElement;

            if (!resultDiv) return;

            applySearchListener(nationalitySearch, fetchNationality, (results) => {
                resultDiv.innerHTML = '';
                console.log(results);
                results.forEach((result: Nationality) => {
                    resultDiv.insertAdjacentHTML("afterbegin", `
                        <div class="col-md-6 d-flex justify-content-between align-items-center" data-id="${result.nationality_id}">
                            <span class="nationality" data-id="1">${result.nationality_name}</span>
                            <span class="pmodal_remove">Remove</span>
                        </div>
                    `);
                });
            });
        }

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