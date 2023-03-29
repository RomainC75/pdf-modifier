const displayReport = (data) => {
  document.getElementsByClassName("report")[0].style.display = "flex";
  document.getElementsByClassName("pdf_handled")[0].textContent =
    data.pdf_handled;
  document.getElementsByClassName("no_errors")[0].textContent = data.no_errors;
  document.getElementsByClassName("errors")[0].textContent = data.errors;
};

window.onload = function () {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location = "/auth/login";
  }
  fetch("/auth/verify", {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((raw) => {
      if(raw.status!=200){
        localStorage.removeItem("token")
        window.location = "/auth/login";
        return
      }  
      return raw.json()
    })
    .catch((error) => console.log("veriy : ", error));

  let socketid = undefined;
  const url = window.location.href;
  console.log("url : ", url);
  const sockett = io(url, { path: "/socket.io" });
  const socket = io(url);

  let progressBar = document.getElementById("progressBar");

  socket.on("connect", function () {
    socketid = socket.id;
    console.log("connected ! ID: " + socketid);
  });
  socket.on("progression", function (perecent) {
    console.log("Got perecent: " + perecent);
    progressBar.style.width = perecent + "%";
  });
  socket.on("report", function (report) {
    console.log("==> REPORT : " + report);
    console.log(report.pdf_handled, report.no_errors, report.errors);
    displayReport(report);
  });

  let mainForm = document.getElementById("mainForm");
  const input = document.getElementById("fileInput");
  console.log("input : ", input.files);

  mainForm.onsubmit = function (event) {
    event.preventDefault();
    console.log("event", event);
    const data = new FormData();
    for (const file of input.files) {
      data.append("files", file, file.name);
    }
    console.log("=> data : ", data);
    const date = document.querySelector('input[name="date"]:checked').value;
    fetch(`/process-pdf/${socketid}/${date}`, {
      method: "POST",
      body: data,
    }).then((response) => {
      setTimeout(function () {
        progressBar.style.width = "0%";
      }, 1000);
    });
  };
};
