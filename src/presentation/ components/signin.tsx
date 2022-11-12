import axios from "axios";
import { useRef, useState } from "react";

const SignIn = (props: any) => {
  const [image, setImage] = useState();
  const userFace = useRef();
  const handleSubmit = (event: any) => {
    event.preventDefault();
    alert(`The name you entered was: ${userFace.current.files[0].name}`);
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
    <form className="flex flex-col" onSubmit={handleSubmit}>
      <input
        type="file"
        placeholder="choose file"
        className="input w-full max-w-xs"
        ref={userFace}
      />
      <input className="btn-primary btn" type="submit" />
    </form>
  );
};

export default SignIn;
