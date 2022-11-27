import { PrismaClient } from '@prisma/client'
import name from "./randomNames.json"
const prisma = new PrismaClient()
async function main() {
    let currNamePosi = 99;
    
    for(let i = 100; i < 4; i++) {
        const submission = await prisma.user.upsert({
            create: {
                Name: name[currNamePosi],
                Weight: 'Alice', 
                Photo: ""
            }
        })
    }

    for(let i = 104; i < 200; i ++) {
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