const {fileURLToPath}=require('node:url');const path=require('node:path');
function isAllowedFrame({url,senderMatches,mainFrame},expectedFile,platform=process.platform){
 if(!senderMatches||!mainFrame||typeof url!=='string')return false;
 try{const parsed=new URL(url);if(parsed.protocol!=='file:'||parsed.hostname||parsed.username||parsed.password||parsed.search)return false;const windows=platform==='win32';const actual=fileURLToPath(parsed,{windows});const paths=windows?path.win32:path.posix;return paths.normalize(actual)===paths.normalize(expectedFile);}catch{return false;}
}
module.exports={isAllowedFrame};
