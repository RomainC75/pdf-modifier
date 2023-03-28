const displayReport = (data) =>{
    document.getElementsByClassName("report")[0].style.display="flex"
    document.getElementsByClassName("pdf_handled")[0].textContent=data.pdf_handled
    document.getElementsByClassName("no_errors")[0].textContent=data.no_errors
    document.getElementsByClassName("errors")[0].textContent=data.errors
}

window.onload = function () {
    let socketid = undefined;

    const sockett = io("http://localhost:5000", { path: "/socket.io" });
    const socket = io("http://localhost:5000");

    let progressBar = document.getElementById("progressBar");

    socket.on("connect", function () {
      console.log("Connected!");
      socketid = socket.id;
      console.log("ID: " + socketid);
    });
    socket.on("progression", function (perecent) {
      //do something with percent
      console.log("Got perecent: " + perecent);
      progressBar.style.width = perecent + "%";
    });
    socket.on("report", function (report) {
      //do something with percent
      console.log("==> REPORT : " + report);
      console.log("xxx : ", Object.keys(report))
      console.log(report.pdf_handled, report.no_errors, report.errors)
      displayReport(report)
    });

    let mainForm = document.getElementById("mainForm");
    const input = document.getElementById("fileInput");
    console.log("input : ", input.files);

    mainForm.onsubmit = function (event) {
      event.preventDefault();
      console.log("event", event)
      const data = new FormData()
      
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