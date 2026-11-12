const fs=require('node:fs'),path=require('node:path');
const {spawn}=require('node:child_process');
const {atomic}=require('./store.cjs');
const IDS=['codex','openai','anthropic','google'];
const LABELS={codex:'Codex · Akaun ChatGPT',openai:'OpenAI · API',anthropic:'Claude · API',google:'Gemini · API'};
function codexBinary(){
 const triples={'win32-x64':'x86_64-pc-windows-msvc','linux-x64':'x86_64-unknown-linux-musl','darwin-arm64':'aarch64-apple-darwin','darwin-x64':'x86_64-apple-darwin'};
 const target=triples[process.platform+'-'+process.arch];if(!target)throw Error('Codex belum dibundel untuk platform ini.');
 const root=path.dirname(require.resolve('@openai/codex-'+process.platform+'-'+process.arch+'/package.json'));
 return path.join(root,'vendor',target,'bin',process.platform==='win32'?'codex.exe':'codex');
}
function devicePrompt(raw){const s=raw.replace(/\x1b\[[0-?]*[ -/]*[@-~]/g,'');const url=/https:\/\/auth\.openai\.com\/codex\/device\b/.exec(s)?.[0];const code=/Enter this one-time code[^\n]*\n\s*([A-Z0-9-]{6,20})/.exec(s)?.[1];return url&&code?{url,code}:null;}
function execArgs(folder,schemaFile,output,images=[]){
 return ['-c','cli_auth_credentials_store="keyring"','exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','--sandbox','read-only','-c','approval_policy="never"','-c','web_search="disabled"',
 ...['shell_tool','unified_exec','js_repl','apps','plugins','multi_agent','image_generation','view_image','browser_use','computer_use'].flatMap(f=>['-c','features.'+f+'=false']),
 '-c','features.skip_host_skill_discovery=true','-C',folder,'--color','never','--json','--output-schema',schemaFile,'--output-last-message',output,...images.flatMap(file=>['--image',file])];
}
class AgentHub{
 constructor({root,providers,binary,spawnFn=spawn}){this.root=root;this.providers=providers;try{this.binary=binary||codexBinary();}catch{this.binary='';}this.spawn=spawnFn;this.file=path.join(root,'agent-selection.json');this.home=path.join(root,'agent-profiles','codex');fs.mkdirSync(this.home,{recursive:true,mode:0o700});this.login={phase:'IDLE',url:'',code:'',error:''};this.child=null;}
 selected(){try{const c=JSON.parse(fs.readFileSync(this.file,'utf8'));return IDS.includes(c.id)?c:{id:'codex',model:''};}catch{return {id:'codex',model:''};}}
 select(id,model=''){if(!IDS.includes(id)||typeof model!=='string'||model.length>120||/[\r\n]/.test(model))throw Error('Agent atau model tidak sah.');const value={id,model:model.trim()};atomic(this.file,JSON.stringify(value));return value;}
 env(){const env={...process.env,CODEX_HOME:this.home};for(const key of ['OPENAI_API_KEY','CODEX_API_KEY','OPENAI_BASE_URL','CODEX_ACCESS_TOKEN'])delete env[key];return env;}
 run(args,{input='',signal,timeout=120000,onData}={}){return new Promise((resolve,reject)=>{
  let out='',err='',ended=false;const child=this.spawn(this.binary,args,{env:this.env(),cwd:this.home,windowsHide:true,stdio:['pipe','pipe','pipe']});const abort=()=>{child.kill();};const timer=setTimeout(abort,timeout);signal?.addEventListener('abort',abort,{once:true});
  const done=(error,code)=>{if(ended)return;ended=true;clearTimeout(timer);signal?.removeEventListener('abort',abort);error?reject(Error('Codex tidak dapat dimulakan. Pasang semula build aplikasi terkini.')):resolve({code,out,err});};
  child.stdout.on('data',d=>{out=(out+d.toString()).slice(-200000);onData?.(out);});child.stderr.on('data',d=>err=(err+d.toString()).slice(-4000));child.on('error',e=>done(e));child.on('close',code=>done(null,code));child.stdin.on('error',()=>{});child.stdin.end(input);if(signal?.aborted)abort();
 });}
 async codexStatus(){if(!fs.existsSync(this.binary))return false;if(!this.statusCache||Date.now()-this.statusAt>3000){this.statusAt=Date.now();this.statusCache=this.run(['-c','cli_auth_credentials_store="keyring"','login','status'],{timeout:10000}).then(r=>r.code===0);}return this.statusCache;}
 voiceModel(){try{const value=JSON.parse(fs.readFileSync(path.join(this.root,'agent-voice.json'),'utf8')).model;return typeof value==='string'&&/^[A-Za-z0-9._-]{1,120}$/.test(value)?value:'gemini-2.5-flash-preview-tts';}catch{return 'gemini-2.5-flash-preview-tts';}}
 setVoiceModel(model){model=model||'gemini-2.5-flash-preview-tts';if(typeof model!=='string'||!/^[A-Za-z0-9._-]{1,120}$/.test(model))throw Error('Model suara tidak sah.');atomic(path.join(this.root,'agent-voice.json'),JSON.stringify({model}));return model;}
 async state(){const api=this.providers.state();let connected=false;try{connected=await this.codexStatus();}catch{}return {selected:this.selected(),voiceModel:this.voiceModel(),login:{...this.login},agents:IDS.map(id=>({id,label:LABELS[id],configured:id==='codex'?connected:!!api.find(p=>p.id===id)?.configured,auth:id==='codex'?'account':'api'}))};}
 startLogin(method='device'){
  if(this.child)throw Error('Login masih berjalan. Lengkapkan atau batalkan dahulu.');if(!fs.existsSync(this.binary))throw Error('Komponen Codex tiada; pasang semula aplikasi.');if(!['device','browser'].includes(method))throw Error('Cara login tidak sah.');
  this.login={phase:'STARTING',url:'',code:'',error:''};let log='';const child=this.spawn(this.binary,['-c','cli_auth_credentials_store="keyring"','login',...(method==='device'?['--device-auth']:[])],{env:this.env(),cwd:this.home,windowsHide:true,stdio:['ignore','pipe','pipe']});this.child=child;
  const timer=setTimeout(()=>child.kill(),16*60*1000);const fail=()=>{this.login={phase:'ERROR',url:'',code:'',error:'Login Codex tidak selesai. Cuba login browser atau semak akses Codex pada akaun ChatGPT anda. Token disimpan oleh Codex dalam storan OS; jika storan OS gagal, guna integrasi API.'};};
  child.stdout.on('data',d=>{log=(log+d.toString()).slice(-5000);const prompt=devicePrompt(log);if(prompt)this.login={phase:'WAITING',...prompt,error:''};else if(method==='browser'){const plain=log.replace(/\x1b\[[0-?]*[ -/]*[@-~]/g,'');const url=/https:\/\/auth\.openai\.com\/oauth\/authorize\?[^\s]+/.exec(plain)?.[0]||'';this.login={phase:'WAITING_BROWSER',url,code:'',error:''};}});child.stderr.on('data',()=>{});
  child.on('error',()=>{clearTimeout(timer);this.child=null;fail();});child.on('close',code=>{clearTimeout(timer);this.child=null;this.statusCache=null;if(this.login.phase==='CANCELLED')return;this.login=code===0?{phase:'DONE',url:'',code:'',error:''}:(fail(),this.login);});return {...this.login};
 }
 cancelLogin(){if(this.child){this.login={phase:'CANCELLED',url:'',code:'',error:''};this.child.kill();}return {...this.login};}
 async logout(){this.cancelLogin();await this.run(['-c','cli_auth_credentials_store="keyring"','logout'],{timeout:15000});this.statusCache=null;this.login={phase:'IDLE',url:'',code:'',error:''};}
 async generate({prompt,schema,folder,images=[],signal}){
  const selection=this.selected();if(selection.id==='codex'){
   if(!await this.codexStatus())throw Error('NEEDS_AGENT: Login Codex dahulu.');const schemaFile=path.join(folder,'plan-schema.json'),output=path.join(folder,'agent-result.json');atomic(schemaFile,JSON.stringify(schema));
   const args=execArgs(folder,schemaFile,output,images);if(selection.model)args.push('--model',selection.model);
   const r=await this.run(args,{input:prompt,signal,timeout:240000});if(r.code!==0||!fs.existsSync(output))throw Error('Codex gagal menjana pelan. Semak login, akses model dan kuota akaun, kemudian cuba semula. Tiada retry automatik dibuat.');return parsePlan(fs.readFileSync(output,'utf8'));
  }
  return parsePlan(await this.providers.plan({id:selection.id,model:selection.model,prompt,images,signal}));
 }
 close(){this.cancelLogin();}
}
function parsePlan(value){if(typeof value!=='string'||value.length>100000)throw Error('Respons agent terlalu besar atau tidak sah.');try{return JSON.parse(value.trim().replace(/^```(?:json)?\s*/,'').replace(/\s*```$/,''));}catch{throw Error('Agent tidak mengembalikan pelan JSON yang sah. Cuba semula atau pilih model lain.');}}
module.exports={AgentHub,codexBinary,devicePrompt,execArgs,parsePlan};
