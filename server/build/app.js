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
const errorHandler = require("./error-handling");
const redis = require("redis");

const PORT = process.env.PORT || 5000;
const REDIS_URL = process.env.REDIS_URL || "redis://redis:6379";

const io = new Server(httpServer, {
  cors: {
    origin: "http://localhost:5000",
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

      // let index = 0;
      // const id = setInterval(async () => {
      //   try {
      //     const percent = ((index + 1) / req.files.length) * 100;
      //     console.log("Percent : ", percent);
      //     req.myIo.emit("update progress", percent);

      //     if (index === req.files.length - 1) {
      //       clearInterval(id);
      //     }
      //     // redisClient.publish('pdf-to-handle', 'hello world');
      //     const originalNames = req.files.map(file=>file.originalname)
          
      //     const data = JSON.stringify(req.files[index]["originalname"])
      //     // const data = "bonjour";
      //     await redisClient.rPush("pdf-to-handle", data);

      //     index++;
      //   } catch (error) {
      //     console.log("===> ERROR : ", error)
      //   }
      // }, 2000);
      res.status(202).json({ message: "PDF processing job added to queue" });
    } catch (error) {
      console.log("ERROR : ", error);
    }
  }
);


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
