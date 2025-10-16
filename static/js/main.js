document.addEventListener("DOMContentLoaded", () => {
    // Zoom image modal functionality
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const closeBtn = document.querySelector(".close");

    document.querySelectorAll(".zoomable").forEach(img => {
        img.addEventListener("click", () => {
            modal.style.display = "flex"; // Utiliser flex pour centrer l'image
            modalImg.src = img.src;
            document.body.style.overflow = 'hidden'; // Empêche le défilement de la page
        });
    });

    // Fermer le modal
    const closeModal = () => {
        modal.style.display = "none";
        document.body.style.overflow = 'auto'; // Réactive le défilement
    };

    closeBtn.onclick = closeModal;

    modal.onclick = function(e) {
        if (e.target === modal) {
            closeModal();
        }
    };
});
