const express = require("express");
const Bull = require("bull");
const path = require("path");
const morgan = require("morgan");
const multerConfig = require("./config/multer.config");
const multerResultConfig = require("./config/multerResult.config")
const app = express();
const httpServer = require("http").createServer(app);
const { Server } = require("socket.io");
const socketMiddleware = require("./middlewares/socket.mid");
const staticProtectorMid = require("./middlewares/staticProtector.mid");
const errorHandler = require("./error-handling");
const redis = require("redis");
const {sendEmail} = require("./tools/email")
const missingFolderHandler = require('./tools/missingFolderHandler')

const PORT = process.env.PORT || 5000;
const REDIS_URL = process.env.REDIS_URL || "redis://redis:6379";

missingFolderHandler()

const io = new Server(httpServer, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
  path: "/socket.io",
});

console.log("=> REDIS URL", REDIS_URL)
// const pdfQueue = new Bull("pdfQueue", REDIS_URL);
const redisClient = redis.createClient({ url: REDIS_URL });
const redisClient_progression = redis.createClient({ url: REDIS_URL });
const redisClient_report = redis.createClient({ url: REDIS_URL });

redisClient.on('error', err => console.log('Redis Client Error', err));
redisClient_progression.on('error', err => console.log('Redis Client Error', err));
redisClient_report.on('error', err => console.log('Redis Client Error', err));

redisClient.connect();
redisClient_progression.connect();
redisClient_report.connect();

// , return_buffers: true
redisClient.on('connect', function(){
  console.log('Connected to redis queue instance');
});
redisClient_progression.on('connect', function(){
  console.log('Connected to redis instance : progression');
});
redisClient_report.on('connect', function(){
  console.log('Connected to redis instance : report');
});

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(staticProtectorMid, express.static(path.join(__dirname, "public")));
app.set("socketio", io);

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use(morgan("combined"));
app.use(socketMiddleware(io));

app.get("/", (req, res, next) => {
  res.render("index");
});

io.on("connection", (socket) => {
  console.log("a user connected");
  socket.on("disconnect", () => {
    console.log("user disconnected");
  });
});

app.post(
  "/process-pdf/:socketId/:date",
  multerConfig.array("files"),
  async (req, res) => {
    try {
      console.log(
        '"=======================================>',
        req.params.socketId
      );

      console.log("=> ", req.files);
      console.log("req.body : ", req.params.date)
      const date = req.params.date
      // add the job to the queue
      // await pdfQueue.add({ pdfData });

      const originalNames = req.files.map(file=>file.originalname)
      console.log("ORIGINAL NAMES : ", originalNames)
      await redisClient.rPush("pdf-to-handle", JSON.stringify({originalNames,date}));
      res.status(202).json({ message: "PDF processing job added to queue" });
    } catch (error) {
      console.log("ERROR : ", error);
    }
  }
);

app.post("/upload-result/", staticProtectorMid, multerResultConfig, async(req,res,next)=>{
  try {
    console.log("====> FILE RECEIVED BY SERVER !")
    const filename = req.file.filename
    console.log("====> req.file : ", filename)
    const email = "rom.chenard@gmail.com"
    
    sendEmail(
      email,
      "AER-PDF zip file",
      "AER-PDF zip file :",
      `<h1>Click on this link to get your file : </h1> <a href="${process.env.BACKENDADDRESS}/results/${filename}">Link</a>`
    );
    res.status(201).json({message: "file uploaded"})
  } catch (error) {
    next(error)
  }
})


redisClient_progression.subscribe('progression', (message)=>{
  const values = JSON.parse(message)
  console.log("===========PROGRESSION : ", values)
  const percent = ((parseInt(values[0]) + 1) / parseInt(values[1])) * 100;
  io.emit("progression", percent);
});

redisClient_report.subscribe('report', (message)=>{
  const values = JSON.parse(message)
  io.emit("report", values);
});



errorHandler(app);

// start the Express app
httpServer.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
