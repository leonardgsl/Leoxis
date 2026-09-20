const { google } = require("googleapis");
const ID="1Bd8wmbV37vcx2kUpsdelKSDS70imhARr3ddQDJSnMRc", TAB="Registrations";
module.exports=async function(req,res){
 if(req.method!=="POST")return res.status(405).json({success:false});
 try{
  const d=req.body||{};
  if(!d.name||!d.email||!d.company||!d.role||!d.country)return res.status(400).json({success:false,error:"Missing required fields"});
  const email=String(d.email).trim().toLowerCase();
  const key=(process.env.GOOGLE_PRIVATE_KEY||"").trim().replace(/^["']|["']$/g,"").replace(/\\n/g,"\n");
  const auth=new google.auth.GoogleAuth({credentials:{client_email:process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,private_key:key},scopes:["https://www.googleapis.com/auth/spreadsheets"]});
  const sheets=google.sheets({version:"v4",auth});
  const existing=await sheets.spreadsheets.values.get({spreadsheetId:ID,range:`${TAB}!C2:C`});
  const duplicate=(existing.data.values||[]).some(r=>String(r[0]||"").trim().toLowerCase()===email);
  if(duplicate)return res.status(409).json({success:false,duplicate:true,message:"This email is already registered."});
  await sheets.spreadsheets.values.append({spreadsheetId:ID,range:`${TAB}!A:N`,valueInputOption:"USER_ENTERED",insertDataOption:"INSERT_ROWS",requestBody:{values:[[d.timestamp||new Date().toISOString(),d.name,email,d.company,d.role,d.country,d.stores||"",d.expansion||"",d.challenge||"",d.pilot||"",d.source||"leoxis.vercel.app","New","",""]]}});
  return res.status(200).json({success:true});
 }catch(e){console.error(e);return res.status(500).json({success:false});}
};
