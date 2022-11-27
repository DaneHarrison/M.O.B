import axios from "axios";
import { useRef, useState } from "react";

const SignIn = (props: any) => {
  const [image, setImage] = useState("");
  const userFace = useRef();
  const handleSubmit = (event: any) => {
    event.preventDefault();
    //  alert(`The name you entered was: ${userFace.current.files[0].name}`);
    const formData = new FormData();
    formData.append("face", userFace.current.files[0]);
    axios
      .post("/api/authenticate", formData)
      .then((res) => {
        alert("File Upload success");
      })
      .catch((err) => alert("File Upload Error"));
  };

  return (
    <>
      <div className="flex flex-col justify-center items-center ">
        {image && (
          <img
            src={image}
            className="mt-4 object-cover mb-9 "
            style={{
              width: "4.375rem",
              height: `5rem`,
              objectFit: "cover",
            }}
          />
        )}
        <form
          className="flex w-7 flex-col justify-center mt-16"
          onSubmit={handleSubmit}
        >
          <input
            type="file"
            placeholder="choose file"
            className="input"
            ref={userFace}
            onChange={(event: ChangeEvent<HTMLInputElement>) => {
              if (event?.target?.files?.[0]) {
                const file = event.target.files[0];
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
