const { google } = require("googleapis");
const SPREADSHEET_ID = "1Bd8wmbV37vcx2kUpsdelKSDS70imhARr3ddQDJSnMRc";
module.exports = async function handler(req,res){
 const steps=[]; const add=(step,ok,detail)=>steps.push({step,ok,detail});
 try{
  const email=process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL||"";
  const raw=process.env.GOOGLE_PRIVATE_KEY||"";
  add("Service account email",!!email,email?"Present":"Missing");
  add("Private key",!!raw,raw?"Present (hidden)":"Missing");
  if(!email||!raw)return res.status(500).json({ok:false,steps});
  const key=raw.trim().replace(/^["']|["']$/g,"").replace(/\\n/g,"\n");
  const pem=key.includes("-----BEGIN PRIVATE KEY-----")&&key.includes("-----END PRIVATE KEY-----");
  add("Private key PEM format",pem,pem?"Valid markers found":"PEM markers missing");
  if(!pem)return res.status(500).json({ok:false,steps});
  const auth=new google.auth.GoogleAuth({credentials:{client_email:email,private_key:key},scopes:["https://www.googleapis.com/auth/spreadsheets"]});
  const client=await auth.getClient(); await client.getAccessToken();
  add("Google authentication",true,"Access token obtained");
  const sheets=google.sheets({version:"v4",auth});
  const meta=await sheets.spreadsheets.get({spreadsheetId:SPREADSHEET_ID,fields:"properties.title,sheets.properties.title"});
  const titles=(meta.data.sheets||[]).map(s=>s.properties.title);
  add("Spreadsheet access",true,meta.data.properties?.title||"Accessible");
  const has=titles.includes("Registrations");
  add("Registrations tab",has,has?"Found":`Not found. Tabs: ${titles.join(", ")}`);
  if(!has)return res.status(500).json({ok:false,steps});
  const row=[new Date().toISOString(),"LEOXIS HEALTH CHECK","healthcheck@leoxis.local","LEOXIS","System Test","Malaysia","","","","","registration-health","TEST","",""];
  const a=await sheets.spreadsheets.values.append({spreadsheetId:SPREADSHEET_ID,range:"Registrations!A:N",valueInputOption:"USER_ENTERED",insertDataOption:"INSERT_ROWS",requestBody:{values:[row]}});
  add("Test write",true,a.data.updates?.updatedRange||"Row appended");
  return res.status(200).json({ok:true,message:"LEOXIS registration database connection is healthy.",steps});
 }catch(e){
  add("Failure",false,e?.response?.data?.error?.message||e?.message||String(e));
  return res.status(500).json({ok:false,steps});
 }
};
