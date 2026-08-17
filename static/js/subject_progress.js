document.addEventListener("DOMContentLoaded", function () {

    const progressBar = document.querySelector(
        ".subject-progress-fill"
    );

    if (!progressBar) {
        return;
    }

    const progress = parseInt(
        progressBar.dataset.progress,
        10
    );

    progressBar.style.width = progress + "%";
});