/*
    Allows Javascript to run Python - connects the server to a database (operations listed below)
    Commands:
        checkDB: Reads and returns information from the database for further processing    
        updateDB: Creates/modifies data in the database
*/
let {PythonShell} = require('python-shell');


class PythonAdapter {

    async runScript(options) {
        let result = new Promise((resolve, reject) => {
            PythonShell.run('training.py', options, function (err, result) {
                if (err) return reject(err);
                return resolve(result)
            });
        });

        return result;
    }
}
 

module.exports = {
    PythonAdapter
}