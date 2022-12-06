/*
   [filename].tsx
   an api dynamic route that accepts a query string of an image name 
   and converts the image bytes into a string the db server can understand
*/

import axios from "axios";
import { type NextApiRequest, type NextApiResponse } from "next";
import { PythonShell } from "python-shell";

/*
  getFromServer
  config param accepts the details of the http requext
  send post request to a server and returns the data in the http body of the response
  returns json string
*/
async function getFromServer(config: any) {
  let data = new Promise((resolve) => {
    axios(config).then(function (response) {
      return resolve(response.data);
    });
  });

  return data;
}

/*
   getDataDecode
   runs a python script to convert image data to a string
   options contains arg parameter of image path
   returns image string
*/
async function getDataDecode(options: any) {
  let result = new Promise((resolve, reject) => {
    PythonShell.run("decode.py", options, function (err, result) {
      if (err) return reject(err);
      if (result) {
        return resolve(result[0]);
      }
    });
  });

  return result;
}

/*
   getPhotoString
   runs a python script to convert image data to a base 64 string
   options contains arg parameter of image path
   returns image string
*/
async function getPhotoString(options: any) {
  let result = new Promise((resolve, reject) => {
    PythonShell.run("encode.py", options, function (err, result) {
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
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { filename } = req.query;
  let result: any;
  let options = { args: [filename] };

  // gets base64 string of tests image
  await getPhotoString(options).then((photoString) => {
    result = photoString;

    let optionsReq = {
      method: "post",
      url: "http://127.0.0.1:5000/",
      data: {
        Photo: result,
      },
    };


    // sends base64 string to front server
    getFromServer(optionsReq).then((response: any) => {
      let matchingData: any = JSON.parse(response);
      let name: string = matchingData.Name; 
      let photoString:any = matchingData.Photo;
          
      res.status(200).json({ name: name, photo: photoString});  // sends response back to clients side 
    });
  });
}
