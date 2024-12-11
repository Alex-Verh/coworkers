// opening modal
export const enableModal = (buttonId: string) => {
    const openBtn = document.getElementById(buttonId) as HTMLElement | null;
    if (!openBtn) {
        console.warn(`Button with ID '${buttonId}' not found.`);
        return;
    }

    const modalId = openBtn.getAttribute('data-modal') as string | null;
    if (!modalId) {
        console.warn(`No 'data-modal' attribute found for button '${buttonId}'.`);
        return;
    }

    const modal = document.getElementById(modalId) as HTMLElement | null;
    if (!modal) {
        console.warn(`Modal with ID '${modalId}' not found.`);
        return;
    }

    openBtn.addEventListener('click', function onClick() {
        modal.classList.remove('none');
        document.body.classList.add('stop-scrolling');
        enableClose(modal);
    });
}


// closing modal
const enableClose = (modal: HTMLElement) => {
    const closeBtn = modal.querySelector('.pmodal_close') as HTMLElement | null;
    if (!closeBtn) {
        console.warn('Close button not found in modal.');
        return;
    }

    closeBtn.addEventListener('click', function onClick() {
        modal.classList.add('none');
        document.body.classList.remove('stop-scrolling');
        closeBtn.removeEventListener('click', onClick);
    })
}


// Server messages alert closing
export const closeAlert = () => {
    document.body.addEventListener("click", function onClick(event: Event) {
        const clickTarget = event.target as HTMLElement | null;

        if (!clickTarget) return;

        const closeBtn = clickTarget.closest(".palert_close") as HTMLElement | null;

        if (!closeBtn) {
            console.warn('Close button not found in alert.');
            return;
        }

        const alert = closeBtn.parentElement as HTMLElement | null;
        if (!alert) return;

        alert.classList.add('none');
        closeBtn.removeEventListener('click', onClick);
    })
}

export const showAlert = (message: string, type: string, priority: boolean = false)  => {
    const style = priority ? 'z-index: 10000;' : '';

    document.body.insertAdjacentHTML("afterbegin", `
        <div style="${style}" class="palert palert_${type} d-flex align-items-center justify-content-center">
            <img src="/static/public/icons/close_alert.svg" alt="Close" class="palert_close">
            <div class="palert_text">${message}</div>
        </div>    
    `)
}


const toggleResultsFilter = (resultsFilter: HTMLElement) => {
    function onResultFilterClick(event: Event) {
        const clickTarget = event.target as HTMLElement | null;

        if (!clickTarget) return;

        const searchResult = clickTarget.closest(".searchbar_result") as HTMLElement | null;

        if (!searchResult) return;

        searchResult.classList.toggle("searchbar_result_active");
    }

    if (resultsFilter.classList.contains("none")) {
        resultsFilter.classList.remove("none");
        console.log(resultsFilter.className);

        resultsFilter.addEventListener("click", onResultFilterClick);
    } else {
        resultsFilter.classList.add("none");
        resultsFilter.removeEventListener("click", onResultFilterClick);
    }
}

const handleSearchbarClick = (event: Event) => {
    const clickTarget = event.target as HTMLElement | null;

    if (!clickTarget) return;

    const filterBtn = clickTarget.closest(".searchbar_filter") as HTMLElement | null;

    if (!filterBtn) return;

    const resultsFilter = filterBtn.nextElementSibling as HTMLElement | null;

    if (!resultsFilter) return;

    toggleResultsFilter(resultsFilter);
}

export const initializeSearchbar = () => {
    const searchBarHTML = document.querySelector(".searchbar") as HTMLElement | null;

    if (!searchBarHTML) {
        console.warn("Searchbar not found.");
        return;
    }
    searchBarHTML.addEventListener("click", handleSearchbarClick);
}


export const applySearchListener = (
    searchInput: HTMLInputElement, 
    fetchFunction: (query: string) => Promise<any>,
    onResults: (results: any) => void
) => {
    let typingTimer: number | null = null;

    searchInput.addEventListener("input", () => {
        if (typingTimer) {
            clearTimeout(typingTimer);
        }

        typingTimer = setTimeout(() => {
            const query = searchInput.value.trim();
            if (query) {
                fetchFunction(query)
                    .then(results => {
                        onResults(results);
                    })
                    .catch(error => {
                        console.error("Error fetching results:", error);
                    });
            } else {
                onResults([]);
            }
        }, 1000); 
    });
};

