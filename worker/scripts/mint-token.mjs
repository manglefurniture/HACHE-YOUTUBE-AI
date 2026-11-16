import {createHmac} from 'node:crypto';
const secret=process.env.SIGNING_SECRET;
const [prefix,methodsText='GET',ttlText='300']=process.argv.slice(2);
const ttl=Number(ttlText);
const methods=methodsText.split(',');
if(!secret||secret.length<32||!prefix||prefix.includes('..')||prefix.startsWith('/')||!(/^[a-zA-Z0-9_./-]+$/).test(prefix)||!Number.isInteger(ttl)||ttl<1||ttl>3600||methods.some(x=>!['GET','PUT'].includes(x))){
 console.error('Usage: SIGNING_SECRET=<32+ characters> node scripts/mint-token.mjs <prefix/> <GET|PUT|GET,PUT> [ttl_seconds<=3600]');
 process.exit(1);
}
const payload=Buffer.from(JSON.stringify({prefix,methods,exp:Math.floor(Date.now()/1000)+ttl})).toString('base64url');
const signature=createHmac('sha256',secret).update(payload).digest('base64url');
process.stdout.write(payload+'.'+signature+'\n');
