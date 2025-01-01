export interface User {
    id: number;
    full_name: string;
    position: string;
    experience: number;
    description: string;
}

export interface FetchResponse {
    users: User[];
    has_next: boolean;
}

export interface Language {
    language_id: number;
    language_name: string;
    language_knowledge: "Beginner" | "Professional" | "Native";
}

export interface Nationality {
    nationality_id: number;
    nationality_name: string;
}

export interface Experience {
    experience_id: number;
    position: string;
    institution_name: string;
    description: string;
    start_year: number;
    end_year: number | null;
    type: "Work" | "Education";
}