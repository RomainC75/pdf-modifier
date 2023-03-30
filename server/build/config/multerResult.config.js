const multer = require('multer');
const { v1:uuidv1 } = require('uuid');

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, './build/results'); 
  },
  filename: function (req, file, cb) {
    const new_name=uuidv1()+'.zip'

    console.log('====>multer : filename : ', new_name)
    cb(null, new_name); 
  },
});

module.exports = multer({storage: storage}).single('file')