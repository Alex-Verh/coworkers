import "../css/index.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal, closeAlert, applySearchListener, renderWorker, renderFilterLanguage } from "./functions";
import { fetchSearchLanguage, fetchWorkers } from "./api";
import { User, FetchResponse, Language } from "./interfaces";


document.addEventListener("DOMContentLoaded", () => {

   
    // enable all modals for this page
    enableModal('contact-form');
    closeAlert();
    initializeSearchbar();

    applyFilters().then((response) => {
        displayWorkers(response, true);
        enableLoadMoreButton(response.has_next);

    }).catch((error) => {
        console.error('Error fetching data:', error);
    });
});


const handleSearchbarClick = (event: Event) => {
    const clickTarget = event.target as HTMLElement | null;

    if (!clickTarget) return;

    const filterBtn = clickTarget.closest(".searchbar_filter") as HTMLElement | null;

    if (!filterBtn) return;

    const resultsFilter = filterBtn.nextElementSibling as HTMLElement | null;

    if (!resultsFilter) return;

    toggleResultsFilter(resultsFilter);
}

const toggleResultsFilter = (resultsFilter: HTMLElement): void => {
    const handleResultClick = (event: Event): void => {
        const target = event.target as HTMLElement | null;

        if (!target) return;

        const searchResult = target.closest(".searchbar_result") as HTMLElement | null;

        if (searchResult) {
            searchResult.classList.toggle("searchbar_result_active");

            applyFilters().then((response) => {
                displayWorkers(response);
            }).catch((error) => {
                console.error('Error fetching data:', error);
            });       
         };
    };

    if (!resultsFilter.dataset.listenerAttached) {
        resultsFilter.addEventListener("click", handleResultClick);
        resultsFilter.dataset.listenerAttached = "true";
    }

    if (resultsFilter.innerHTML.trim() == '') {
        return;
    }

    resultsFilter.classList.toggle("none");
};

const getSelectedFilters = (dropdown: HTMLElement): string[] => {
    const activeResults = dropdown.querySelectorAll(".searchbar_result_active");
    return Array.from(activeResults).map((el) => el.getAttribute("data-value") || "");
};

const initializeSearchbar = () => {
    const searchBarHTML = document.querySelector(".searchbar") as HTMLElement | null;

    if (!searchBarHTML) {
        console.warn("Searchbar not found.");
        return;
    }
    searchBarHTML.addEventListener("click", handleSearchbarClick);

    const jobSearch = document.querySelector("#find_job") as HTMLInputElement | null;
    const locationSearch = document.querySelector("#find_location") as HTMLInputElement | null;
    const languageSearch = document.querySelector("#find_language") as HTMLInputElement | null;

    if (!jobSearch || !locationSearch || !languageSearch) return;

    applySearchListener(jobSearch, applyFilters, (results) => {displayWorkers(results)});
    applySearchListener(locationSearch, applyFilters, (results) => {displayWorkers(results)});
    applySearchListener(languageSearch, fetchSearchLanguage, (results) => {displayLanguages(results)});
}


const applyFilters = async () : Promise<FetchResponse>  => {
    const salaryDropdown = document.querySelector('[data-dropdown="salary"]') as HTMLElement;
    const experienceDropdown = document.querySelector('[data-dropdown="experience"]') as HTMLElement;
    const languageDropdown = document.querySelector('[data-dropdown="language"]') as HTMLElement;

    const selectedSalaries = getSelectedFilters(salaryDropdown);
    const selectedExperiences = getSelectedFilters(experienceDropdown);
    const selectedLanguages = getSelectedFilters(languageDropdown);

    const jobSearch = document.querySelector("#find_job") as HTMLInputElement | null;
    const locationSearch = document.querySelector("#find_location") as HTMLInputElement | null;
    const loadBtn = document.querySelector("#load-more") as HTMLButtonElement | null;

    const selectedJob = jobSearch?.value || "";
    const selectedLocation = locationSearch?.value || "";

    const page = loadBtn?.getAttribute('data-page') as string | 1;

    const params = new URLSearchParams({
        salary: selectedSalaries.join(","),
        experience: selectedExperiences.join(","),
        language: selectedLanguages.join(","),
        worker: selectedJob,
        location: selectedLocation,
        page: page.toString()
    });
    
    return fetchWorkers(params);
};

const displayWorkers = (fetchResponse: FetchResponse, clearResults= true) => {
    const searchResult = document.querySelector("#user-list") as HTMLElement;

    const userList = fetchResponse.users as Array<User>;

    console.log(userList.length);

    if (!searchResult) return;

    if (clearResults) searchResult.innerHTML = '';

    if (!userList || userList.length === 0) {
        searchResult.innerHTML = 'No worker found for this query.';
        return;
    }

    userList.forEach((user: User) => {
        renderWorker(user, searchResult);
    });

    enableLoadMoreButton(fetchResponse.has_next);
};

const enableLoadMoreButton = (has_next: boolean) => {
    const loadBtn = document.getElementById('load-more') as HTMLButtonElement | null;

    if (loadBtn) {
        if (!has_next) {
            loadBtn.classList.remove("button");
            loadBtn.classList.add("button_disabled");
            loadBtn.removeEventListener('click', onLoadClick);
        } else {
            loadBtn.classList.remove("button_disabled");
            loadBtn.classList.add("button");
            loadBtn.addEventListener('click', onLoadClick);
        }
    }
};

const onLoadClick = () => {
    const loadBtn = document.getElementById('load-more') as HTMLButtonElement | null;
    if (!loadBtn) return;

    const page = loadBtn.getAttribute('data-page') as string | null;
    if (!page) return;

    const currentPage = parseInt(page);

    if (loadBtn.classList.contains("button_disabled")) return;

    applyFilters().then((response) => {
        displayWorkers(response, false);

        enableLoadMoreButton(response.has_next);

        const nextPage = currentPage + 1;
        loadBtn.setAttribute('data-page', nextPage.toString());

    }).catch((error) => {
        console.error('Error fetching data:', error);
    });
};

const displayLanguages = (languages: Array<Language>) => {
    const languageResults = document.querySelector(".searchbar_languages") as HTMLElement;

    if (!languageResults) return;

    const removeElements = languageResults.querySelectorAll('.searchbar_result:not(.searchbar_result_active)');

    removeElements?.forEach(element => {
        element.remove();
    });

    const addedLanguages = languageResults.querySelectorAll('.searchbar_result_active');

    console.log(languages);

    if (languages.length > 0) {
        languageResults.classList.remove("none");
    } else if (languages.length === 0 && addedLanguages.length === 0) {
        languageResults.classList.add("none");
        return;
    }

    languages.forEach((language: Language) => {
        if (languageResults.querySelector(`[data-value="${language.language_id}"]`)) {
            return;
        }   
        renderFilterLanguage(language, languageResults);
    }) ;
}