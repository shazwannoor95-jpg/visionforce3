const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
const URL_AI='https://aistudio.google.com/';
function permitted(raw){try{const u=new URL(raw);return u.protocol==='https:'&&!u.username&&!u.password&&!u.port&&['aistudio.google.com','accounts.google.com'].includes(u.hostname);}catch{return false;}}
const editorScript=`(()=>{const visible=e=>!!e.getClientRects().length&&!e.disabled&&!e.readOnly;const nodes=[...document.querySelectorAll('textarea,[contenteditable="true"][role="textbox"],rich-textarea [contenteditable="true"]')].filter(visible);return nodes;})()`;
class BrowserSession{
 constructor({BrowserWindow,session,shell}){Object.assign(this,{BrowserWindow,session,shell});this.window=null;this.error='';this.downloads=[];this.directory=fs.mkdtempSync(path.join(os.tmpdir(),'vf-audio-'));this.downloadHandler=null;}
 state(){return {open:!!this.window&&!this.window.isDestroyed(),login:'MANUAL_ACTION_REQUIRED',error:this.error,audio:this.downloads.map(({id,name})=>({id,name}))};}
 async open(){
  if(this.state().open){this.window.show();this.window.focus();return this.state();}
  this.error='';const partition='persist:vf-provider-google';const ses=this.session.fromPartition(partition);
  if(!this.downloadHandler){this.downloadHandler=(event,item,wc)=>{
   const ext=path.extname(item.getFilename()).toLowerCase();
   if(wc!==this.window?.webContents||!['.wav','.mp3'].includes(ext)){event.preventDefault();this.error='Hanya WAV/MP3 dari browser aplikasi disokong.';return;}
   const id=crypto.randomUUID();const file=path.join(this.directory,id+ext);item.setSavePath(file);
   item.on('updated',()=>{if(item.getReceivedBytes()>50*1024*1024)item.cancel();});
   item.once('done',(_event,status)=>{if(status==='completed'&&fs.existsSync(file)&&fs.statSync(file).size<=50*1024*1024){this.downloads.push({id,file,name:item.getFilename()});}else{fs.rmSync(file,{force:true});this.error='Muat turun audio gagal atau melebihi 50 MiB.';}});
  };ses.on('will-download',this.downloadHandler);}
  ses.setPermissionRequestHandler((_wc,_permission,callback)=>callback(false));ses.setPermissionCheckHandler(()=>false);
  const win=new this.BrowserWindow({width:1100,height:820,title:'VISIONFORGE — Login Google AI Studio',webPreferences:{partition,contextIsolation:true,nodeIntegration:false,sandbox:true,webSecurity:true}});this.window=win;win.setMenu(null);
  const guard=(event,url)=>{if(!permitted(url))event.preventDefault();};win.webContents.on('will-navigate',guard);win.webContents.on('will-redirect',guard);
  win.webContents.setWindowOpenHandler(({url})=>{if(permitted(url))win.loadURL(url).catch(()=>{this.error='Halaman gagal dimuatkan. Cuba browser sistem.';});return {action:'deny'};});
  win.on('closed',()=>{if(this.window===win)this.window=null;});
  try{await win.loadURL(URL_AI);}catch{this.error='Halaman gagal dimuatkan. Cuba browser sistem.';}return this.state();
 }
 async speech(){await this.open();await this.window.loadURL('https://aistudio.google.com/generate-speech');return this.probe();}
 importAudio(id,attach){const audio=this.downloads.find(d=>d.id===id);if(!audio)throw Error('Audio belum tersedia. Tekan Download dalam AI Studio dahulu.');const result=attach(audio.file);fs.rmSync(audio.file,{force:true});this.downloads=this.downloads.filter(d=>d!==audio);return result;}
 dispose(){this.close();if(this.downloadHandler)this.session.fromPartition('persist:vf-provider-google').removeListener('will-download',this.downloadHandler);fs.rmSync(this.directory,{recursive:true,force:true});}
 async probe(){
  const state=this.state();if(!state.open)return {...state,connection:'CLOSED'};
  const url=this.window.webContents.getURL();if(!permitted(url)||new URL(url).hostname!=='aistudio.google.com')return {...state,connection:'LOGIN_REQUIRED'};
  try{const denied=await this.window.webContents.executeJavaScript("document.body.innerText.includes('Failed to list API keys: permission denied')");if(denied)return {...this.state(),connection:'PAGE_PERMISSION_DENIED'};if(/\/(api-?keys?|apikey)(?:\/|$)/.test(new URL(url).pathname))return {...this.state(),connection:'API_KEY_MANAGEMENT'};const count=await this.window.webContents.executeJavaScript(`(${editorScript}).length`);return {...this.state(),connection:count===1?'EDITOR_FOUND':count>1?'EDITOR_AMBIGUOUS':'PAGE_NOT_READY'};}catch{return {...this.state(),connection:'PAGE_NOT_READY'};}
 }
 async fill(text){
  if(typeof text!=='string'||!text.trim()||text.length>20000)throw Error('Brief perlu 1–20000 aksara.');
  if((await this.probe()).connection!=='EDITOR_FOUND')throw Error('Ruang prompt belum sedia atau tidak dapat dikenal pasti. Buka Playground dalam browser aplikasi dahulu.');
  const win=this.window;
  const focused=await win.webContents.executeJavaScript(`(()=>{const nodes=${editorScript};if(nodes.length!==1)return false;const e=nodes[0];if((e.value||e.textContent||'').trim())return false;e.focus();return document.activeElement===e;})()`);
  if(!focused)throw Error('Ruang prompt mempunyai teks atau fokus gagal. Kosongkan sendiri untuk mengelakkan teks ditimpa.');
  win.show();win.focus();await win.webContents.insertText(text);return {filled:true};
 }
 async selection(){
  if((await this.probe()).connection==='CLOSED')throw Error('Buka browser aplikasi dahulu.');
  const url=this.window.webContents.getURL();if(!permitted(url)||new URL(url).hostname!=='aistudio.google.com')throw Error('Buka AI Studio dahulu.');
  const text=await this.window.webContents.executeJavaScript('window.getSelection().toString()');
  if(!text.trim()||text.length>20000)throw Error('Pilih teks jawapan dalam AI Studio dahulu (maksimum 20000 aksara).');return {text};
 }
 close(){this.window?.close();return this.state();}
 async external(){await this.shell.openExternal(URL_AI);return {opened:true};}
}
module.exports={BrowserSession,permitted,URL_AI};
