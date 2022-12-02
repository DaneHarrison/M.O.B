const Matches = (props:any) => {
    const images = props.resultImages
    return (
        <>
        {images&&(
           
                <img src={images} />
            
        )}
        </>
      );
}
 
export default Matches;