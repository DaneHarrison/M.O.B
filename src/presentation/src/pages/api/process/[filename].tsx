import { type NextApiRequest, type NextApiResponse } from "next";
import { PythonShell } from "python-shell";

async function get_data(options: any) {
  let result = new Promise((resolve, reject) => {
    PythonShell.run("test.py", options, function (err, result) {
      if (err) return reject(err);
      if (result) {
        return resolve(result[0]);
      }
    });
  });

  return result;
}

async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}


// handler
// processes file string on /api/process end point
export default async function handler(req: NextApiRequest, res: NextApiResponse) {

  const {filename} = req.query
  //console.log(`file$ ${filename}`)
  let imgString: string = "";
  let result :any ;
  let options = { args: [filename] };
  // runPython({args:["9_1.jpg"]})
  await get_data(options).then((name) => {
    result = name
    //console.log(name)
  });
  
 // console.log(result)
 



  res.status(200).json({result})
}
