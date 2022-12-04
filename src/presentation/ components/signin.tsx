import axios from "axios";
import { ChangeEvent, useRef, useState } from "react";

const SignIn = (props: any) => {
  const [image, setImage] = useState("");
  const [fileName, setFileName] = useState("");
  const [byteString , setByteString] = useState("")
  const userFace = useRef<HTMLInputElement>(null);
  const addImages = props.addImages;

  async function postData(url:string , data:string ) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify({"Photo":data}) // body data type must match "Content-Type" header
    });
    return response.json; // parses JSON response into native JavaScript objects
  }
  
  

  const handleSubmit =  async (event: any) => {
    event.preventDefault();
   // alert("submi")
    let options = { args: ["9_1.jpg"] };
    fetch("/api/process").then((response) => response.json())
      .then((data) => setByteString(data.result));
    
    console.log(byteString)
    postData("http://localhost:5000/photo",byteString)
      .then()
    
  

  }

  return (
    <>
      <div className="flex flex-col items-center justify-center ">
        {image && (
          <img
            src={image}
            className="mt-4 mb-9 object-cover "
            style={{
              width: "4.375rem",
              height: `5rem`,
              objectFit: "cover",
            }}
          />
        )}
        <form
          className="mt-16 flex w-7 flex-col justify-center"
          onSubmit={handleSubmit}
        >
          <input
            type="file"
            placeholder="choose file"
            className="input"
            ref={userFace as any}
            onChange={(event: ChangeEvent<HTMLInputElement>) => {
              if (event?.target?.files?.[0]) {
                const file = event.target.files[0];
                setFileName(file.name);
                const reader = new FileReader();
                reader.onloadend = () => {
                  setImage(reader.result as string);
                };
                reader.readAsDataURL(file);
              }
            }}
          />
          <input className="btn-primary btn " type="submit" />
        </form>
      </div>
    </>
  );
};


export default SignIn;
