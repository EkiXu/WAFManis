const express = require('express')
const multer  = require('multer')
const bodyParser = require('body-parser')
const upload = multer({ dest: 'uploads/' })

const app = express()

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())


app.post('/', upload.single('file'), function (req, res) {
   // req.file is the name of your file in the form above, here 'uploaded_file'
   // req.body will hold the text fields, if there were any
   console.log(req.file, req.body)

   res.setHeader('Content-Type', 'application/json')
   res.end(JSON.stringify({form:req.body}))
});

app.listen(6000)
