const {contextBridge,ipcRenderer}=require('electron');
const invoke=(name,...args)=>ipcRenderer.invoke('vf:'+name,...args);
contextBridge.exposeInMainWorld('visionforge',Object.freeze({
 saveCloud:origin=>invoke('saveCloud',origin),generate:(id,prompt)=>invoke('generate',id,prompt),pollRender:id=>invoke('pollRender',id),saveDraft:(id,text)=>invoke('saveDraft',id,text),bootstrap:()=>invoke('bootstrap'),createProject:name=>invoke('createProject',name),openProject:id=>invoke('openProject',id),
 send:(id,text)=>invoke('send',id,text),attach:id=>invoke('attach',id),backup:()=>invoke('backup'),restorePlan:id=>invoke('restorePlan',id),restore:id=>invoke('restore',id),
 testProvider:id=>invoke('testProvider',id),saveProvider:(id,key)=>invoke('saveProvider',id,key),exportResult:id=>invoke('exportResult',id),exportProject:id=>invoke('exportProject',id),openBackup:()=>invoke('openBackup'),
 browserSpeech:()=>invoke('browserSpeech'),browserAudioImport:(id,audioId)=>invoke('browserAudioImport',id,audioId),
 browserFill:text=>invoke('browserFill',text),browserSelection:()=>invoke('browserSelection'),browserImport:(id,text)=>invoke('browserImport',id,text),
 browserOpen:()=>invoke('browserOpen'),browserState:()=>invoke('browserState'),browserClose:()=>invoke('browserClose'),browserExternal:()=>invoke('browserExternal'),
 health:()=>invoke('health')
}));
