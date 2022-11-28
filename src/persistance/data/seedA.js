import {PrismaClient} from '@prisma/client'
import fs from 'fs'

import photos from "./fileManifest.json"
import name from "./randomNames.json"
import weights from "./weights.json"

async function main() {
    let client = new PrismaClient();
    let currNamePosi = 0;
    let submission;
    
    for(let i = 0; i < 100; i ++) {
        if(i % 8 == 0) {
            currNamePosi++;
        }

        submission = await creatEntry(client, index, name[i]);
        index++;

        if(!submission) {
            console.log("there was an error seeding the database");
            return;
        }
    }
}

async function creatEntry(client, index, name) {
    let results = await client.user.upsert({
        create: {
            Name: name,
            Weight: weights[index], 
            Photo: fs.readFileSync(photos[index], {flag: 'r'})
        }
    });

    return results;
}