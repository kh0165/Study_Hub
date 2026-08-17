document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("q");
    const noteCards = document.querySelectorAll(".note-card");
    
    if (!searchInput || !noteCards.length) {
        return;
    }
    
    searchInput.addEventListener("input", function () {
    
        const searchText = this.value.toLowerCase().trim();
    
        noteCards.forEach(function (card) {
    
            const title = card
                .querySelector(".card-item-title")
                .textContent
                .toLowerCase();
    
            const content = card
                .querySelector(".card-item-desc")
                .textContent
                .toLowerCase();
    
            const category = card
                .querySelector(".badge-primary")
                ?.textContent
                .toLowerCase() || "";
    
            const subject = card
                .querySelector(".badge-neutral")
                ?.textContent
                .toLowerCase() || "";
    
            const matches =
                title.includes(searchText) ||
                content.includes(searchText) ||
                category.includes(searchText) ||
                subject.includes(searchText);
    
            card.style.display = matches ? "" : "none";
        });
    });

    
    });
    