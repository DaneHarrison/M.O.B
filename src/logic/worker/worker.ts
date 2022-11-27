import net from "net";
import Handler from "./handler";

const HOST: string = 'localhost';
const PORT: number = 8080;

//setup the server
let handler = new Handler();
let server = net.createServer().listen({
    host: HOST,
    port: PORT
});

console.log(`Server llistening @ ${HOST}:${PORT}`);

//setup listener
server.on('connection', (conn) => { handler.handleIncoming(conn); });