module.exports = (req,res,next) =>{
    if(req.url.match(/^\/uploads\//) && req.headers.authorization!==`Bearer ${process.env.STATIC_TOKEN}`){
        next('static => token invalid')
    }
    next()
}