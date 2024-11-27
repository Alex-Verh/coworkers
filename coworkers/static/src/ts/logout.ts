import "../css/logout.css";
import "../css/base.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import { enableModal, closeAlert } from "./functions";


document.addEventListener("DOMContentLoaded", () => {

    // enable all modals for this page
    enableModal('contact-form');
    closeAlert();
});