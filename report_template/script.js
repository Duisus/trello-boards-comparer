let expandButtons = document.querySelectorAll(".btn");

for (let button of expandButtons) {
    button.addEventListener("click", handleExpandButtonClick)
}

function handleExpandButtonClick(event) {
    let currentButton = event.currentTarget;
    currentButton.classList.toggle("active");

    let sectionWithDetails = currentButton.parentNode.parentNode;
    let comparisonsList = sectionWithDetails.querySelector(".comparisons");
    comparisonsList.classList.toggle("active");
}
