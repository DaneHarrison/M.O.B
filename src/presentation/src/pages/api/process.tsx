import axios from "axios";
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
  let imgString: string = "";
  let result :any ;
  let options = { args: ["9_1.jpg"] };
  // runPython({args:["9_1.jpg"]})
  await get_data(options).then((name) => {
    result = name
    //console.log(name)
  });
  // res.status(200).json({ name: name})
  //runPython({args:["9_1.jpg"]})
//  console.log(result)
  const config = { // might need to explicity set a header as sending JSON
    method: 'post',
    url: 'http://localhost:5000/',
    data: result
  }
  console.log(typeof result)
 // postData('http://localhost:5000/photo', { Photo: result })
 // .then((data) => {
   // console.log(data); // JSON data parsed by `data.json()` call
  //});



  res.status(200).json({result})
}
