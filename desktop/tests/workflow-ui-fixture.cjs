// Inspector-only test patch. No production IPC exposes these replacements.
function installFixture(appRoot){
 const {createRequire}=process.getBuiltinModule('node:module');const load=createRequire(appRoot+'/package.json');const Hub=load('./electron/agent-hub.cjs').AgentHub;const original={status:Hub.prototype.codexStatus,login:Hub.prototype.startLogin,generate:Hub.prototype.generate};let authenticated=false;
 Hub.prototype.codexStatus=async()=>authenticated;
 Hub.prototype.startLogin=function(){this.login={phase:'WAITING',url:'https://auth.openai.com/codex/device',code:'TEST-1234',error:''};globalThis.vfCompleteWorkflowLogin=()=>{authenticated=true;this.login={phase:'DONE',url:'',code:'',error:''};};return this.login;};
 Hub.prototype.generate=async()=>({title:'Rekod teratur',scenes:[{heading:'Susun rekod',body:'Simpan dokumen mengikut kategori.',narration:'Simpan dokumen mengikut kategori.',sourceId:'s1',quote:'Simpan dokumen mengikut kategori.',imageId:null}]});
 globalThis.vfRestoreWorkflowAgent=()=>{Hub.prototype.codexStatus=original.status;Hub.prototype.startLogin=original.login;Hub.prototype.generate=original.generate;delete globalThis.vfCompleteWorkflowLogin;delete globalThis.vfRestoreWorkflowAgent;};
}
module.exports={installFixture};
