import "../css/register.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal, closeAlert, showAlert } from "./functions";


document.addEventListener("DOMContentLoaded", () => {

    // enable all modals for this page
    enableModal('contact-form');
    closeAlert();

    const profileImage = document.getElementById('profile-image') as HTMLImageElement;
    const fileInput = document.getElementById('profile_picture') as HTMLInputElement;

    if (profileImage && fileInput) {
        profileImage.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', async () => {
            const file = fileInput.files?.[0];
            if (!file) return;
    
            const allowedExtensions = ['.jpg', '.jpeg', '.png'];
            const fileExtension = file.name.split('.').pop()?.toLowerCase();
            if (!fileExtension || !allowedExtensions.includes(`.${fileExtension}`)) {
                showAlert('Only JPG, JPEG, and PNG formats are accepted.', 'error');
                return;
            }
    
            const reader = new FileReader();
            reader.onload = () => {
                if (reader.result && typeof reader.result === 'string') {
                    profileImage.src = reader.result;
                }
            };
            reader.readAsDataURL(file);
    
        });
    };
});