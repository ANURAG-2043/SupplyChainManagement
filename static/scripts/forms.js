var modal = document.getElementById("register-modal");

var link = document.getElementById("register-link");

var span = document.getElementsByClassName("close")[0];

//trigger register link
link.onclick = function(event) {
    event.preventDefault(); 
    modal.style.display = "block";
}
//close button clicked
span.onclick = function() {
    modal.style.display = "none";
}
//when clicked outside any where of the pop up
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

