var config = require('/config/config.json');
var cors = require('cors');
var express = require('express');
var path = require('path');
var passport = require('passport');
var bodyParser = require('body-parser');

var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

require('./models/main').connect(config.mongoDbUri);

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));


// Load passport strategies
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// Todo: remove this after development is done.
app.use(cors());

// Below code is to bypass CORS error during development. If using above cors module, no need to have below code
// app.all('*', function (req, res, next) {
//   res.header("Access-Control-Allow-Origin", "*");
//   res.header("Access-Control-Allow-Headers", "X-Requested-with");
//   next();
// });


app.use('/', index);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  res.send('404 Not Found');
});

module.exports = app;
