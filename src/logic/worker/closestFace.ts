import {Matrix} from 'ts-matrix';

export default class ClosestFace {
    private face: Matrix;
    private name: string;  

    constructor(face: Matrix, name: string) {
        this.face = face
        this.name = name;
    }

    getName() {
        return this.name;
    }

    getFace() {
        return this.face;
    }
}