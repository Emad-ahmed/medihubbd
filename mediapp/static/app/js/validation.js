function formValidation() {

    var phone = document.getElementById("phone").value;


    var phonePattern = /^(\+88|88)?01[3-9]\d{8}$/;


    if (phonePattern.test(phone)) {
        document.getElementById("merror").innerHTML = "";

    } else {
        document.getElementById("merror").innerHTML = "**Phone Number Is Invalid**";
        return false;
    }







}