const mongoose = require("mongoose");
const MONGO_URI = process.env.MONGODB_URI

mongoose
  .connect(MONGO_URI)
  .then((x) => {
    console.log(
      `=> Mongoose is connected ! Database name: "${x.connections[0].name}"`
    );
  })
  .catch((err) => {
    console.error("Error connecting to mongo: ", err);
  });
