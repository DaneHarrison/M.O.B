import { PrismaClient } from '@prisma/client'
import name from "./randomNames.json"
const prisma = new PrismaClient()
async function main() {
    let currNamePosi = 0;
    
    for(let i = 0; i < 100; i ++) {
        if(i % 8 == 0) {
            currNamePosi++;
        }

        const submission = await prisma.user.upsert({
            create: {
                Name: name[currNamePosi],
                Weight: 'Alice', 
                Photo: ""
            }
        })
    }
}