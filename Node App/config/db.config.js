'use strict';
require('dotenv').config();

const mysql = require('mysql2');

//local mysql db connection
const dbConn = mysql.createConnection({
    host     : process.env.DB_HOST,
    port     : process.env.DB_PORT,
    user     : process.env.DB_USER,
    password : process.env.DB_PWD,
    database : process.env.DB_DATABASE
});

dbConn.connect(function(err) {
    if (err) throw err;
    console.log("Database Connected!");
});

module.exports = dbConn;