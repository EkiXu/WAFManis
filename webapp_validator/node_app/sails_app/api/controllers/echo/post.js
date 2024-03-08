/**
 * Module dependencies
 */

// ...


/**
 * echo/post.js
 *
 * Post echo.
 */
module.exports = async function post(req, res) {
  return res.json({form:req.body});

};
