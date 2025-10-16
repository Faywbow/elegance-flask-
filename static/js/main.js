document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("imageModal");
    if (modal) {
        const modalImg = document.getElementById("modalImage");
        const closeBtn = modal.querySelector(".close");

        document.querySelectorAll(".zoomable").forEach(img => {
            img.addEventListener("click", () => {
                modal.style.display = "flex";
                modalImg.src = img.src;
            });
        });

        const closeModal = () => {
            modal.style.display = "none";
        };

        closeBtn.onclick = closeModal;

        modal.addEventListener("click", (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
});
