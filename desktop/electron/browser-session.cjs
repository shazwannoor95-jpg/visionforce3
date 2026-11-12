const URL_AI='https://aistudio.google.com/';
function permitted(raw){try{const u=new URL(raw);return u.protocol==='https:'&&!u.username&&!u.password&&!u.port&&['aistudio.google.com','accounts.google.com'].includes(u.hostname);}catch{return false;}}
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
 close(){this.window?.close();return this.state();}
 async external(){await this.shell.openExternal(URL_AI);return {opened:true};}
}
module.exports={BrowserSession,permitted,URL_AI};
