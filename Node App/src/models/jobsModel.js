let dbConn = require('../../config/db.config');

//Job object create
let Job = function (job) {
    this.jobId = job.jobId;
    this.link = job.link;
    this.department = job.department;
    this.jobNumber = job.jobNumber;
    this.salaryRange = job.salaryRange;
    this.jobType = job.jobType;
    this.location = job.location;
    this.state = job.state;
    this.description = job.description;
    this.startDate = job.startDate;
    this.pubDate = job.pubDate;
    this.closeDate = job.closeDate;
};

// Job.create = function (newJob, result) {
//     dbConn.query("INSERT INTO jobs set ?", newJob, function (err, res) {
//         if (err) {
//             console.log("error: ", err);
//             result(err, null);
//         }
//         else {
//             console.log(res.insertId);
//             result(null, res.insertId);
//         }
//     });
// };

// Job.findById = function (id, result) {
//     dbConn.query("Select * from jobs where id = ? ", id, function (err, res) {
//         if (err) {
//             console.log("error: ", err);
//             result(err, null);
//         }
//         else {
//             result(null, res);
//         }
//     });
// };
// Job.findAll = function () {
    
// };
// Job.update = function (id, job, result) {
//     dbConn.query("UPDATE jobs SET first_name=?,last_name=?,email=?,phone=?,organization=?,designation=?,salary=? WHERE id = ?", [job.first_name, job.last_name, job.email, job.phone, job.organization, job.designation, job.salary, id], function (err, res) {
//         if (err) {
//             console.log("error: ", err);
//             result(null, err);
//         } else {
//             result(null, res);
//         }
//     });
// };
// Job.delete = function (id, result) {
//     dbConn.query("DELETE FROM jobs WHERE id = ?", [id], function (err, res) {
//         if (err) {
//             console.log("error: ", err);
//             result(null, err);
//         }
//         else {
//             result(null, res);
//         }
//     });
// };
module.exports = Job;