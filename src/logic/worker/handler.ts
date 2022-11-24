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

    private _genNewRequest() {
        //process face
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