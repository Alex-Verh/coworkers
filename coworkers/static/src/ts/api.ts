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

export const fetchLanguage = (language: string) => {
    fetch(`/language/?name=${encodeURIComponent(language)}`, {
        method: "GET",
        headers: {
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

        console.log("Languages:", data.results);
        data.results.forEach((language: Language) => {
            console.log(language.language_id);
            console.log(language.language_name);
        })

    })
    .catch((error) => {
        console.error('Error searching languages:', error);
    
        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error");
            });
        };
    });
}

export const fetchNationality = (nationality: string) => {
    fetch(`/nationality/?name=${encodeURIComponent(nationality)}`, {
        method: "GET",
        headers: {
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

        console.log("Nationalities:", data.results);
        data.results.forEach((nationality: Nationality) => {
            console.log(nationality.nationality_id);
            console.log(nationality.nationality_name);
        })

    })
    .catch((error) => {
        console.error('Error searching nationality:', error);
    
        if (error.messages && Array.isArray(error.messages)) {
            error.messages.forEach((msg: string) => {
                showAlert(msg, "error");
            });
        };
    });
}


