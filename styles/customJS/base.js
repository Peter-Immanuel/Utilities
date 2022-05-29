
function loginFunctionality(number){
   if (number === 1){
      document.getElementById("usernameInput").style.display="none"
      document.getElementById("passwordInput").style.display="block"
      document.getElementById("passwordInput").style.animation="fadeIn ease 1.5s 1"

   }
   else if (number === 2){
      document.getElementById("usernameInput").style.display="block"
      document.getElementById("passwordInput").style.display="none"
      document.getElementById("usernameInput").style.animation="fadeIn ease 1.5s 1"
   }
}

