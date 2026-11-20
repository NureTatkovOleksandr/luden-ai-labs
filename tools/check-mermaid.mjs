import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const base=path.dirname(here);
const moduleRoot=process.env.LUDEN_NODE_MODULES||path.join(here,'node_modules');
const {JSDOM}=await import(pathToFileURL(path.join(moduleRoot,'jsdom/lib/api.js')).href);
const dom=new JSDOM('<!DOCTYPE html><html><body></body></html>');
globalThis.window=dom.window;globalThis.document=dom.window.document;
const {default:mermaid}=await import(pathToFileURL(path.join(moduleRoot,'mermaid/dist/mermaid.core.mjs')).href);
mermaid.initialize({startOnLoad:false,securityLevel:'strict'});
const content=fs.readFileSync(path.join(base,'docs/architecture.md'),'utf8');
const blocks=[...content.matchAll(/```mermaid\r?\n([\s\S]*?)\r?\n```/g)].map(m=>m[1].replace(/\r/g,''));
const diagrams=[];
for(let i=0;i<blocks.length;i++){
  try{await mermaid.parse(blocks[i]);diagrams.push({diagram:i+1,status:'PASS',type:blocks[i].split('\n')[0]});}
  catch(e){diagrams.push({diagram:i+1,status:'FAIL',error:String(e)});}
}
const version=JSON.parse(fs.readFileSync(path.join(moduleRoot,'mermaid/package.json'),'utf8')).version;
const result={architecture_sha256:crypto.createHash('sha256').update(content).digest('hex'),parser:'mermaid '+version,diagrams};
fs.writeFileSync(path.join(base,'verification/mermaid-validation.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify(result));
if(diagrams.length!==4||diagrams.some(d=>d.status!=='PASS'))process.exitCode=1;
