import "../css/profile.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal, closeAlert, initializeEntityModal, renderNationality, renderLanguage, enableClose } from "./functions";
import { fetchWorkerTrait, 
    fetchAddLanguage, fetchOwnLanguage, fetchDeleteLanguage, fetchSearchLanguage, 
    fetchSearchNationality, fetchAddNationality, fetchOwnNationality, fetchDeleteNationality, 
    fetchExperience,
    fetchUpdateExperience,
    fetchDeleteExperience} from "./api";
import { Experience } from "./interfaces";


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
        enableModal("experience_add");

        const timelineDiv = document.querySelector(".timeline") as HTMLElement;

        if (!timelineDiv) return;

        timelineDiv.addEventListener("click", async function onClick(event: Event ) {
            const target = event.target as HTMLElement;

            const editExperience = target.closest(".experience_edit") as HTMLElement | null;

            if (editExperience) {
                const experienceId = Number(editExperience.getAttribute("data-id")) as number;
                const experienceModal = document.querySelector("#experience_modal") as HTMLElement;
                const experienceForm = document.querySelector("#experience_form") as HTMLFormElement;
    
                const experience = await fetchExperience(experienceId) as Experience;
    
                if (!experience && !experienceModal && !experienceForm) return;
    
                experienceForm.action = `/experience/${experienceId}/`;
                experienceForm.method = "PATCH";
    
                (experienceForm.querySelector('input[name="position"]') as HTMLInputElement).value = experience.position;
                (experienceForm.querySelector('input[name="institution_name"]') as HTMLInputElement).value = experience.institution_name;
                (experienceForm.querySelector('textarea[name="description"]') as HTMLTextAreaElement).value = experience.description;
                (experienceForm.querySelector('input[name="start_year"]') as HTMLInputElement).value = experience.start_year.toString();
                (experienceForm.querySelector('input[name="end_year"]') as HTMLInputElement).value = experience.end_year ? experience.end_year.toString() : "";
                experienceModal.classList.remove("none");   
                enableClose(experienceModal);         
            
                experienceForm.addEventListener("submit", async (event) => {
                    event.preventDefault();
            
                    const experience: Experience = {
                        experience_id: Number(experienceForm.action.split("/").slice(-2, -1)[0]),
                        position: (experienceForm.querySelector('input[name="position"]') as HTMLInputElement).value,
                        institution_name: (experienceForm.querySelector('input[name="institution_name"]') as HTMLInputElement).value,
                        description: (experienceForm.querySelector('textarea[name="description"]') as HTMLTextAreaElement).value,
                        start_year: Number((experienceForm.querySelector('input[name="start_year"]') as HTMLInputElement).value),
                        end_year: Number((experienceForm.querySelector('input[name="end_year"]') as HTMLInputElement).value) || null,
                        type: (experienceForm.querySelector('input[name="type"]') as HTMLInputElement).value as "Work" | "Education",
                    };
            
                    await fetchUpdateExperience(experience);
    
                });
            };

            const deleteExperience = target.closest(".experience_delete") as HTMLElement | null;

            if (deleteExperience) {
                const experienceId = Number(deleteExperience.getAttribute("data-id")) as number;
                await fetchDeleteExperience(experienceId);
            }
        });

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