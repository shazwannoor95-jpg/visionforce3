const fs=require('node:fs'),path=require('node:path');
async function portableWorkflowCheck(workflow,store,hub,providers){
 const original={state:hub.state,generate:hub.generate,providerState:providers.state,google:providers.google};let voiceCalls=0;
 try{
  const cli=await hub.run(['--version'],{timeout:10000});if(cli.code!==0||!/^codex-cli 0\.167\.2\b/.test(cli.out))throw Error('Bundled Codex CLI cannot start in Portable');const codexCliVersion=cli.out.trim();
  hub.state=async()=>({selected:{id:'codex',model:''},agents:[{id:'codex',configured:true}]});
  hub.generate=async()=>({title:'Portable workflow fixture',scenes:[{heading:'Rekod',body:'Simpan rekod teratur.',narration:'Simpan rekod teratur.',sourceId:'s1',quote:'Simpan rekod teratur.',imageId:null},{heading:'Kategori',body:'Gunakan kategori.',narration:'Gunakan kategori.',sourceId:'s1',quote:'Gunakan kategori.',imageId:null}]});
  providers.state=()=>[{id:'google',configured:true}];providers.google=async()=>{voiceCalls++;const pcm=Buffer.alloc(24000*2);for(let i=0;i<pcm.length/2;i++)pcm.writeInt16LE(Math.round(2000*Math.sin(i*(voiceCalls===1?440:660)*2*Math.PI/24000)),i*2);return {audio:require('../providers.cjs').wav({mimeType:'audio/L16;rate=24000',data:pcm.toString('base64')})};};
  let p=store.create('Portable simple workflow fixture');const dir=path.join(store.root,'portable-workflow-fixture');fs.mkdirSync(dir,{recursive:true});const source=path.join(dir,'source.txt');fs.writeFileSync(source,'Simpan rekod teratur. Gunakan kategori.');p=store.attach(p.id,source);
  await workflow.start(p.id,'Video penerangan 4 saat',{narration:true},[p.files[0].id]);const until=Date.now()+90000;while(Date.now()<until){p=workflow.get(p.id);if(p.workflow.status==='FAILED')throw Error(p.workflow.error);if(p.workflow.status==='COMPLETE'){if(voiceCalls!==2||!p.workflow.proof.audio)throw Error('Voice composition fixture failed');return {status:'PASS',codexCliVersion,scope:'synthetic agent + TTS fixtures; actual native rendering, live OAuth/inference NOT RUN',voiceCalls,proof:p.workflow.proof,video:store.resolveMedia(p.id,p.workflow.videoId)};}await new Promise(r=>setTimeout(r,250));}throw Error('Portable simple workflow timeout');
 }finally{hub.state=original.state;hub.generate=original.generate;providers.state=original.providerState;providers.google=original.google;}
}
module.exports={portableWorkflowCheck};
