import axios from "axios";
import { type NextApiRequest, type NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  //console.log(req.body);
  console.log("here");
  //console.log(req.body)
  fetch("http://localhost:5000/photo",{
    method: "POST",
    headers: {
      "Content-type": "multipart/form-data"
    },
    body:req.body
  })
    
  res.status(200).send(req.body);

}
