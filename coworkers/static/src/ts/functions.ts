import { User, Language, Nationality } from "./interfaces";


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
            return;
        }

        const alert = closeBtn.parentElement as HTMLElement | null;
        if (!alert) return;

        alert.classList.add('none');
        closeBtn.removeEventListener('click', onClick);
    })
}

export const showAlert = (message: string, type: string, priority: boolean = false) => {
    const style = priority ? 'z-index: 10000;' : '';

    const alertElement = document.createElement("div");
    alertElement.style.cssText = style;
    alertElement.className = `palert palert_${type} d-flex align-items-center justify-content-center`;
    alertElement.innerHTML = `
        <img src="/static/public/icons/close_alert.svg" alt="Close" class="palert_close">
        <div class="palert_text">${message}</div>
    `;
    
    document.body.insertAdjacentElement("afterbegin", alertElement);

    // Automatically remove the alert after 3 seconds
    setTimeout(() => {
        alertElement.classList.add("fade-out");
        setTimeout(() => {
            alertElement.remove();
        }, 1500);
    }, 3000); 

    const closeButton = alertElement.querySelector(".palert_close");
    if (closeButton) {
        closeButton.addEventListener("click", () => {
            alertElement.remove();
        });
    }
};

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

export const renderNationality = (nationality: Nationality, action: string, div: HTMLElement) => {
    div.insertAdjacentHTML(
        "afterbegin", 
        `<div class="col-md-6 d-flex justify-content-between align-items-center" data-id="${nationality.nationality_id}" data-name="${nationality.nationality_name}">
            <span class="nationality">${nationality.nationality_name}</span>
            <span class="result_${action.toLowerCase()}">${action}</span>
        </div>`
    );
};

export const renderLanguage = (language: Language, action: string, div: HTMLElement) => {
    div.insertAdjacentHTML(
        "afterbegin",
        `
        <div class="row language d-flex align-items-center" data-id="${language.language_id}" data-name="${language.language_name}">
            <div class="col-md-4 d-flex justify-content-start">${language.language_name}</div>
            <div class="col-md-2 pmodal_level level_select">Beginner</div>
            <div class="col-md-2 pmodal_level">Professional</div>
            <div class="col-md-2 pmodal_level pmodal_level_active">Native</div>
            <div class="col-md-2 result_${action.toLowerCase()}">${action}</div>
        </div>
        `
    );
};

export const renderFilterLanguage = (language: Language, div: HTMLElement) => {
    div.insertAdjacentHTML(
        "beforeend",
        `
        <div class="searchbar_result" data-value="${language.language_id}">${language.language_name}</div>
        `
    );
};

export const renderWorker = (worker: User, div: HTMLElement) => {
    div.insertAdjacentHTML(
        "beforeend",
        `
        <a href="/profile/${worker.id}">
            <div class="search_profile">
                <div class="row align-items-center">
                <div class="col-md-3">
                    <div class="profile_information">
                    <div class="profile_name">${worker.full_name}</div>
                    <div class="profile_position">${worker.position}</div>
                    <div class="profile_experience">${worker.experience} year experience</div>
                    </div>
                </div>
                <div class="col-md-9">
                    <div class="profile_description">
                    Some additional details about this idiot.
                    </div>
                </div>
                </div>
            </div>
            </a>
        `
    );
};

const handleEntityClick = (
    e: MouseEvent,
    addedEntities: Set<number>,
    addedDiv: HTMLElement,
    fetchAddEntity: Function,
    fetchDeleteEntity: Function,
    renderEntity: Function,
    addedClassName: string
) => {
    const target = e.target as HTMLElement;
    const container = target.closest("[data-id]");
    if (!container) return;

    const entityId = Number(container?.getAttribute("data-id"));
    const entityName = String(container?.getAttribute("data-name"));

    if (target.classList.contains("result_remove")) {
        addedEntities.delete(entityId);
        container?.remove();
        fetchDeleteEntity(entityId);
    } else if (target.classList.contains("result_add")) {
        if (addedEntities.size === 0) {
            addedDiv.innerHTML = '';
        }

        addedEntities.add(entityId);
        fetchAddEntity(entityId);
        renderEntity({ [`${addedClassName}_id`]: entityId, [`${addedClassName}_name`]: entityName }, "Remove", addedDiv);
        container?.remove();
    }
};

type FetchNoParamEntitiesFunction = () => Promise<any[]>;
type FetchEntitiesFunction = (query: string) => Promise<any[]>;
type FetchEntityFunction = (entityId: number) => Promise<void>;
type RenderEntityFunction = (entity: any, action: string, container: HTMLElement) => void;

export const initializeEntityModal = (
    searchElement: HTMLInputElement,
    fetchOwnEntities: FetchNoParamEntitiesFunction,
    fetchSearchEntities: FetchEntitiesFunction,
    fetchAddEntity: FetchEntityFunction,
    fetchDeleteEntity: FetchEntityFunction,
    renderEntity: RenderEntityFunction,
    addedClassName: string,
    searchedClassName: string
) => {
    const parentDiv = document.querySelector(`.${addedClassName}_result`) as HTMLElement;
    if (!parentDiv) return;

    const addedDiv = parentDiv.querySelector(`.${addedClassName}_added`) as HTMLElement;
    const searchedDiv = parentDiv.querySelector(`.${searchedClassName}_searched`) as HTMLElement;
    const addedEntities = new Set<number>();

    if (!addedDiv || !searchedDiv) return;

    fetchOwnEntities()
        .then((results: any) => {
            if (results.length === 0) {
                addedDiv.innerHTML = `No ${addedClassName} indicated at the moment.`;
                return;
            }

            results.forEach((entity: any) => {
                addedEntities.add(entity[`${addedClassName}_id`]);
                renderEntity(entity, "Remove", addedDiv);
            });
        })
        .catch((error: any) => {
            console.error(`Error fetching initial ${addedClassName}s:`, error);
        });

    parentDiv.addEventListener("click", (e) =>
        handleEntityClick(e, addedEntities, addedDiv, fetchAddEntity, fetchDeleteEntity, renderEntity, addedClassName)
    );

    applySearchListener(searchElement, fetchSearchEntities, (results) => {
        searchedDiv.innerHTML = '';
        results.forEach((result: any) => {
            if (!addedEntities.has(result[`${addedClassName}_id`])) {
                renderEntity(result, "Add", searchedDiv);
            };
        });
    });
};

export const showLoading = () => {
    const loadingDiv = document.createElement('div');

    loadingDiv.className = 'loading d-flex align-items-center justify-content-center';
    loadingDiv.innerHTML = `
      <img src="/static/public/icons/loading.svg" alt="Loading" class="loading-icon" />
    `;

    document.body.appendChild(loadingDiv);

    document.body.style.overflow = 'hidden';
};

export const hideLoading = () => {
    const loadingDiv = document.querySelector('.loading');
    if (loadingDiv) {
        loadingDiv.remove();
    }

    document.body.style.overflow = '';
};

    

