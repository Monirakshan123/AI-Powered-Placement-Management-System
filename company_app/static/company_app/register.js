const menuBtn =
document.getElementById("menuBtn");


const menu =
document.getElementById("menu");



menuBtn.onclick=function(){


if(menu.style.display==="flex"){

menu.style.display="none";

}

else{

menu.style.display="flex";

}


}





// DARK MODE


const themeBtn =
document.getElementById("themeBtn");


themeBtn.onclick=function(){


document.body.classList.toggle("dark");


themeBtn.innerHTML =
document.body.classList.contains("dark")
? "☀️"
: "🌙";


}




// PASSWORD VALIDATION


const form =
document.getElementById("registerForm");


form.addEventListener(
"submit",
function(event){


event.preventDefault();



let password =
document.getElementById("password").value;


let confirm =
document.getElementById("confirmPassword").value;


let error =
document.getElementById("error");



if(password.length < 8){


error.innerHTML =
"Password must contain at least 8 characters";

return;


}



if(password !== confirm){


error.innerHTML =
"Password and Confirm Password do not match";

return;


}



error.style.color="green";

error.innerHTML =
"Registration Successful 🚀";



});