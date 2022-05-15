const express = require('express');
const router = express.Router();
const controller = require('../controller/jobsController');

router.get('/', function(req, res, next) {
    let limit = 50
    let page = 1
    let offset = 0
    controller.findAll(req,res,limit,offset,page);
})

router.get('/:page', function(req, res, next) {
    let limit = 50
    let page = req.params.page || 1
    let offset = (page-1)*limit
    controller.findAll(req,res,limit,offset,page);
})

module.exports= router;