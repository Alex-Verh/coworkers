export interface User {
    id: number;
    full_name: string;
    position: string;
    experience: number;
}

export interface FetchResponse {
    users: User[];
    has_next: boolean;
}

export interface Language {
    language_id: number;
    language_name: string;
}

export interface Nationality {
    nationality_id: number;
    nationality_name: string;
}