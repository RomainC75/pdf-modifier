const express = require('express');
const Bull = require('bull');
const path = require('path')
const morgan =require("morgan")
const multerConfig = require('./config/multer.config')

const PORT = process.env.PORT || 5000
const REDIS_URL = process.env.REDIS || "redis://redis:6379"


const pdfQueue = new Bull('pdfQueue',REDIS_URL);

const app = express();

app.set('view engine', 'ejs')
app.set('views', path.join(__dirname, 'views'))

app.use(express.json());
app.use(express.urlencoded({ extended: false }))
app.use(morgan('combined'))

app.get('/',(req,res,next)=>{
    res.render("index")
})

app.post('/process-pdf/:socketid', multerConfig.array('files'), async (req, res) => {
  console.log('"=======================================')
  const { pdfData } = req.body;
  console.log('=>', pdfData)
  // add the job to the queue
  await pdfQueue.add({ pdfData });

  res.status(202).json({ message: 'PDF processing job added to queue' });
});

// start the Bull queue worker to process PDF jobs
pdfQueue.process(async (job) => {
  const { pdfData } = job.data;

  // TODO: process the PDF data

  console.log(`Processed PDF with data: ${pdfData}`);
});

// start the Express app
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

