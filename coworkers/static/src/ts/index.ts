import "../css/index.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal } from "./functions";

interface User {
    id: number;
    full_name: string;
    position: string;
    experience: number;
}

interface FetchResponse {
    users: User[];
    has_next: boolean;
}

document.addEventListener("DOMContentLoaded", () => {

   
    // enable all modals for this page
    enableModal('contact-form');
    

    // loading more users button
    const loadBtn = document.getElementById('load-more') as HTMLButtonElement | null;

    if (loadBtn && !loadBtn.classList.contains("button_disabled")) {
        loadBtn.addEventListener('click', function onClick() {
            const page = loadBtn.getAttribute('data-page') as string | null;
    
            if (!page) return;

            fetch(`/?page=${page}`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then((response): Promise<FetchResponse> => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                const userList = document.getElementById('user-list') as HTMLElement | null;

                if (!userList) return;

                data.users.forEach((user: User) => {
                    const userHTML = `
                    <a href="/profile/${user.id}/">
                        <div class="search_profile">
                            <div class="row align-items-center">
                                <div class="col-md-3">
                                    <div class="profile_information">
                                        <div class="profile_name">${user.full_name}</div>
                                        <div class="profile_position">${user.position}</div>
                                        <div class="profile_experience">${user.experience} year experience</div>
                                    </div>
                                </div>
                                <div class="col-md-9">
                                    <div class="profile_description">
                                        Some additional details about ${user.full_name}.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </a>`;
                    userList.insertAdjacentHTML('beforeend', userHTML);
                });

                if (data.has_next) {
                    loadBtn.setAttribute('data-page', (parseInt(page) + 1).toString());
                } else {
                    loadBtn.classList.remove("button");
                    loadBtn.classList.add("button_disabled");
                    loadBtn.removeEventListener('click', onClick);  
                }
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
            });
        });
    }
});