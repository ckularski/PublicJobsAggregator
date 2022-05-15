const dbConn = require('../../config/db.config');

const queryableColumns = ['jobid', 'title', 'location','department'];
const sortableColumns = ['jobid', 'title', 'location'];

exports.findAll = function (req, res, limit, offset, page) {
    let base = 'where 1=1';
    let sortBy = ' order by ';

    let qParams = req.query
    for (p in qParams) {
        if (qParams[p]){
            if (queryableColumns.includes(p)) {
                base+= ' and ' + p + ' like \'%' + qParams[p] + '%\''
            }else if(p!='sort'){
                console.log("error: Invalid query parameter");
            }
        }
    }
    if(!!qParams.sort){
        if(sortableColumns.includes(qParams.sort))
            sortBy+=qParams.sort;
    }
    
    let q =  'Select * from jobs '+ base + (sortBy==' order by '?"":sortBy) +" limit " + limit + " offset " + offset;
    let pageCountQ = "SELECT count(*) as cnt FROM jobs " + base;
    dbConn.query(pageCountQ, function (err, pageCount) {
        if (err) {
            console.log("error: ", err);
        }
        else {
            dbConn.query(q, function (err, results) {
                if (err) {
                    console.log("error: ", err);
                }else {
                    console.log(pageCount[0].cnt);
                    let jsonResult = {
                        'pageSize': limit,
                        'total': pageCount[0].cnt,
                        'pageNumber': page,
                        'data': results,
                        'req': (req.originalUrl.split("?")[1]==undefined ? '' : "?" + req.originalUrl.split("?")[1])
                    }
                    res.render('index', jsonResult);
                    
                }
            });
        }
    });
    
};