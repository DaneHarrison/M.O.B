/*
   [filename].tsx
   an api dynamic route that accepts a query string of an image name 
   and converts the image bytes into a string the db server can understand
*/

import axios from "axios";
import { type NextApiRequest, type NextApiResponse } from "next";
import { PythonShell } from "python-shell";


async function getFromServer(config:any) {
  let data = new Promise((resolve) => {
      axios(config).then(function(response){
          return resolve(response.data);
      })
  });

  return data;
}


async function postData(url: string, data: string) {
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ Photo: data }),
  }).then((response)=>{
    response.json()
  }).then(
    data => console.log(data)
  )
}


/*
   get_data
   runs a python script to convert image data to a string
   options contains arg parameter of image path
   returns image string
*/
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


/*
   handler
   handles api requests made by clients for image string conversion
   req ,is the user req to server
   res, is the response object to respond to client request
*/
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const {filename} = req.query
  let result :any ;
  let options = { args: [filename] };
  await get_data(options).then((name) => {
    result = name 
  });

   
  let optionsReq = {
    method: 'post',
    url: 'http://127.0.0.1:5000/',
    data: {
        Photo:result
    }
  }

  console.log(getFromServer(optionsReq))

  res.status(200).json({result})
}
