const Koa = require('koa');
const Router = require('@koa/router');
const multer = require('@koa/multer');

const app = new Koa();
const router = new Router();
const upload = multer(); // note you can pass `multer` options here

// add a route for uploading multiple files
router.post(
  '/',
  upload.fields([
    {
      name: 'file',
      maxCount: 1
    },
    {
      name: 'file2',
      maxCount: 2
    }
  ]),
  ctx => {
    console.log('ctx.request.files', ctx.request.files);
    console.log('ctx.files', ctx.files);
    console.log('ctx.request.body', ctx.request.body);
    ctx.body = JSON.stringify({form:ctx.request.body});
    ctx.set({"content-type":"application/json"})
  }
);

// add the router to our app
app.use(router.routes());
app.use(router.allowedMethods());

// start the server
app.listen(6000);
