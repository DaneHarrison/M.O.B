import axios from "axios";
import { useRef, useState } from "react";
import { createRef, PureComponent } from "react";
const SignIn = (props: any) => {
  const [image, setImage] = useState("");
  const userFace = useRef(null);
  const addImages = props.addImages;
  const handleSubmit = (event: any) => {
    event.preventDefault();
    console.log(image);
    //  alert(`The name you entered was: ${userFace.current.files[0].name}`);
    const formData = new FormData();
    const config = {
      headers: {
        "content-type": "multipart/form-data"
      }
    };
    if (userFace.current  && userFace?.current?.files?.[0] ) {
      formData.append("face", userFace.current.files[0]);
      axios
        .post("/api/authenticate", formData,config)
        .then((res) => {
          // alert("File Upload success");
        //  const reader = new FileReader();

          // alert(res.data)
       //   reader.onloadend = () => {
       //     addImages(reader.result as string);
        //  };
          //  reader.readAsDataURL();
        //  reader.readAsDataURL(res.data);
          alert(typeof res.data)
          console.log("here");
        })
        .catch((err) => alert(err));
    }
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
