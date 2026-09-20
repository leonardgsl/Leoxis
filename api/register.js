const { google } = require("googleapis");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ success:false });
  try {
    const d = req.body || {};
    if (!d.name || !d.email || !d.company || !d.role || !d.country)
      return res.status(400).json({ success:false, error:"Missing required fields" });

    const auth = new google.auth.GoogleAuth({
      credentials: {
        client_email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
        private_key: (process.env.GOOGLE_PRIVATE_KEY || "").replace(/\\n/g, "\n"),
      },
      scopes: ["https://www.googleapis.com/auth/spreadsheets"],
    });
    const sheets = google.sheets({ version:"v4", auth });
    await sheets.spreadsheets.values.append({
      spreadsheetId:"1Bd8wmbV37vcx2kUpsdelKSDS70imhARr3ddQDJSnMRc",
      range:"Registrations!A:N",
      valueInputOption:"USER_ENTERED",
      requestBody:{ values:[[
        d.timestamp || new Date().toISOString(), d.name, d.email, d.company, d.role,
        d.country, d.stores || "", d.expansion || "", d.challenge || "", d.pilot || "",
        d.source || "leoxis.vercel.app", "New", "", ""
      ]] }
    });
    return res.status(200).json({ success:true });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success:false });
  }
};
