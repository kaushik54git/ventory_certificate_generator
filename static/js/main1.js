function validateForm() {
    var name = document.getElementById('nameInput').value;
    var id = document.getElementById('idInput').value;

    // Check if either NAME or ID is filled
    if (!name && !id) {
        alert("Please fill in either NAME or ID.");
        return false; // Prevent form submission
    }
    return true; // Allow form submission
}