/**
 * VENDOR STATEMENT AUTO-SAVE — DriveSync.gs
 *
 * Watches Gmail for vendor replies with statement attachments
 * and saves them automatically to their Drive folder.
 *
 * Uses SPREADSHEET_ID and SHEET_NAME from Mail.gs (same project scope).
 *
 * HOW TO SET UP:
 * 1. In Apps Script, click the + next to Files → New script → name it DriveSync
 * 2. Paste this entire file
 * 3. Run setupStatementSaveTrigger() ONCE to activate the hourly check
 * 4. Authorize permissions when prompted
 */

// ── CONFIG ─────────────────────────────────────────────────────────────────────
const PROCESSED_LABEL       = "Statement Saved";   // Gmail label to mark processed emails
const FALLBACK_FOLDER_NAME  = "Vendor Statements"; // Root Drive folder if vendor has no Drive URL
const ALLOWED_EXTENSIONS    = ["pdf", "xlsx", "xls", "csv", "zip"];

// Column names in "Vendor info" sheet (must match exactly, case-insensitive)
const VI_COL_VENDOR    = "Vendor";
const VI_COL_EMAIL     = "Vendor email";
const VI_COL_DRIVE_URL = "Drive URL";


// ── MAIN ───────────────────────────────────────────────────────────────────────

/**
 * Main function: finds vendor reply emails with attachments and saves to Drive.
 * Runs on a time trigger (see setupStatementSaveTrigger below).
 */
function saveVendorStatements() {
  const vendorMap   = buildVendorMap_();
  const rootFolder  = getOrCreateFolder_(FALLBACK_FOLDER_NAME);
  const doneLabel   = getOrCreateLabel_(PROCESSED_LABEL);

  // Search Gmail for replies with attachments that haven't been processed yet.
  // Vendors reply with "Re: Updated Vendor Statement Request – [Vendor Name]"
  const query   = `subject:"Updated Vendor Statement Request" has:attachment -label:"${PROCESSED_LABEL}"`;
  const threads = GmailApp.search(query, 0, 100);

  let saved  = 0;
  let errors = [];

  for (const thread of threads) {
    let threadHasSave = false;

    for (const message of thread.getMessages()) {
      // Skip emails WE sent — only process vendor replies
      const fromEmail = extractEmail_(message.getFrom());
      if (isCookUnityEmail_(fromEmail)) continue;

      const attachments = message.getAttachments();
      if (attachments.length === 0) continue;

      // Identify vendor by their reply-from email
      const vendorInfo = vendorMap.get(fromEmail.toLowerCase())
                      || vendorMap.get(extractDomain_(fromEmail)); // fallback: match by domain

      const vendorName = vendorInfo
        ? vendorInfo.name
        : guessVendorFromSubject_(message.getSubject());

      if (!vendorName) {
        errors.push(`Unknown vendor: ${fromEmail} | ${message.getSubject()}`);
        continue;
      }

      // Resolve Drive folder: use vendor's Drive URL if set, else fallback root
      const vendorFolder = resolveVendorFolder_(vendorInfo, rootFolder, vendorName);

      // Date string for file naming
      const dateStr = Utilities.formatDate(
        message.getDate(),
        Session.getScriptTimeZone(),
        "yyyy-MM-dd"
      );

      for (const attachment of attachments) {
        const ext = attachment.getName().split(".").pop().toLowerCase();
        if (!ALLOWED_EXTENSIONS.includes(ext)) continue;

        // File name: "VendorName - 2026-04-14.pdf"
        const fileName = `${sanitizeName_(vendorName)} - ${dateStr}.${ext}`;

        try {
          if (fileExists_(vendorFolder, fileName)) {
            Logger.log(`Already saved: ${fileName}`);
            continue;
          }
          vendorFolder.createFile(attachment.copyBlob().setName(fileName));
          Logger.log(`✓ Saved: ${fileName} → ${vendorFolder.getName()}`);
          saved++;
          threadHasSave = true;
        } catch (e) {
          errors.push(`Error saving ${fileName}: ${e.message}`);
        }
      }
    }

    // Mark thread as processed (whether we saved or not — avoids re-scanning)
    thread.addLabel(doneLabel);
  }

  Logger.log(`Done. Files saved: ${saved} | Errors: ${errors.length}`);
  if (errors.length > 0) Logger.log("Errors:\n" + errors.join("\n"));
}


// ── TRIGGER SETUP ──────────────────────────────────────────────────────────────

/**
 * Sets up an hourly trigger for saveVendorStatements.
 * Run this ONCE manually.
 */
function setupStatementSaveTrigger() {
  deleteTriggerByName_("saveVendorStatements");

  ScriptApp.newTrigger("saveVendorStatements")
    .timeBased()
    .everyHours(1)
    .create();

  Logger.log("Trigger set: saveVendorStatements runs every hour.");
}

/**
 * Removes the auto-save trigger (to disable or reset).
 */
function removeStatementSaveTrigger() {
  deleteTriggerByName_("saveVendorStatements");
  Logger.log("Trigger removed.");
}


// ── HELPERS ────────────────────────────────────────────────────────────────────

/**
 * Reads "Vendor info" sheet and builds a Map:
 *   email (lowercase) → { name, driveUrl }
 * Also indexes by domain as fallback.
 */
function buildVendorMap_() {
  const ss    = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheetByName(SHEET_NAME) || ss.getActiveSheet();
  const data  = sheet.getDataRange().getValues();

  const headers = data[0].map(h => h.toString().toLowerCase().trim());

  const colVendor    = headers.indexOf(VI_COL_VENDOR.toLowerCase());
  const colEmail     = headers.indexOf(VI_COL_EMAIL.toLowerCase());
  const colDriveUrl  = headers.indexOf(VI_COL_DRIVE_URL.toLowerCase());

  if (colVendor === -1 || colEmail === -1) {
    throw new Error(`"Vendor info" must have columns "${VI_COL_VENDOR}" and "${VI_COL_EMAIL}".`);
  }

  const map = new Map();

  for (let i = 1; i < data.length; i++) {
    const name     = data[i][colVendor]   ? data[i][colVendor].toString().trim()   : "";
    const email    = data[i][colEmail]    ? data[i][colEmail].toString().trim()    : "";
    const driveUrl = colDriveUrl !== -1 && data[i][colDriveUrl]
                   ? data[i][colDriveUrl].toString().trim()
                   : "";

    if (!name || !email || !email.includes("@")) continue;

    const entry = { name, driveUrl };
    map.set(email.toLowerCase(), entry);

    // Also index by domain for fuzzy matching
    const domain = extractDomain_(email);
    if (domain && !map.has(domain)) {
      map.set(domain, entry);
    }
  }

  return map;
}

/**
 * Returns the Drive folder for a vendor.
 * Priority: vendor's Drive URL → subfolder inside root → root itself.
 */
function resolveVendorFolder_(vendorInfo, rootFolder, vendorName) {
  if (vendorInfo && vendorInfo.driveUrl) {
    const folder = getFolderFromUrl_(vendorInfo.driveUrl);
    if (folder) return folder;
  }
  // Fallback: create a subfolder named after the vendor inside the root folder
  return getOrCreateSubFolder_(rootFolder, vendorName);
}

/**
 * Extracts a Drive folder from a Drive URL.
 * Supports: /folders/FOLDER_ID and /drive/folders/FOLDER_ID
 */
function getFolderFromUrl_(url) {
  if (!url) return null;
  try {
    const match = url.match(/folders\/([a-zA-Z0-9_-]+)/);
    if (!match) return null;
    return DriveApp.getFolderById(match[1]);
  } catch (e) {
    Logger.log(`Could not open Drive folder from URL: ${url} — ${e.message}`);
    return null;
  }
}

/**
 * Gets or creates a Drive folder by name at the root level.
 */
function getOrCreateFolder_(name) {
  const folders = DriveApp.getFoldersByName(name);
  if (folders.hasNext()) return folders.next();
  return DriveApp.createFolder(name);
}

/**
 * Gets or creates a subfolder inside a parent folder.
 */
function getOrCreateSubFolder_(parent, name) {
  const safe = sanitizeName_(name);
  const folders = parent.getFoldersByName(safe);
  if (folders.hasNext()) return folders.next();
  return parent.createFolder(safe);
}

/**
 * Gets or creates a Gmail label.
 */
function getOrCreateLabel_(name) {
  return GmailApp.getUserLabelByName(name) || GmailApp.createLabel(name);
}

/**
 * Checks if a file with the given name already exists in a folder.
 */
function fileExists_(folder, fileName) {
  const files = folder.getFilesByName(fileName);
  return files.hasNext();
}

/**
 * Extracts the raw email address from a "Name <email@domain.com>" string.
 */
function extractEmail_(from) {
  const match = from.match(/<([^>]+)>/);
  return match ? match[1].trim() : from.trim();
}

/**
 * Extracts the domain from an email address.
 */
function extractDomain_(email) {
  const parts = email.split("@");
  return parts.length === 2 ? parts[1].toLowerCase() : "";
}

/**
 * Returns true if the email belongs to Cook Unity.
 */
function isCookUnityEmail_(email) {
  return email.toLowerCase().includes("cookunity.com");
}

/**
 * Tries to extract the vendor name from the email subject.
 * Subject format: "Re: Updated Vendor Statement Request – VendorName"
 */
function guessVendorFromSubject_(subject) {
  const match = subject.match(/Statement Request\s*[–\-]\s*(.+)/i);
  return match ? match[1].trim() : null;
}

/**
 * Removes characters that are invalid in file/folder names.
 */
function sanitizeName_(name) {
  return name.replace(/[\/\\:*?"<>|]/g, " ").replace(/\s+/g, " ").trim();
}

/**
 * Deletes all triggers matching a function name.
 */
function deleteTriggerByName_(functionName) {
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === functionName) ScriptApp.deleteTrigger(t);
  });
}


// ── TEST ───────────────────────────────────────────────────────────────────────

/**
 * TEST: runs the save manually without the trigger.
 * Check Execution Log for results.
 */
function testSaveStatements() {
  saveVendorStatements();
}
