const fs = require("fs");

module.exports = () => {
  const folderNames = ["./build/public/uploads","./build/results"];
  folderNames.forEach((dir) => {
    console.log(`${dir} exists ? ${fs.existsSync(dir)}`);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}
