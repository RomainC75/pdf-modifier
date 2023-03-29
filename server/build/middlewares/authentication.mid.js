const router = require('express').Router()
const jwt = require('jsonwebtoken')
const User = require('../models/user.model')

router.use( async (req,res,next)=>{
    try{
        const token = req.headers.authorization.split(' ')[1]
        const decodedToken = jwt.verify(token,process.env.TOKEN_SECRET)
        const user = await User.findById(decodedToken.id)
        if(user===null){
            res.status(400).json({message: "wrong Token/user"})
            return 
        }
        req.user = {
            _id:user._id.toString(),
            email: user.email
        }
        next()
    }catch(e){
        res.status(403).json({message : 'not authorized'})
    }
})

module.exports = router