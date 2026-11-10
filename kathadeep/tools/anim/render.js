// node render.js out.mp4 [t0 t1] | stills: node render.js --stills dir t1 t2 ...
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>{console.error('PAGEERR',e.message);});
await p.goto('file://'+process.cwd()+'/index.html');if(process.env.NOSUBS)await p.evaluate(()=>window.NOSUBS=1);await p.evaluate(async()=>{for(const f of ['92px Anton','24px SpaceMono','50px Baloo']){try{await document.fonts.load(f)}catch(e){}}await document.fonts.ready;});
const a=process.argv.slice(2);
if(a[0]==='--stills'){fs.mkdirSync(a[1],{recursive:true});for(const t of a.slice(2)){await p.evaluate(t=>{renderAt(t);if(window.NOSUBS)document.getElementById('subs').innerHTML='';},+t);await p.screenshot({path:`${a[1]}/s_${(+t).toFixed(2)}.jpg`,type:'jpeg',quality:85});}await b.close();return;}
const end=await p.evaluate(()=>TIMES.END);const t0=+(a[1]||0),t1=+(a[2]||end);
const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',a[0]],{stdio:['pipe','inherit','inherit']});
const n0=Math.round(t0*30),n1=Math.round(t1*30);
for(let f=n0;f<n1;f++){await p.evaluate(t=>renderAt(t),f/30);const buf=await p.screenshot({type:'jpeg',quality:94});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(f%150===0)console.log('frame',f,'/',n1);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();})();
