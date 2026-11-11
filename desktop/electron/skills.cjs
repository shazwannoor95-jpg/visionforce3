const fs=require('node:fs');const path=require('node:path');const crypto=require('node:crypto');
const EXPECTED=['remotion-best-practices','remotion-captions','remotion-create','remotion-docs','remotion-interactivity','remotion-license','remotion-maps','remotion-markup','remotion-multimedia','remotion-render','remotion-saas','remotion-studio','remotion-upgrade','playwright-cli','playwright-component-testing','playwright-trace','buat-video-motion-grafik','buat-video-motion-grafik-gemini'];
function discover(root){return EXPECTED.map(id=>{const file=path.join(root,id,'SKILL.md');try{const text=fs.readFileSync(file,'utf8');const name=/^name:\s*(.+)$/m.exec(text)?.[1];const description=/^description:\s*(.+)$/m.exec(text)?.[1];if(!text.startsWith('---\n')||name!==id||!description)throw Error('Frontmatter tidak sah');return {id,description,status:'VERIFIED',sha256:crypto.createHash('sha256').update(text).digest('hex'),runtime:'Belum diuji pada komputer ini',catalog:id==='buat-video-motion-grafik'?'Atlas asal (842, namespace berasingan)':id==='buat-video-motion-grafik-gemini'?'Atlas Gemini 922':'',platform:id.startsWith('buat-video')?'Windows: adapter terpilih; runtime Linux berasingan':'Node/Windows atau Cloud mengikut fungsi'};}catch(error){return {id,status:'FAILED',description:String(error),runtime:'Tidak tersedia'};}});}
class VisionForgeSkillRouter{
 select(prompt,skills,mode='auto'){
 if(typeof prompt!=='string'||prompt.length>10000)throw Error('Prompt tidak sah');
 const selected=['remotion-create','remotion-markup','remotion-render'];
 if(/sari|caption|subtitle/i.test(prompt))selected.push('remotion-captions');
 if(/atlas|kartun|infografik|motion/i.test(prompt))selected.push('buat-video-motion-grafik');
 if(/vox|papercut|bang motion|hyperframes|gemini/i.test(prompt))selected.push('buat-video-motion-grafik-gemini');
 if(mode==='browser')selected.push('playwright-cli');
 return {selected:skills.filter(s=>selected.includes(s.id)),status:'PLANNED',engine:mode==='browser'?'browser':'remotion',planner:'Router peraturan tempatan; bukan inferens AI.',cost:'Tiada panggilan berbayar dilakukan.',fallback:'Worker Cloud jika dikonfigurasi; tiada pemasangan model automatik.'};
 }
}
module.exports={discover,EXPECTED,VisionForgeSkillRouter};
