var multer = require('multer');

Picker.middleware(multer().any());

Picker.route('/', function(params, req, res)
{
  console.log(req.body);
  //console.log(req.files[0]);
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify({form:req.body,files:req.files}));
});
