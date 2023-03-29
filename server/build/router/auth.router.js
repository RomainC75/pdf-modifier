const router = require("express").Router();
const User = require("../models/user.model");
const AuthorizedUser = require("../models/authorizedUser.model");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");

router.get("/signup", (req, res, next) => {
  try {
    res.render("signup");
  } catch (error) {
    next(error);
  }
});

router.get("/login", (req, res, next) => {
  try {
    res.render("login");
  } catch (error) {
    next(error);
  }
});

router.post("/signup", async (req, res, next) => {
  try {
    const { email, password } = req.body;

    const foundAuthorizedUser = await AuthorizedUser.findOne({ email });
    if (!foundAuthorizedUser) {
      return res
        .status(400)
        .json({ message: "email not authorized ! contact the admin :-)" });
    }

    foundUser = await User.findOne({ email });
    if (foundUser !== null) {
      return res
        .status(400)
        .json({ message: "user already exists ! try another one!" });
    }
    const salt = await bcrypt.genSalt(10);
    const hash = await bcrypt.hash(password, salt);
    const emailValidationCode = Math.random() * 1000;

    const ans = await User.create({
      email,
      password: hash,
      emailValidationCode,
    });
    console.log(" ==> user ans : ", ans);
    res.redirect("/auth/login");
    // const emailToken = jwt.sign(
    //   { email: email, emailValidationCode, id:ans._id},
    //   process.env.TOKEN_SECRET,
    //   { expiresIn: "3d" }
    // );

    // sendEmail(
    //   email,
    //   "email verification",
    //   "email verification",
    //   `<h1>${'isadmin' in req.headers && req.headers.isadmin==='true' ? 'Admin' : 'User'} mail validation</h1><b>Awesome Message</b> <a href="${process.env.BACKENDADDRESS}/emailconfirmation/${emailToken}">Click on the link below :</a>`
    // );
  } catch (e) {
    next(e);
  }
});

router.post("/login", async (req, res, next) => {
  try {
    console.log("===> BODY : ", req.body)
    if (!("email" in req.body) || !("password" in req.body)) {
      return res.status(422).json({ message: "need an email or a password" });
    }
    console.log("xxxxx2")
    
    const foundUser = await User.findOne({ email: req.body.email });
    console.log("==> found User : ", foundUser)
    if (!foundUser) {
        return res.status(401).json({ message: "wrong email or password" });
    }
    console.log("xxxxx3")

    const isPasswordValid = await bcrypt.compare(req.body.password, foundUser.password);
    console.log("===>", req.body.password, isPasswordValid)
    console.log("found User : " , foundUser)
    if (!isPasswordValid) {
      return res.status(401).json({ message: "wrong email or password" });
    }

    const token = jwt.sign(
      {
        email: foundUser.email,
        id: foundUser._id,
      },
      process.env.TOKEN_SECRET,
      { expiresIn: "3d" }
    );


    res.status(200).json({ message: "authorized", token });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
