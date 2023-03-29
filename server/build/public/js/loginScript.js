window.onload = function () {
  let mainForm = document.getElementById("login_form");

  mainForm.onsubmit = function (event) {
    event.preventDefault();

    console.log("event : ", event.target);
    const email = event.target[0].value;
    const password = event.target[1].value;
    console.log("email : ", email);

    fetch(`/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    })
      .then((raw) => raw.json())
      .then((ans) => {
        console.log("ans : ",ans)
        if('token' in ans){
            localStorage.setItem("token",ans.token)
        }else{
            const errorEl = document.getElementById("error")
            errorEl.textContent=ans.message
        }})
      .catch((error) => {
        console.log("erorr : ", error)
        const errorEl = document.getElementById("error")
            errorEl.textContent=error.message
      });
  };
};
