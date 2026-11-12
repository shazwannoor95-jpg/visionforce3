const fs=require('node:fs'),path=require('node:path');
function fixture(dir){
 const {createCanvas}=require('@napi-rs/canvas');
 const actor=path.join(dir,'fixture-actor.png'),prop=path.join(dir,'fixture-prop.png'),audio=path.join(dir,'fixture-narration.wav');
 const c=createCanvas(240,380),x=c.getContext('2d');x.strokeStyle='#15202b';x.lineWidth=5;x.beginPath();x.arc(120,55,35,0,Math.PI*2);x.moveTo(120,90);x.lineTo(120,230);x.moveTo(120,130);x.lineTo(60,180);x.moveTo(120,130);x.lineTo(190,165);x.moveTo(120,230);x.lineTo(65,335);x.moveTo(120,230);x.lineTo(175,335);x.stroke();fs.writeFileSync(actor,c.toBuffer('image/png'));
 x.clearRect(0,0,240,380);x.fillStyle='#ffc94a';x.fillRect(20,110,190,130);x.strokeRect(20,110,190,130);fs.writeFileSync(prop,c.toBuffer('image/png'));
 const bed=path.join(dir,'fixture-ambience.wav');const pcm=Buffer.alloc(24000*2*2);for(let i=0;i<pcm.length/2;i++)pcm.writeInt16LE(Math.round(2000*Math.sin(i*440*2*Math.PI/24000)),i*2);const {wav}=require('../electron/providers.cjs');fs.writeFileSync(audio,wav({mimeType:'audio/L16;rate=24000',data:pcm.toString('base64')}));const noise=Buffer.alloc(pcm.length);let seed=42;for(let i=0;i<noise.length/2;i++){seed=(1664525*seed+1013904223)>>>0;noise.writeInt16LE(Math.round((seed/4294967296-.5)*8000),i*2);}fs.writeFileSync(bed,wav({mimeType:'audio/L16;rate=24000',data:noise.toString('base64')}));return {actor,prop,audio,bed};
}
module.exports={fixture};
