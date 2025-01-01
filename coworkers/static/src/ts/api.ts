import { showAlert, showLoading, hideLoading } from "./functions";
import { Language, Nationality, Experience} from "./interfaces";


const csrfTokenElem = document.querySelector('meta[name="csrf-token"]') as HTMLElement | null;
let csrfToken = "";
if (csrfTokenElem) {csrfToken = csrfTokenElem.getAttribute('content') as string | ""};




    export const fetchPfp = async (formData: FormData, profileImage: HTMLImageElement) => {
        showLoading();

        try {
            const response = await fetch('/profile', {
                method: 'POST',
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken,
                }
            });

            if (response.ok) {
                const contentType = response.headers.get('Content-Type');
                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();

                    if (data.url) {
                        profileImage.src = data.url;
                    } else {
                        showAlert('Failed to update the profile picture.', 'error');
                    }

                    if (data.message) {
                        showAlert(data.message, "success");
                    }
                } else {
                    showAlert('Unexpected server response, expected JSON but received HTML.', 'error');
                }
        } else {
            showAlert('Failed to upload the profile picture.', 'error');
        }
        } catch (error:any) {
            console.error("An error occurred while fetching data:", error);

            if (error.messages && Array.isArray(error.messages)) {
                error.messages.forEach((msg: string) => {
                    showAlert(msg, "error");
                });
            };
            return [];
        } finally {
            hideLoading();
        }
    }      


export const fetchWorkers = async (params: URLSearchParams) => {
    showLoading();

    try {
        const response = await fetch(`/?${params.toString()}`, {
            method: "GET",
            headers: {
                "x-requested-with": "XMLHttpRequest",
            },
        });

        if (!response.ok) {
            console.error("Failed to fetch data:", response.statusText);
            return [];
        }

        const data = await response.json();

        if (data.users) {

            return data;
            
        } else {
            console.warn("No user data found.");
            showAlert("No workers found for applied filters.", "error")
            return [];
        }

        
    } catch (error:any) {
        console.error("An error occurred while fetching data:", error);

        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error");
            });
        };
        return [];
    } finally {
        hideLoading();
    }
}


export const fetchWorkerTrait = (idValue : string, traitScore: string, onSuccess: Function) => {
    showLoading();

    try{
        fetch(`/worker-trait/`, {
            method: "POST",
            body: JSON.stringify({
                trait_id: idValue,
                trait_score: traitScore,
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
            onSuccess();
        
            if (data.messages && Array.isArray(data.messages)) {
                data.messages.forEach((msg: string) => {
                    showAlert(msg, "success");
                });
            }
        })
    } catch(error: any) {
        console.error('Error saving data:', error);
    
        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error");
            });
        };
    } finally {
        hideLoading();
    }
};


export const fetchOwnLanguage = async (): Promise<Array<Language>> => {
    showLoading();

    try {
        const response = await fetch(`/languages/own/`, {
            method: "GET",
            headers: {
                "X-CSRFToken": csrfToken,
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        const languages = data.results as Array<Language>;

        if (!languages || languages.length == 0) {
            return [];
        }

        return languages;
    } catch (error: any) {
        console.error("Error searching for own languages:", error);

        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }

        return [];
    } finally {
        hideLoading();
    }
};


export const fetchSearchLanguage = async (language: string): Promise<Array<Language>> => {
    showLoading();

    try {
        const response = await fetch(`/languages/?name=${encodeURIComponent(language)}`, {
            method: "GET",
            headers: {
                "X-CSRFToken": csrfToken,
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        const languages = data.results as Array<Language>;

        if (!languages || languages.length == 0) {
            showAlert("No languages found for such query.", "error", true);
            return [];
        }

        return languages;

    } catch (error: any) {
        console.error("Error searching languages:", error);

        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }

        return [];
    } finally {
        hideLoading();
    }
};


export const fetchAddLanguage = async (entityId: number, knowledge: string): Promise<void> => {
    showLoading();

    try {
        const response = await fetch('/languages/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                language_id: entityId,
                language_knowledge: knowledge,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to add language.");
        }

        const data = await response.json();
        console.log(data.message);
        showAlert(data.message, "success", true);


    } catch (error: any) {
        
        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }
    } finally {
        hideLoading();
    }
};


export const fetchDeleteLanguage= async (languageId: number): Promise<void> => {
    showLoading();

    try {
        const response = await fetch('/languages/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ language_id: languageId }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to delete language.");

        }

        const data = await response.json();
        showAlert(data.message, "success", true);


    } catch (error: any) {
        
        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }
    } finally {
        hideLoading();
    }
};


export const fetchOwnNationality = async (): Promise<Array<Nationality>> => {
    showLoading();

    try {
        const response = await fetch(`/nationalities/own/`, {
            method: "GET",
            headers: {
                "X-CSRFToken": csrfToken,
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        const nationalities = data.results as Array<Nationality>;

        if (!nationalities || nationalities.length == 0) {
            return [];
        }

        return nationalities;
    } catch (error: any) {
        console.error("Error searching for own nationalities:", error);

        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }

        return [];
    } finally {
        hideLoading();
    }
};

export const fetchSearchNationality = async (nationality: string): Promise<Array<Nationality>> => {
    showLoading();

    try {
        const response = await fetch(`/nationalities/?name=${encodeURIComponent(nationality)}`, {
            method: "GET",
            headers: {
                "X-CSRFToken": csrfToken,
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        const nationalities = data.results as Array<Nationality>;

        if (!nationalities || nationalities.length == 0) {
            showAlert("No nationalities found for such query.", "error", true);
            return [];
        }

        return nationalities;
    } catch (error: any) {
        console.error("Error searching nationality:", error);

        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }

        return [];
    } finally {
        hideLoading();
    }
};


export const fetchAddNationality = async (nationalityId: number): Promise<void> => {
    showLoading();

    try {
        const response = await fetch('/nationalities/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ nationality_id: nationalityId }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to add nationality.");
        }

        const data = await response.json();
        console.log(data.message);
        showAlert(data.message, "success", true);


    } catch (error: any) {
        
        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }
    } finally {
        hideLoading();
    }
};


export const fetchDeleteNationality = async (nationalityId: number): Promise<void> => {
    showLoading();

    try {
        const response = await fetch('/nationalities/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ nationality_id: nationalityId }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to delete nationality.");

        }

        const data = await response.json();
        showAlert(data.message, "success", true);


    } catch (error: any) {
        
        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }
    } finally {
        hideLoading();
    }
};

export async function fetchExperience(experienceId: number): Promise<Experience | null> {
    showLoading();

    try {
        const response = await fetch(`/experience/${experienceId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Error fetching experience with ID ${experienceId}: ${response.statusText}`);
        }

        const data: Experience = await response.json();
        return data;

    } catch (error: any) {
        console.error(error);

        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }

        return null;
    } finally {
        hideLoading();
    }
}

export async function fetchUpdateExperience(experience: Experience) {
    showLoading();

    try {
        const response = await fetch(`/experience/${experience.experience_id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(experience),
        });

        if (!response.ok) {
            throw new Error(`Error updating experience with ID ${experience.experience_id}: ${response.statusText}`);
        }

        await window.location.reload();
        const data = await response.json();
        showAlert(data.message, "success", true);

    } catch (error: any) {
        console.error(error);

        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }

    } finally {
        hideLoading();
    }
}


export const fetchDeleteExperience = async (experienceId: number): Promise<void> => {
    showLoading();

    try {
        const response = await fetch(`/experience/${experienceId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to delete language.");

        }

        const data = await response.json();
        await window.location.reload();
        showAlert(data.message, "success", true);


    } catch (error: any) {
        
        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error", true);
            });
        } else {
            showAlert(error.message || "An unexpected error occurred.", "error", true);
        }
    } finally {
        hideLoading();
    }
};