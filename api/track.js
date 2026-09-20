const { google } = require("googleapis");
const ID="1Bd8wmbV37vcx2kUpsdelKSDS70imhARr3ddQDJSnMRc";
module.exports=async function(req,res){
 if(req.method!=="POST")return res.status(405).json({ok:false});
 try{
  const d=req.body||{}, allowed=new Set(["page_view","expansion_click","registration_cta_click","registration_submit"]);
  if(!allowed.has(d.event))return res.status(400).json({ok:false});
  const key=(process.env.GOOGLE_PRIVATE_KEY||"").trim().replace(/^["']|["']$/g,"").replace(/\\n/g,"\n");
  const auth=new google.auth.GoogleAuth({credentials:{client_email:process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,private_key:key},scopes:["https://www.googleapis.com/auth/spreadsheets"]});
  const sheets=google.sheets({version:"v4",auth});
  const meta=await sheets.spreadsheets.get({spreadsheetId:ID,fields:"sheets.properties"});
  const exists=(meta.data.sheets||[]).some(x=>x.properties.title==="Analytics");
  if(!exists){
   await sheets.spreadsheets.batchUpdate({spreadsheetId:ID,requestBody:{requests:[{addSheet:{properties:{title:"Analytics"}}}]}});
   await sheets.spreadsheets.values.update({spreadsheetId:ID,range:"Analytics!A1:E1",valueInputOption:"RAW",requestBody:{values:[["Timestamp","Event","Path","Referrer","Label"]]}});
  }
  await sheets.spreadsheets.values.append({spreadsheetId:ID,range:"Analytics!A:E",valueInputOption:"USER_ENTERED",insertDataOption:"INSERT_ROWS",requestBody:{values:[[d.ts||new Date().toISOString(),d.event,String(d.path||"").slice(0,200),String(d.referrer||"").slice(0,500),String(d.label||"").slice(0,100)]]}});
  return res.status(200).json({ok:true});
 }catch(e){console.error(e);return res.status(500).json({ok:false});}
};
