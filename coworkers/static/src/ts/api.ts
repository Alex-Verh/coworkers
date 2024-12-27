import { showAlert } from "./functions";
import { Language, Nationality } from "./interfaces";


const csrfTokenElem = document.querySelector('meta[name="csrf-token"]') as HTMLElement | null;
let csrfToken = "";
if (csrfTokenElem) {csrfToken = csrfTokenElem.getAttribute('content') as string | ""};


export const fetchWorkerTrait = (idValue : string, traitScore: string, onSuccess: Function) => {
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
    .catch((error) => {
        console.error('Error saving data:', error);
    
        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error");
            });
        };
    });
};


export const fetchOwnLanguage = async (): Promise<Array<Language>> => {
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
    }
};


export const fetchSearchLanguage = async (language: string): Promise<Array<Language>> => {
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
    }
};


export const fetchAddLanguage = async (languageId: number): Promise<void> => {
    try {
        const response = await fetch('/languages/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ language_id: languageId }),
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
    }
};


export const fetchDeleteLanguage= async (languageId: number): Promise<void> => {
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
    }
};


export const fetchOwnNationality = async (): Promise<Array<Nationality>> => {
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
    }
};

export const fetchSearchNationality = async (nationality: string): Promise<Array<Nationality>> => {
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
    }
};


export const fetchAddNationality = async (nationalityId: number): Promise<void> => {
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
    }
};


export const fetchDeleteNationality = async (nationalityId: number): Promise<void> => {
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
    }
};