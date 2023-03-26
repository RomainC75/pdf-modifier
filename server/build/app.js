const express = require("express");
const Bull = require("bull");
const path = require("path");
const morgan = require("morgan");
const multerConfig = require("./config/multer.config");
const app = express();
const httpServer = require("http").createServer(app);
const { Server } = require("socket.io");
const socketMiddleware = require("./middlewares/socket.mid");
const staticProtectorMid = require("./middlewares/staticProtector.mid");
const errorHandler = require('./error-handling')

const io = new Server(httpServer, {
  cors: {
    origin: "http://localhost:5000",
    methods: ["GET", "POST"],
  },
  path:"/socket.io"
})



const PORT = process.env.PORT || 5000;
const REDIS_URL = process.env.REDIS || "redis://redis:6379";

const pdfQueue = new Bull("pdfQueue", REDIS_URL);

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(staticProtectorMid, express.static(path.join(__dirname, 'uploads')));
app.set('socketio',io)

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use(morgan("combined"));
app.use(socketMiddleware(io))

app.get("/", (req, res, next) => {
  res.render("index");
});


io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

app.post(
  "/process-pdf/:socketId",
  multerConfig.array("files"),
  async (req, res) => {
    console.log('"=======================================>', req.params.socketId);
    
    console.log('=> ', req.files)
    // add the job to the queue
    // await pdfQueue.add({ pdfData });


    let index = 0
    const id = setInterval(()=>{
      const percent = (index+1)/req.files.length*100
      console.log("Percent : ", percent)
      req.mySocket.emit("update progress",percent)

      if(index===req.files.length-1){
        clearInterval(id)
      }
      index++
    },2000)

    

    res.status(202).json({ message: "PDF processing job added to queue" });
  }
);



// start the Bull queue worker to process PDF jobs
pdfQueue.process(async (job) => {
  const { pdfData } = job.data;

  // TODO: process the PDF data

  console.log(`Processed PDF with data: ${pdfData}`);
});

errorHandler(app)

// start the Express app
httpServer.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
