let timerout;

function resetTimer() {
    clearTimeout(timerout);
    localStorage.removeItem("sesssionExpire");
    timerout = setTimeout(logoutUser, 10 * 60 * 1000); 
}
function logoutUser(){

    localStorage.setItem("sesssionExpire", "true");

        Swal.fire({
        title: "ອອກຈາກລະບົບ",
        text: "ອອກຈາກລະບົບເນື່ອງຈາກບໍ່ໄດ້ໃຊ້ງານ 10 ນາທີແລ້ວ",
        icon: "warning",
        confirmButtonText: "ຕົກລົງ",
        allowOutsideClick: false,  
        allowEscapeKey: false,
          customClass: {
            title: 'lao-font',
            htmlContainer: 'lao-font',
            confirmButton: 'lao-font'
            }
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/login/";
        }
    });
}
function logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("department");
    localStorage.removeItem("department_name");
    localStorage.removeItem("sesssionExpire");
    window.location.href = "/login/";
}
window.onload = function(){
    if (localStorage.getItem("sesssionExpire") === "true") {
        logoutUser();
    } else {
        resetTimer();
    }

};
document.onmousemove = resetTimer;
document.onkeypress = resetTimer;
document.onscroll = resetTimer;
document.onclick = resetTimer;

