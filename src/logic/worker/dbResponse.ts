export default class DBResponse {
    private ID: number;
    private eigenVal: number;

    constructor(ID: number, eigenVal: number) {
        this.ID = ID;
        this.eigenVal = eigenVal
    }


    getID() {
        return this.ID;
    }

    getEigenVal() {
        return this.eigenVal;
    }
}