import fs from 'fs';
import { youtubeAccessToken } from '../src/lib/publishing/youtube-token';
import { prisma } from '../src/lib/storage/prisma';
const ids=['K0TQHg4XCHY','JI2ewIT1KSM','6btaax7wp2E','DdggTdAzk84','VZsUxmzGyyE'];
async function main(){
 const token=await youtubeAccessToken();
 async function api(url:string,init:RequestInit={}){const r=await fetch('https://www.googleapis.com/youtube/v3/'+url,{...init,headers:{Authorization:`Bearer ${token}`,'Content-Type':'application/json'}});const d=await r.json();if(!r.ok)throw Error(JSON.stringify(d));return d;}
 const ch=await api('channels?part=id&mine=true');if(ch.items?.[0]?.id!=='UCXp7HkBIl1LgaznXuZHJyRg')throw Error('Wrong channel');
 const results=[];
 function stable(o:any):string{return JSON.stringify(o,Object.keys(o).sort())}
 for(const id of ids){
  const v=(await api(`videos?part=snippet,status&id=${id}`)).items[0];
  if(v.status.privacyStatus!=='private'||v.status.publishAt)throw Error('Draft state changed: '+id);
  if(v.snippet.defaultLanguage==='en-GB'){results.push({id,alreadyRepaired:true,title:v.snippet.title,status:v.status});console.log(id+' already en-GB');continue;}
  const snippet:Record<string,unknown>={};for(const k of ['title','description','tags','categoryId','defaultAudioLanguage'])if(v.snippet[k]!==undefined)snippet[k]=v.snippet[k];snippet.defaultLanguage='en-GB';
  await api('videos?part=snippet',{method:'PUT',body:JSON.stringify({id,snippet})});
  let a:any; for(let k=0;k<10;k++){a=(await api(`videos?part=snippet,status&id=${id}`)).items[0];if(a.snippet.defaultLanguage==='en-GB')break;await new Promise(r=>setTimeout(r,1000));}
  if(a.snippet.defaultLanguage!=='en-GB'||stable(a.status)!==stable(v.status)||a.snippet.title!==v.snippet.title||a.snippet.description!==v.snippet.description)throw Error('Readback mismatch '+id+' '+JSON.stringify({before:v.status,after:a.status,language:a.snippet.defaultLanguage,titleSame:a.snippet.title===v.snippet.title,descriptionSame:a.snippet.description===v.snippet.description}));
  results.push({id,before:{title:v.snippet.title,language:null,status:v.status},after:{title:a.snippet.title,language:a.snippet.defaultLanguage,status:a.status}});console.log(id+' language en-GB; title/status preserved');
 }
 fs.writeFileSync('../02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/10_Shorts/11_Upload-Package/s04_galen_stove/evidence_J0188_20261014/language_repairs.json',JSON.stringify(results,null,2)+'\n');
}
main().catch(e=>{console.error(e.message);process.exitCode=1}).finally(()=>prisma.$disconnect());
