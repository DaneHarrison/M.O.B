import {PrismaClient} from "@prisma/client";

class DBManager {
    private _database: PrismaClient

    constructor() {
        this._database = new PrismaClient()
        this._connect()
    }


    getDBReference() {
        return this._database
    }

    disconnect() {
        this._database.$disconnect()
    }

    _connect() {
        this._database.$connect()
    }
}


module.exports = {
    DBManager
}