//Gestión del popup S
var activeModal = undefined;
var addClient = undefined;
var addEmail = undefined;

function toggleModal(modalId) {
    var modal = document.getElementById(modalId);
    // If there's no active modal, just open the modal
    if (activeModal === undefined) {
        activeModal = modal;
        activeModal.style.display = "flex";
    }
    // check if the actual modal is active and the new one is the same, so we close it
    else if (activeModal.style.display === "flex" && activeModal.id == modalId) {
        activeModal.style.display = "none";
        activeModal = undefined;
    }
}

function addOptions() {
    if (addClient === undefined && addEmail === undefined) {
        addClient = document.getElementById("add-client");
        addEmail = document.getElementById("add-email");
        addClient.style.display = "block";
        addEmail.style.display = "block";
    } else {
        addClient.style.display = "none";
        addEmail.style.display = "none";
        addClient = undefined;
        addEmail = undefined;
    }
}

document.addEventListener("DOMContentLoaded", function(event) { 
    window.onclick = function(event) {
        if (event.target == activeModal) {
            activeModal.style.display = "none";
            activeModal = undefined;
             // When the user clicks anywhere outside of the modal, close it
        }
    }
});