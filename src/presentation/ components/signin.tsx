import { useRef, useState } from "react";

const SignIn = (props: any) => {
  const [image, setImage] = useState();
  const userFace = useRef();
  const handleSubmit = (event:any) => {
    event.preventDefault();
    alert(`The name you entered was: ${userFace.current.files[0].name}`)
  }
  ;

  return (
    <form className="w-full max-w-xs" onSubmit={handleSubmit}>
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
