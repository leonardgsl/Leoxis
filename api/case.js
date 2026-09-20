const { google } = require("googleapis");
const ID="1Bd8wmbV37vcx2kUpsdelKSDS70imhARr3ddQDJSnMRc";
const TAB="Expansion Cases";
const HEADERS=["Timestamp","Case ID","Country","City","Site Name","Store Format","Currency","Selling Area","Lease Term Years","Capex","Deposit","Monthly Rent","Service Charge","Turnover Rent %","Projected Monthly Sales","Gross Margin %","Opex Mode","Payroll","Utilities","Maintenance","Other Store Opex","Total Monthly Store Opex","Catchment Population","Footfall","Ramp Up Months","Competitors","Notes","Evidence Sales","Evidence Rent","Evidence Capex","Evidence Margin","Evidence Footfall","Evidence Catchment","EBITDA","EBITDA Margin %","Investment","Payback Months","Breakeven Sales","Occupancy %","Economic Status","Evidence Confidence","Evidence Coverage %","Target Margin %","Target Payback Months"];
module.exports=async function(req,res){
 if(req.method!=="POST")return res.status(405).json({ok:false});
 try{
  const d=req.body||{}, i=d.input||{}, o=d.output||{};
  if(!d.caseId||!i.country||!i.siteName)return res.status(400).json({ok:false});
  const key=(process.env.GOOGLE_PRIVATE_KEY||"").trim().replace(/^["']|["']$/g,"").replace(/\\n/g,"\n");
  const auth=new google.auth.GoogleAuth({credentials:{client_email:process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,private_key:key},scopes:["https://www.googleapis.com/auth/spreadsheets"]});
  const sheets=google.sheets({version:"v4",auth});
  const meta=await sheets.spreadsheets.get({spreadsheetId:ID,fields:"sheets.properties"});
  const exists=(meta.data.sheets||[]).some(x=>x.properties.title===TAB);
  if(!exists){
   await sheets.spreadsheets.batchUpdate({spreadsheetId:ID,requestBody:{requests:[{addSheet:{properties:{title:TAB}}}]}});
   await sheets.spreadsheets.values.update({spreadsheetId:ID,range:`${TAB}!A1:AR1`,valueInputOption:"RAW",requestBody:{values:[HEADERS]}});
  }
  const ev=i.evidence||{};
  const row=[d.timestamp||new Date().toISOString(),d.caseId,i.country||"",i.city||"",i.siteName||"",i.storeFormat||"",i.currency||"",i.sellingArea??"",i.leaseTermYears??"",i.capex??"",i.deposit??"",i.monthlyRent??"",i.serviceCharge??"",i.turnoverRentPct??"",i.projectedMonthlySales??"",i.grossMarginPct??"",i.opexMode||"",i.payroll??"",i.utilities??"",i.maintenance??"",i.otherStoreOpex??"",i.totalMonthlyStoreOpex??"",i.catchmentPopulation??"",i.footfall??"",i.rampUpMonths??"",String(i.competitors||"").slice(0,1000),String(i.notes||"").slice(0,2000),!!ev.sales,!!ev.rent,!!ev.capex,!!ev.margin,!!ev.footfall,!!ev.catchment,o.ebitda??"",o.ebitdaMargin??"",o.investment??"",o.paybackMonths??"",o.breakevenSales??"",o.occupancyPct??"",o.economicStatus||"",o.evidenceConfidence||"",o.evidenceCoverage??"",o.targetMargin??"",o.targetPayback??""];
  await sheets.spreadsheets.values.append({spreadsheetId:ID,range:`${TAB}!A:AR`,valueInputOption:"USER_ENTERED",insertDataOption:"INSERT_ROWS",requestBody:{values:[row]}});
  return res.status(200).json({ok:true,caseId:d.caseId});
 }catch(e){console.error(e);return res.status(500).json({ok:false});}
};
