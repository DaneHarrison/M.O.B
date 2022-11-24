import  {PrismaClient}  from '@prisma/client';

export default class DBAdapter {
    database: PrismaClient;

    constructor() {
        this.database = new PrismaClient()
    }


    _connect() {
        this.database.$connect()

        return this.database;
    }

    disconnect() {
        this.database.$disconnect()
    }
}