import DBResponse from "./dbResponse";
import ClosestFace from "./closestFace";
import net from "net";

export default class Request {
    processedImg: number;
    DBARes: DBResponse | null;
    DBBRes: DBResponse | null;
    DBCRes: DBResponse | null;
    closest: ClosestFace | null;

    

    constructor(processedImg: number) {
        this.processedImg = processedImg;
        this.DBARes = null;
        this.DBBRes = null;
        this.DBCRes = null;
        this.closest = null;
    }


    readyToRequestClosest() {
        return this.DBARes && this.DBBRes && this.DBCRes
    }

    setDBARes(res: string) {

    }

    getDBARes() {
        return this.DBARes;
    }

    setDBBRes(res: string) {

    }

    getDBBRes() {
        return this.DBBRes;
    }

    setDBCRes(res: string) {

    }

    getDBCRes() {
        return this.DBCRes;
    }

    setClosest(res: string) {

    }

    getClosest() {
        return this.closest;
    }
}