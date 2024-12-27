import "../css/profile.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal, closeAlert, applySearchListener, renderNationality, renderLanguage } from "./functions";
import { fetchWorkerTrait, 
    fetchAddLanguage, fetchOwnLanguage, fetchDeleteLanguage, fetchSearchLanguage, 
    fetchSearchNationality, fetchAddNationality, fetchOwnNationality, fetchDeleteNationality } from "./api";
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


        const handleLanguageClick = (e: MouseEvent, addedLanguages: Set<number>, addedDiv: HTMLElement) => {
            const target = e.target as HTMLElement;
            const container = target.closest("[data-id]");
            if (!container) return;
        
            const languageId = Number(container?.getAttribute("data-id"));
            const languageName = String(container?.getAttribute("data-name"));
        
            if (target.classList.contains("result_remove")) {
                addedLanguages.delete(languageId);
                container?.remove();
                fetchDeleteLanguage(languageId);
            } else if (target.classList.contains("result_add")) {
                if (addedLanguages.size === 0) {
                    addedDiv.innerHTML = '';
                }

                addedLanguages.add(languageId);
                fetchAddLanguage(languageId);
                renderLanguage({ language_id: languageId, language_name: languageName }, "Remove", addedDiv);
                container?.remove();
            };
        };

        const initializeLanguageModal = () => {
            const parentDiv = document.querySelector(".language_result") as HTMLElement;
            if (!parentDiv) return;
        
            const addedDiv = parentDiv.querySelector(".language_added") as HTMLElement;
            const searchedDiv = parentDiv.querySelector(".language_searched") as HTMLElement;
            const addedLanguages = new Set<number>();
        
            if (!addedDiv || !searchedDiv) return;
        
            fetchOwnLanguage()
                .then((results) => {
                    if (results.length === 0) {
                        addedDiv.innerHTML = 'No language indicated at the moment.';
                        return;
                    }
        
                    results.forEach((language: Language) => {
                        addedLanguages.add(language.language_id);
                        renderLanguage(language, "Remove", addedDiv);
                    });
                })
                .catch((error) => {
                    console.error("Error fetching initial languages:", error);
                });
        
            parentDiv.addEventListener("click", (e) => handleLanguageClick(e, addedLanguages, addedDiv));
        
            applySearchListener(languageSearch, fetchSearchLanguage, (results) => {
                searchedDiv.innerHTML = '';
                results.forEach((result: Language) => {
                    if (!addedLanguages.has(result.language_id)) {
                        renderLanguage(result, "Add", searchedDiv);
                    };
                });
            });
        };

        const handleNationalityClick = (e: MouseEvent, addedNationalities: Set<number>, addedDiv: HTMLElement) => {
            const target = e.target as HTMLElement;
            const container = target.closest("[data-id]");
            if (!container) return;
        
            const nationalityId = Number(container?.getAttribute("data-id"));
            const nationalityName = String(container?.getAttribute("data-name"));
        
            if (target.classList.contains("result_remove")) {
                addedNationalities.delete(nationalityId);
                container?.remove();
                fetchDeleteNationality(nationalityId); 
            } else if (target.classList.contains("result_add")) {
                if (addedNationalities.size === 0) {
                    addedDiv.innerHTML = '';
                }

                addedNationalities.add(nationalityId);
                fetchAddNationality(nationalityId);
                renderNationality({ nationality_id: nationalityId, nationality_name: nationalityName }, "Remove", addedDiv);
                container?.remove();
            }
        };
        
        const initializeNationalityModal = () => {
            if (!nationalitySearch) return;
        
            const parentDiv = document.querySelector(".nationality_result") as HTMLElement;
            if (!parentDiv) return;
        
            const addedDiv = parentDiv.querySelector(".nationality_added") as HTMLElement;
            const searchedDiv = parentDiv.querySelector(".nationality_searched") as HTMLElement;
            const addedNationalities = new Set<number>();
        
            if (!addedDiv || !searchedDiv) return;
        
            fetchOwnNationality()
            .then((results) => {
                if (results.length === 0) {
                    addedDiv.innerHTML = 'No nationality indicated at the moment.';
                    return;
                }
        
                results.forEach((nationality: Nationality) => {
                    addedNationalities.add(nationality.nationality_id);
                    renderNationality(nationality, "Remove", addedDiv);
                });
            })
            .catch((error) => {
                console.error("Error fetching initial nationalities:", error);
            });
        
            parentDiv.addEventListener("click", (e) => handleNationalityClick(e, addedNationalities, addedDiv));
        
            applySearchListener(nationalitySearch, fetchSearchNationality, (results) => {
                searchedDiv.innerHTML = '';
                results.forEach((result: Nationality) => {
                    if (!addedNationalities.has(result.nationality_id)) {
                        renderNationality(result, "Add", searchedDiv);
                    };
                });
            });
        };
        
        initializeNationalityModal();
        initializeLanguageModal();

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