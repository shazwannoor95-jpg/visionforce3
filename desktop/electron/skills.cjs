const fs=require('node:fs');const path=require('node:path');const crypto=require('node:crypto');
const EXPECTED=['remotion-best-practices','remotion-captions','remotion-create','remotion-docs','remotion-interactivity','remotion-license','remotion-maps','remotion-markup','remotion-multimedia','remotion-render','remotion-saas','remotion-studio','remotion-upgrade','playwright-cli','playwright-component-testing','playwright-trace','directing-stickman-videos','buat-video-motion-grafik','buat-video-motion-grafik-gemini'];
const {TextDecoder}=require('node:util');
const {parseDocument}=require('yaml');
function frontmatter(raw, expectedId){
 const text=new TextDecoder('utf-8',{fatal:true}).decode(raw).replace(/^\uFEFF/,'').replace(/\r\n?/g,'\n');
 const lines=text.split('\n');
 if(lines[0]!=='---')throw Error('Pembuka frontmatter --- mesti pada baris pertama (BOM dibenarkan)');
 const end=lines.findIndex((line,i)=>i>0&&/^---[ \t]*$/.test(line));
 if(end<0)throw Error('Penutup frontmatter --- tiada');
 const header=lines.slice(1,end).join('\n');
 if(Buffer.byteLength(header)>65536)throw Error('Frontmatter melebihi had 64 KiB');
 const doc=parseDocument(header,{schema:'core',version:'1.2',uniqueKeys:true,customTags:[]});
 if(doc.errors.length||doc.warnings.length)throw Error('YAML frontmatter tidak sah: '+[...doc.errors,...doc.warnings].map(e=>e.code||e.message).join(', '));
 const fields=doc.toJS({mapAsMap:true,maxAliasCount:0});
 if(!(fields instanceof Map))throw Error('Frontmatter mesti mapping YAML');
 const name=fields.get('name'),description=fields.get('description');
 if(typeof name!=='string'||name!==expectedId)throw Error('ID skill tidak sepadan direktori: dijangka '+expectedId+', diterima '+JSON.stringify(name));
 if(typeof description!=='string'||!description.trim())throw Error('description mesti teks tidak kosong');
 return {name,description:description.trim()};
}
function discover(root){return EXPECTED.map(id=>{const file=path.join(root,id,'SKILL.md');try{
 const raw=fs.readFileSync(file);const {description}=frontmatter(raw,id);
 return {id,description,status:'VERIFIED',sha256:crypto.createHash('sha256').update(raw).digest('hex'),runtime:'Belum diuji pada komputer ini',catalog:id==='buat-video-motion-grafik'?'Atlas asal (842, namespace berasingan)':id==='buat-video-motion-grafik-gemini'?'Atlas Gemini 922':'',platform:id.startsWith('buat-video')?'Windows: adapter terpilih; runtime Linux berasingan':'Node/Windows atau Cloud mengikut fungsi'};
 }catch(error){const reason=error.code==='ENOENT'?'SKILL.md tiada':error.message;return {id,status:'FAILED',reason,file,description:reason,runtime:'Tidak tersedia'};}});}
function audit(root){
 const rows=discover(root);const directories=fs.readdirSync(root,{withFileTypes:true}).filter(x=>x.isDirectory()).map(x=>x.name);
 const unexpected=directories.filter(id=>!EXPECTED.includes(id));
 const failed=rows.filter(r=>r.status!=='VERIFIED').map(r=>({id:r.id,file:r.file,reason:r.reason}));
 return {ok:rows.length===EXPECTED.length&&directories.length===EXPECTED.length&&!unexpected.length&&!failed.length,expected:EXPECTED.length,folders:directories.length,verified:rows.filter(r=>r.status==='VERIFIED').length,unexpected,failed,rows};
}
class VisionForgeSkillRouter{
 select(prompt,skills,mode='auto'){
 if(typeof prompt!=='string'||prompt.length>10000)throw Error('Prompt tidak sah');
 const selected=['remotion-create','remotion-markup','remotion-render'];
 if(/sari|caption|subtitle/i.test(prompt))selected.push('remotion-captions');
 if(/atlas|kartun|infografik|motion/i.test(prompt))selected.push('buat-video-motion-grafik');
 if(/vox|papercut|bang motion|hyperframes|gemini/i.test(prompt))selected.push('buat-video-motion-grafik-gemini');
 if(/stickman|stick figure/i.test(prompt))selected.push('directing-stickman-videos');
 if(mode==='browser')selected.push('playwright-cli');
 return {selected:skills.filter(s=>selected.includes(s.id)),status:'PLANNED',engine:mode==='browser'?'browser':'remotion',planner:'Router peraturan tempatan; bukan inferens AI.',cost:'Tiada panggilan berbayar dilakukan.',fallback:'Worker Cloud jika dikonfigurasi; tiada pemasangan model automatik.'};
 }
}
module.exports={discover,audit,frontmatter,EXPECTED,VisionForgeSkillRouter};
