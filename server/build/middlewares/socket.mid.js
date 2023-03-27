const socketMiddleware = (io) => (req, res, next) => {
    req.myIo = io;
    next();
  };

module.exports = socketMiddleware