const socketMiddleware = (io) => (req, res, next) => {
    req.mySocket = io;
    next();
  };

module.exports = socketMiddleware