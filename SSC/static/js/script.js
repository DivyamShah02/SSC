document.addEventListener("keydown", function(event) {
    // If the focused element is an input field of type "number"
    if (event.target.type === "number" && (event.key === "ArrowUp" || event.key === "ArrowDown")) {
        event.preventDefault(); // Prevent default number change
    }
});

function toggleVisibility(element_id) {
    let element = document.getElementById(element_id);
    if (element.style.display === "none") {
        element.style.display = ""; // or "flex", "grid", etc., depending on the layout
    } else {
        element.style.display = "none";
    }
}