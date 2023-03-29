module.exports = () => {
  const folderNames = ["results", "uploads"];
  const fs = require("fs");
  const dirBase = "./build/public/";
  folderNames.forEach((fName) => {
    const dir = dirBase + fName;
    console.log(`${dir} exists ? ${fs.existsSync(dir)}`);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
};
