import net from "net";

export default class Handler {
    private pending: [];

    constructor() {
        this.pending = [];
    }

    handleIncoming(conn: net.Socket) {
        
        //if from server
            this._genNewRequest();

        //if from database
            this._updateRequest()

        conn.end();
    }

    //mean vector is the mean vector of all the training output
    //eigenVectors have nothing to do with mean vector this is covarient matrix
        //eigvenVectors 
    private _genNewRequest() { //mean vector s 5600 x1
        //process face
            //transpose mean/eigen matrix (from trainer)
            //with image from server (input image)
                //flatten
                //multiply by transposed vector
                //gives 136x1 matrix

                //(136, 320) => 136 
        //put request into pending
        //send requests to DB
    }

    private _updateRequest() {
            //if photo and image:
                //send to server
                //remove from pending
            //else
                //find which one needs to be updated and update it
                //if all responses have been recieved
                //check which was closest
                //request that photo
    }
}