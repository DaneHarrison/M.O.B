import { type NextApiRequest, type NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  //console.log(req.body);
  console.log("here");
  //console.log(req.body)
  res.status(200).send(req.body);

}
