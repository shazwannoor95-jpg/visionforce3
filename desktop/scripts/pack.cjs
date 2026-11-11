const fs=require('node:fs');const path=require('node:path');const crypto=require('node:crypto');const {spawnSync}=require('node:child_process');
const root=path.resolve(__dirname,'..'),version=require('../../version.json');
const dir=path.join(root,'release',version.display,crypto.randomUUID());fs.mkdirSync(dir,{recursive:true});
const record={display:version.display,directory:dir,platform:process.argv[2]||'win',status:'BUILDING',created:new Date().toISOString()};
function save(){fs.writeFileSync(path.join(root,'release/latest-build.json'),JSON.stringify(record,null,2)+'\n');fs.writeFileSync(path.join(dir,'build.json'),JSON.stringify(record,null,2)+'\n');}
const sha=spawnSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'});record.sourceCommit=sha.status===0?sha.stdout.trim():null;save();
const args=[require.resolve('electron-builder/out/cli/cli.js'),...(record.platform==='win'?['--win','nsis','portable','--x64']:['--linux','dir']),'--publish','never','-c.directories.output='+dir];
const result=spawnSync(process.execPath,args,{cwd:root,stdio:'inherit',env:process.env});record.status=result.status===0?'BUILT_NOT_TESTED':'FAILED';if(result.error)record.error=result.error.message;save();process.exit(result.status??1);
