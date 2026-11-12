const URL_AI='https://aistudio.google.com/';
function permitted(raw){try{const u=new URL(raw);return u.protocol==='https:'&&!u.username&&!u.password&&!u.port&&['aistudio.google.com','accounts.google.com'].includes(u.hostname);}catch{return false;}}
const editorScript=`(()=>{const visible=e=>!!e.getClientRects().length&&!e.disabled&&!e.readOnly;const nodes=[...document.querySelectorAll('textarea,[contenteditable="true"][role="textbox"],rich-textarea [contenteditable="true"]')].filter(visible);return nodes;})()`;
class BrowserSession{
 constructor({BrowserWindow,session,shell}){Object.assign(this,{BrowserWindow,session,shell});this.window=null;this.error='';}
 state(){return {open:!!this.window&&!this.window.isDestroyed(),login:'MANUAL_ACTION_REQUIRED',error:this.error};}
 async open(){
  if(this.state().open){this.window.show();this.window.focus();return this.state();}
  this.error='';const partition='persist:vf-provider-google';const ses=this.session.fromPartition(partition);
  ses.setPermissionRequestHandler((_wc,_permission,callback)=>callback(false));ses.setPermissionCheckHandler(()=>false);
  const win=new this.BrowserWindow({width:1100,height:820,title:'VISIONFORGE — Login Google AI Studio',webPreferences:{partition,contextIsolation:true,nodeIntegration:false,sandbox:true,webSecurity:true}});this.window=win;win.setMenu(null);
  const guard=(event,url)=>{if(!permitted(url))event.preventDefault();};win.webContents.on('will-navigate',guard);win.webContents.on('will-redirect',guard);
  win.webContents.setWindowOpenHandler(({url})=>{if(permitted(url))win.loadURL(url).catch(()=>{this.error='Halaman gagal dimuatkan. Cuba browser sistem.';});return {action:'deny'};});
  win.on('closed',()=>{if(this.window===win)this.window=null;});
  try{await win.loadURL(URL_AI);}catch{this.error='Halaman gagal dimuatkan. Cuba browser sistem.';}return this.state();
 }
 async probe(){
  const state=this.state();if(!state.open)return {...state,connection:'CLOSED'};
  const url=this.window.webContents.getURL();if(!permitted(url)||new URL(url).hostname!=='aistudio.google.com')return {...state,connection:'LOGIN_REQUIRED'};
  try{const count=await this.window.webContents.executeJavaScript(`(${editorScript}).length`);return {...this.state(),connection:count===1?'EDITOR_FOUND':count>1?'EDITOR_AMBIGUOUS':'PAGE_NOT_READY'};}catch{return {...this.state(),connection:'PAGE_NOT_READY'};}
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
