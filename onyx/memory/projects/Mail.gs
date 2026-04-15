/**
 * VENDOR STATEMENT REQUEST - Weekly Email Automation
 *
 * Sends every Monday at 8:00 AM (Argentina time / ART = UTC-3)
 * to all vendors with "Lu" in the Owner column.
 *
 * HOW TO SET UP:
 * 1. Open your Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Paste this entire script and click Save
 * 4. Run setupTrigger() ONCE to activate the weekly schedule
 * 5. Authorize the permissions when prompted
 */

// ── CONFIGURATION ──────────────────────────────────────────────────────────────
const SPREADSHEET_ID = "1_ByYPzghRzKNdz1wcVvWMj8NhlDWgthoTVHAMpyIX-A";
const SHEET_NAME     = "Vendor info";
const OWNER_FILTER   = "Lu";

const COL_VENDOR = 1;  // Column A: Vendor name
const COL_OWNER  = 2;  // Column B: Owner
const COL_EMAIL  = 3;  // Column C: Vendor email

// ── TEST MODE ──────────────────────────────────────────────────────────────────
const TEST_MODE  = false;                 // producción — manda a vendors reales
const TEST_EMAIL = "lucia@cookunity.com"; // solo se usa si TEST_MODE = true
// ──────────────────────────────────────────────────────────────────────────────


/**
 * Main function: reads the sheet and sends emails to matching vendors.
 * En TEST_MODE todos los mails van a TEST_EMAIL con asunto [TEST].
 */
function sendVendorStatementRequests() {
  const ss    = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheetByName(SHEET_NAME) || ss.getActiveSheet();
  const data  = sheet.getDataRange().getValues();

  let emailsSent    = 0;
  let emailsSkipped = 0;
  const errors      = [];

  for (let i = 1; i < data.length; i++) {
    const vendorName = String(data[i][COL_VENDOR - 1]).trim();
    const owner      = String(data[i][COL_OWNER  - 1]).trim();
    const email      = String(data[i][COL_EMAIL  - 1]).trim();

    if (!vendorName || !email) continue;
    if (owner !== OWNER_FILTER) continue;
    if (!email.includes("@")) {
      errors.push(`Row ${i + 1} - ${vendorName}: invalid email "${email}"`);
      emailsSkipped++;
      continue;
    }

    const recipient = TEST_MODE ? TEST_EMAIL : email;
    const subject   = TEST_MODE
      ? `[TEST → ${email}] Updated Vendor Statement Request – ${vendorName}`
      : `Updated Vendor Statement Request – ${vendorName}`;
    const body = buildEmailBody(vendorName);

    try {
      GmailApp.sendEmail(recipient, subject, body, {
        name: "Lu – Cook Unity Accounts Payable",
        cc:   TEST_MODE ? "" : "invoices@cookunity.com",
      });
      emailsSent++;
      Logger.log(`${TEST_MODE ? "[TEST] " : ""}Sent: ${vendorName} → ${recipient}`);
    } catch (e) {
      errors.push(`Row ${i + 1} - ${vendorName} <${email}>: ${e.message}`);
      emailsSkipped++;
    }
  }

  Logger.log(`Done. Sent: ${emailsSent} | Skipped/Errors: ${emailsSkipped}`);
  if (errors.length > 0) Logger.log("Errors:\n" + errors.join("\n"));
}


/**
 * Builds the plain-text email body for a given vendor.
 */
function buildEmailBody(vendorName) {
  return `Dear ${vendorName} Team,

I hope this message finds you well.

I am reaching out on behalf of Cook Unity to kindly request an updated vendor statement for our account. Could you please send us your most recent statement at your earliest convenience? This will help us ensure our records are accurate and up to date.

If you have any questions or need any information from our end, please don't hesitate to reach out.

Thank you for your continued partnership with Cook Unity. We truly appreciate your support.

Best regards,

Lu
Accounts Payable
Cook Unity`;
}


/**
 * Creates a time-based trigger: every Monday at 8:00 AM Argentina time.
 * ART = UTC-3, so 8 AM ART = 11:00 AM UTC.
 * Run this function ONCE to activate the schedule.
 */
function setupTrigger() {
  deleteTrigger("sendVendorStatementRequests");

  ScriptApp.newTrigger("sendVendorStatementRequests")
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(11)
    .nearMinute(0)
    .create();

  Logger.log("Trigger set: every Monday at ~8:00 AM Argentina time.");
}


/**
 * Removes all triggers for a given function name.
 */
function deleteTrigger(functionName) {
  ScriptApp.getProjectTriggers().forEach(trigger => {
    if (trigger.getHandlerFunction() === functionName) {
      ScriptApp.deleteTrigger(trigger);
    }
  });
}
