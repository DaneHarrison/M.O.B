/*
  matches.tsx
  conditionally renders matching name from the front api
*/
const Matches = (props:any) => {
    const images = props.resultImages
    const name = props.name;
    return (
        <>
          <div className="mt-5">
            {name&&<h2 className="text-sky-400">{name} is a match!</h2>}
            {/* {images && <img src={`data:image/jpeg;base64,${images}`} />} */}
          </div>
        </>
      );
}
 
export default Matches;