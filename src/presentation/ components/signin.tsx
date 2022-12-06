/*
  signin.tsx
  This component grabs the user photo and  converts it to a string
  and sends it to the database server
*/
import { ChangeEvent, useRef, useState } from "react";

/*
  SignIn 
  displays the signin form jsx into html
*/
const SignIn = (props: any) => {
  const [image, setImage] = useState(""); //stores preview image
  const [fileName, setFileName] = useState(""); //stores filename of image
  const userFace = useRef<HTMLInputElement>(null);
  const addImages = props.addImages;
  const changeName = props.changeName;

  

  // handleSubmit
  // submits name of the image test file and opens it on backend route 
  // localhosthost:3000/api/process/<name of file>
  // then it sets the state of the matching photo and name and using prop drilling 
  // it renders it on the matching component
  const handleSubmit = async (event: any) => {
    event.preventDefault();
    fetch(`/api/process/${fileName}`)
      .then((response) => response.json())
      .then((data) => {
        changeName(data.name);
        addImages(data.photo);
      });
  };

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
          {image && <input className="btn-primary btn " type="submit" />}
        </form>
      </div>
    </>
  );
};

export default SignIn;
