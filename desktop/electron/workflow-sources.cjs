const fs=require('node:fs'),path=require('node:path');
const {unzipSync}=require('fflate');
function xmlText(xml,tag){return [...xml.matchAll(new RegExp('<'+tag+'(?:\\s[^>]*)?>([\\s\\S]*?)<\\/'+tag+'>','g'))].map(m=>m[1].replace(/&(?:lt|gt|amp|quot|apos);|&#(?:x[\da-f]+|\d+);/gi,e=>{const map={'&lt;':'<','&gt;':'>','&amp;':'&','&quot;':'"','&apos;':"'"};if(map[e])return map[e];const hex=e.startsWith('&#x');const v=parseInt(e.slice(hex?3:2,-1),hex?16:10);return v>0&&v<=0x10ffff?String.fromCodePoint(v):'';})).join(' ');}
async function readSources(store,id,fileIds){
 if(!Array.isArray(fileIds)||!fileIds.length||fileIds.length>20||new Set(fileIds).size!==fileIds.length)throw Error('Pilih 1–20 bahan rujukan.');
 const project=store.get(id),sources=[],images=[];let characters=0;
 const add=(file,location,text)=>{text=text.replace(/\s+/g,' ').trim();if(!text)return;characters+=text.length;if(characters>60000)throw Error('Bahan melebihi 60000 aksara. Pilih bahan atau petikan lebih pendek; tiada teks dipotong secara senyap.');for(let p=0;p<text.length;p+=1800)sources.push({id:'s'+(sources.length+1),fileId:file.id,name:file.name,location,text:text.slice(p,p+1800)});};
 for(const fileId of fileIds){const file=project.files.find(f=>f.id===fileId);if(!file)throw Error('Bahan projek tidak ditemui.');const target=store.resolveMedia(id,fileId),ext=path.extname(file.name).toLowerCase();
  if(['.txt','.md'].includes(ext)){if(fs.statSync(target).size>200000)throw Error('Fail teks terlalu besar.');add(file,'teks',fs.readFileSync(target,'utf8'));}
  else if(ext==='.pdf'){const pages=[];const result=await require('pdf-parse')(fs.readFileSync(target),{max:60,pagerender:async page=>{const content=await page.getTextContent();const text=content.items.map(i=>i.str).join(' ');pages.push(text);return text;}});if(result.numpages>60)throw Error('PDF melebihi 60 halaman. Pilih petikan dahulu.');pages.forEach((s,i)=>add(file,'halaman '+(i+1),s));if(!pages.some(s=>s.trim()))throw Error('PDF imbasan tidak mengandungi teks. Gunakan PDF berteks atau sertakan transkrip; OCR belum tersedia.');}
  else if(['.docx','.pptx'].includes(ext)){let size=0;const entries=unzipSync(fs.readFileSync(target),{filter:f=>{if(!(ext==='.docx'?f.name==='word/document.xml':/^ppt\/slides\/slide\d+\.xml$/.test(f.name)))return false;size+=f.originalSize;if(size>20*1024*1024||f.originalSize>4*1024*1024)throw Error('Kandungan Office terlalu besar.');return true;}});const names=Object.keys(entries).sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));if(!names.length)throw Error('Fail Office tidak mempunyai kandungan teks yang boleh dibaca.');for(const n of names)add(file,n,xmlText(Buffer.from(entries[n]).toString('utf8'),ext==='.docx'?'w:t':'a:t'));}
  else if(['.png','.jpg','.jpeg'].includes(ext)){if(images.length>=4||fs.statSync(target).size>5*1024*1024)throw Error('Maksimum 4 imej, setiap satu sehingga 5 MiB untuk analisis agent.');images.push({id:fileId,path:target,name:file.name});}
  else if(['.wav','.mp3','.mp4'].includes(ext)){/* Media stays available for existing advanced workflow; never invent a transcript. */}
  else throw Error('Format bahan tidak disokong: '+file.name);
 }
 if(!sources.length&&!images.length)throw Error('Untuk analisis audio/video, sertakan teks atau transkrip. Audio/video tidak ditranskrip secara automatik.');
 return {sources,images};
}
module.exports={readSources,xmlText};
