require('dotenv').config();

const express = require('express');
const cors = require("cors");
const path = require('path');
const jobs = require('./src/routes/jobsRoutes');
const sites = require('./src/routes/siteRoutes');

// create express app
const app = express();

app.use(cors());

// parse application/json
app.use(express.json());

// parse application/xwww-
app.use(express.urlencoded({ extended: true }));

// view engine setup
app.set('views', path.join(__dirname, 'src/views'));
app.set('view engine', 'pug')

// Setup server port
const port = process.env.PORT;

app.use(express.static(path.join(__dirname, 'src/public')));

// define a root route
app.get('/', (req, res) => {
  res.send("Hello World");
});

app.use('/jobs', jobs);

app.use((req, res, next) => {
  const error = new Error("Not found");
  error.status = 404;
  next(error);
});

app.use((error, req, res, next) => {
  res.status(error.status || 500);
  res.render('error');
});
  
// listen for requests
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

module.exports = app;
