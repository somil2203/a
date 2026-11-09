const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(300);if(process.argv[4])await p.evaluate(t=>window.renderAt&&window.renderAt(t),+process.argv[4]);await p.screenshot({path:process.argv[3]});await b.close();})();
