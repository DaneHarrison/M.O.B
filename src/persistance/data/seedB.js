import {PrismaClient} from '@prisma/client'
import fs from 'fs'

import photos from "./fileManifest.json"
import name from "./randomNames.json"
import weights from "./weights.json"

async function main() {
    let client = new PrismaClient();
    let currNamePosi = 99;
    let index = 11;
    let submission;
    
    for(let i = 100; i < 4; i++) {
        submission = await creatEntry(client, index, name[currNamePosi]);
        index++;

        if(!submission) {
            console.log("there was an error seeding the database");
            return;
        }
    }

    for(; index < 200 && submission; index ++) {
        if(i % 8 == 0) {
            currNamePosi++;
        }

        const submission = await creatEntry(client, index, name[currNamePosi]);
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