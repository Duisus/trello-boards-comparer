let expandButtons = document.querySelectorAll(".trello-compare-report .btn");

for (let button of expandButtons) {
    button.addEventListener("click", handleExpandButtonClick)
}

function handleExpandButtonClick(event) {
    let currentButton = event.currentTarget;
    currentButton.classList.toggle("active");

    let sectionWithDetails = currentButton.parentNode.parentNode;
    let comparisonsList = sectionWithDetails.querySelector(".comparisons");
    animateComparisonsList(comparisonsList)
}

function animateComparisonsList(comparisons) {
    if (comparisons.classList.contains("hidden")) {
        comparisons.classList.remove("hidden");
        setTimeout(function () {
                comparisons.classList.add("active");
            }, 2);
    } else {
        comparisons.classList.remove("active");
        comparisons.addEventListener("transitionend", addHiddenClassOnce);
    }
}

function addHiddenClassOnce(event) {
    let target = event.currentTarget
    target.classList.add("hidden")
    target.removeEventListener("transitionend", addHiddenClassOnce)
}
