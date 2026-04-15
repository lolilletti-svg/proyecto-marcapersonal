/***********************
 * MENÚ
 ***********************/
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('📌 Open Items')
    .addItem('1) Generar Current', 'generarCurrent')
    .addItem('2) Copiar análisis a tab semanal', 'copiarAnalisisATabSemanal')
    .addToUi();
}

/***********************
 * CONFIG: leer Principal (col B labels / col C values)
 ***********************/
function getPrincipalConfig_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName('Principal');
  if (!sh) throw new Error('No encuentro la tab "Principal".');

  const lastRow = sh.getLastRow();
  const range = sh.getRange(1, 2, lastRow, 2).getValues(); // B:C
  const map = new Map();

  for (const [label, value] of range) {
    const key = (label ?? '').toString().trim();
    if (!key) continue;
    map.set(key, value);
  }

  function mustGet(label) {
    if (!map.has(label)) throw new Error(`Falta en Principal el label: "${label}"`);
    const v = map.get(label);
    if (v === null || v === undefined || v === '') throw new Error(`Principal "${label}" está vacío.`); // FIX 1: v === null
    return v;
  }

  const sourceTab = mustGet('Tab a analizar').toString().trim();
  const percentRaw = mustGet('% sobre total a analizar');
  const outTab = mustGet('Nombre de tab de salida').toString().trim();
  const copyTo = (map.get('Copiar notas a tab') ?? '').toString().trim() || sourceTab;

  return {
    sourceTab,
    outTab,
    copyTo,
    percent: parsePercent_(percentRaw)
  };
}

function parsePercent_(v) {
  const s = (v ?? '').toString().trim();
  if (!s) throw new Error('El % en Principal está vacío.');

  if (s.includes('%')) {
    const n = parseFloat(s.replace('%', '').trim());
    if (isNaN(n)) throw new Error(`No pude interpretar el %: "${s}"`);
    return n / 100;
  }

  const n = parseFloat(s);
  if (isNaN(n)) throw new Error(`No pude interpretar el %: "${s}"`);
  return n > 1 ? n / 100 : n;
}

/***********************
 * PARSEO MONEDA (US + ES) + paréntesis negativos
 * Soporta:
 *  - $9954
 *  - $99.756,54
 *  - ($93.514,41)
 *  - (93,514.41)
 ***********************/
function parseMoney_(v) {
  if (v === null || v === undefined || v === '') return 0;
  if (typeof v === 'number') return v;

  let s = v.toString().trim();
  if (!s) return 0;

  // Paréntesis = negativo
  let neg = false;
  if (s.startsWith('(') && s.endsWith(')')) {
    neg = true;
    s = s.slice(1, -1).trim();
  }

  // Quitar $
  s = s.replace(/\$/g, '').trim();

  // Signo negativo explícito
  if (s.startsWith('-')) {
    neg = true;
    s = s.slice(1).trim();
  }

  // Quitar espacios
  s = s.replace(/\s+/g, '');

  const hasDot = s.includes('.');
  const hasComma = s.includes(',');

  if (hasDot && hasComma) {
    const lastDot = s.lastIndexOf('.');
    const lastComma = s.lastIndexOf(',');
    if (lastComma > lastDot) {
      // ES: 99.756,54
      s = s.replace(/\./g, '');
      s = s.replace(/,/g, '.');
    } else {
      // US: 99,756.54
      s = s.replace(/,/g, '');
    }
  } else if (hasComma && !hasDot) {
    // ES: 756,54
    s = s.replace(/,/g, '.');
  } else {
    // Solo dot o ninguno: quitar comas por las dudas
    s = s.replace(/,/g, '');
  }

  const n = parseFloat(s);
  if (isNaN(n)) return 0;

  return neg ? -n : n;
}

/***********************
 * NORMALIZACIÓN PARA MATCH CON Vendor info (mantiene location)
 ***********************/
function getBaseVendorName_(name) {
  let s = (name ?? '').toString().toUpperCase().trim();
  s = s.replace(/\b(LLC|INC|INCORPORATED|LTD|LIMITED|CORP|CORPORATION|CO|COMPANY|LP|PLC)\b/g, "");
  s = s.replace(/[^\w\s]/g, " ");
  s = s.replace(/\s+/g, " ").trim();
  return s;
}

function truthyYes_(v) {
  const s = (v ?? '').toString().trim().toUpperCase();
  return s === 'YES' || s === 'Y' || s === 'TRUE' || s === 'SI' || s === 'SÍ' || s === '1';
}

/***********************
 * Header utils
 ***********************/
function getColumnIndexByHeader_(headersRow, headerName) {
  const target = headerName.toString().replace(/\s+/g, ' ').trim().toUpperCase();
  for (let i = 0; i < headersRow.length; i++) { // FIX 2: headersRow (era "adersRow")
    const h = (headersRow[i] ?? '').toString().replace(/\s+/g, ' ').trim().toUpperCase();
    if (h === target) return i;
  }
  return -1;
}

/***********************
 * Selección Top X% por acumulado (value siempre positivo)
 * items: [{idx, value}]
 ***********************/
function selectTopPercentByAccum_(items, percent) {
  const sorted = [...items].sort((a, b) => (b.value - a.value));
  const total = sorted.reduce((sum, x) => sum + (x.value || 0), 0);
  const target = total * percent;

  let acc = 0;
  const selected = new Set();

  for (const it of sorted) {
    if (acc < target) {
      selected.add(it.idx);
      acc += (it.value || 0);
    } else {
      break;
    }
  }
  return selected;
}

/***********************
 * 1) GENERAR CURRENT
 * Current = Vendor | Total | Owner | Vendor email | Drive | Motivo | Check | Notes
 * Selección = 100% Plate + Top X% deuda + Top X% crédito (por magnitud)
 * HEADER_ROW=7, START_ROW=8
 ***********************/
function generarCurrent() { // FIX 3: paréntesis de cierre + llave de apertura
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const cfg = getPrincipalConfig_();

  const shSource = ss.getSheetByName(cfg.sourceTab);
  if (!shSource) throw new Error(`No encuentro la tab semanal "${cfg.sourceTab}".`);

  const shVendor = ss.getSheetByName('Vendor info');
  if (!shVendor) throw new Error('No encuentro la tab "Vendor info".');

  const shOut = ss.getSheetByName(cfg.outTab) || ss.insertSheet(cfg.outTab);

  /******** Vendor info (por headers) ********/
  const vData = shVendor.getDataRange().getValues();
  if (vData.length < 2) throw new Error('"Vendor info" no tiene datos.');

  const vHead = vData[0].map(x => (x ?? '').toString().trim());
  const colVVendor   = vHead.indexOf('Vendor');
  const colVOwner    = vHead.indexOf('Owner');
  const colVEmail    = vHead.indexOf('Vendor email');
  const colVDriveUrl = vHead.indexOf('Drive URL');
  const colVMand     = vHead.indexOf('Mandatory');

  if (colVVendor === -1) throw new Error('En "Vendor info" falta header "Vendor".');
  if (colVOwner  === -1) throw new Error('En "Vendor info" falta header "Owner".');
  if (colVEmail  === -1) throw new Error('En "Vendor info" falta header "Vendor email".');
  if (colVDriveUrl === -1) throw new Error('En "Vendor info" falta header "Drive URL".');
  if (colVMand   === -1) throw new Error('En "Vendor info" falta header "Mandatory".');

  const vendorInfoByBase = new Map(); // base -> {owner,email,driveUrl,mandatory}
  for (let r = 1; r < vData.length; r++) {
    const vendor = vData[r][colVVendor];
    if (!vendor) continue;

    const base = getBaseVendorName_(vendor);
    if (!vendorInfoByBase.has(base)) {
      vendorInfoByBase.set(base, {
        owner:    (vData[r][colVOwner]    ?? '').toString().trim(),
        email:    (vData[r][colVEmail]    ?? '').toString().trim(),
        driveUrl: (vData[r][colVDriveUrl] ?? '').toString().trim(),
        mandatory: truthyYes_(vData[r][colVMand])
      });
    } else {
      const existing = vendorInfoByBase.get(base);
      const mand = truthyYes_(vData[r][colVMand]);
      if (mand) existing.mandatory = true;
      if (!existing.owner)    existing.owner    = (vData[r][colVOwner]    ?? '').toString().trim();
      if (!existing.email)    existing.email    = (vData[r][colVEmail]    ?? '').toString().trim();
      if (!existing.driveUrl) existing.driveUrl = (vData[r][colVDriveUrl] ?? '').toString().trim();
    }
  }

  /******** Leer tab semanal (header fila 7, data desde fila 8) ********/
  const HEADER_ROW = 7;
  const START_ROW  = 8;

  const lastCol = shSource.getLastColumn();
  const lastRow = shSource.getLastRow();
  if (lastRow < START_ROW) throw new Error(`La tab "${cfg.sourceTab}" no tiene filas desde la ${START_ROW}.`);

  const headers = shSource.getRange(HEADER_ROW, 1, 1, lastCol).getValues()[0];

  const colVendor = getColumnIndexByHeader_(headers, 'Vendor');
  const colTotal  = getColumnIndexByHeader_(headers, 'Total');

  if (colVendor === -1) throw new Error(`No encontré header "Vendor" en fila ${HEADER_ROW} de "${cfg.sourceTab}".`);
  if (colTotal  === -1) throw new Error(`No encontré header "Total" en fila ${HEADER_ROW} de "${cfg.sourceTab}".`);

  const data = shSource.getRange(START_ROW, 1, lastRow - START_ROW + 1, lastCol).getValues();

  const rows = [];
  for (const r of data) {
    const vendor = (r[colVendor] ?? '').toString().trim();
    if (!vendor) continue;

    const total = parseMoney_(r[colTotal]);
    const base  = getBaseVendorName_(vendor);
    const info  = vendorInfoByBase.get(base) || { owner: '', email: '', driveUrl: '', mandatory: false };

    rows.push({
      vendor,
      total,
      mandatory: !!info.mandatory,
      owner:    info.owner    || '',
      email:    info.email    || '',
      driveUrl: info.driveUrl || ''
    });
  }

  if (rows.length === 0) throw new Error(`No encontré vendors en "${cfg.sourceTab}" desde la fila ${START_ROW}.`);

  /******** Selección: Plate + Top X% Deuda + Top X% Créditos ********/
  const debtItems   = [];
  const creditItems = [];

  for (let i = 0; i < rows.length; i++) {
    const t = rows[i].total || 0;
    if (t > 0) debtItems.push({ idx: i, value: t });          // FIX 4: debtItems (era "deems")
    if (t < 0) creditItems.push({ idx: i, value: Math.abs(t) });
  }

  const selectedDebt   = selectTopPercentByAccum_(debtItems,   cfg.percent);
  const selectedCredit = selectTopPercentByAccum_(creditItems, cfg.percent);

  /******** Preservar Check/Notes existentes ********/
  const existingMap = new Map(); // vendor -> {checked, notes}
  const outLastRowBefore = shOut.getLastRow();
  if (outLastRowBefore >= 2) {
    const existing = shOut.getRange(2, 1, outLastRowBefore - 1, 8).getValues();
    for (const row of existing) {
      const v = (row[0] ?? '').toString().trim();
      if (!v) continue;
      existingMap.set(v, { checked: row[6], notes: row[7] });
    }
  }

  /******** Output ********/
  // A Vendor | B Total | C Owner | D Vendor email | E Drive | F Motivo | G Check | H Notes
  const output = [];

  for (let i = 0; i < rows.length; i++) {
    const r     = rows[i];
    const inPct = selectedDebt.has(i) || selectedCredit.has(i);
    const analyze = r.mandatory || inPct;
    if (!analyze) continue;

    const motivo = (r.mandatory && inPct) ? 'Both'
                 : (r.mandatory)          ? 'Plate'
                 : '%';

    const preserved = existingMap.get(r.vendor) || { checked: false, notes: '' };
    const driveCell = r.driveUrl ? `=HYPERLINK("${r.driveUrl}","📁 Drive")` : '';

    output.push([
      r.vendor,
      r.total,
      r.owner,
      r.email,
      driveCell,
      motivo,
      preserved.checked === true,
      preserved.notes || ''
    ]);
  }

  // Orden: deuda arriba (total desc), luego créditos por magnitud
  output.sort((a, b) => {
    const aT  = a[1] || 0;
    const bT  = b[1] || 0;
    const aPos = aT >= 0;
    const bPos = bT >= 0;
    if (aPos && !bPos) return -1;
    if (!aPos && bPos) return 1;
    if (aPos && bPos)  return bT - aT;
    return Math.abs(bT) - Math.abs(aT);
  });

  /******** Pintar Current ********/
  shOut.clear();

  const headersOut = [['Vendor','Total','Owner','Vendor email','Drive','Motivo','Check','Notes']];
  shOut.getRange(1, 1, 1, 8).setValues(headersOut); // FIX 6: getRange(1,1,1,8) — 1 fila, 8 cols

  if (output.length > 0) {
    shOut.getRange(2, 1, output.length, 8).setValues(output);
    shOut.getRange(2, 7, output.length, 1).insertCheckboxes();
  }

  /******** Formato ********/
  const headerRange = shOut.getRange(1, 1, 1, 8);
  headerRange
    .setFontWeight('bold')
    .setHorizontalAlignment('center')
    .setVerticalAlignment('middle')
    .setWrap(true)
    .setBackground('#FFF2CC');

  shOut.setFrozenRows(1);

  shOut.setColumnWidth(1, 320);
  shOut.setColumnWidth(2, 160);
  shOut.setColumnWidth(3, 160);
  shOut.setColumnWidth(4, 240);
  shOut.setColumnWidth(5, 110);
  shOut.setColumnWidth(6, 110);
  shOut.setColumnWidth(7, 90);
  shOut.setColumnWidth(8, 380);

  const n = output.length;
  if (n > 0) {
    shOut.getRange(2, 1, n, 1).setHorizontalAlignment('left');
    shOut.getRange(2, 2, n, 1).setHorizontalAlignment('right');
    shOut.getRange(2, 3, n, 1).setHorizontalAlignment('left');
    shOut.getRange(2, 4, n, 1).setHorizontalAlignment('left');
    shOut.getRange(2, 5, n, 1).setHorizontalAlignment('center');
    shOut.getRange(2, 6, n, 1).setHorizontalAlignment('center');
    shOut.getRange(2, 7, n, 1).setHorizontalAlignment('center');
    shOut.getRange(2, 8, n, 1).setHorizontalAlignment('left');

    shOut.getRange(2, 2, n, 1).setNumberFormat('$#,##0.00');

    const lightGray = '#F5F5F5';
    const white     = '#FFFFFF';
    const bg = [];
    for (let i = 0; i < n; i++) {
      const color = (i % 2 === 0) ? white : lightGray;
      bg.push([color, color, color, color, color, color, color, color]);
    }
    shOut.getRange(2, 1, n, 8).setBackgrounds(bg);
    headerRange.setBackground('#FFF2CC');
  }
}

/***********************
 * 2) COPIAR ANALISIS A TAB SEMANAL
 * HEADER_ROW=7, START_ROW=8
 ***********************/
function copiarAnalisisATabSemanal() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const cfg = getPrincipalConfig_();

  const shOut = ss.getSheetByName(cfg.outTab);
  if (!shOut) throw new Error(`No encuentro la tab "${cfg.outTab}" (Current). Generala primero.`);

  const shDest = ss.getSheetByName(cfg.copyTo);
  if (!shDest) throw new Error(`No encuentro la tab destino "${cfg.copyTo}".`);

  const outLastRow = shOut.getLastRow();
  if (outLastRow < 2) throw new Error('"Current" no tiene filas para copiar.');

  const cur = shOut.getRange(2, 1, outLastRow - 1, 8).getValues();
  // cols: 0 Vendor, 2 Owner, 6 Check, 7 Notes
  const curRows = cur
    .map(r => ({
      vendor:   (r[0] ?? '').toString().trim(),
      owner:    (r[2] ?? '').toString().trim(),
      reviewed: r[6] === true,
      notes:    (r[7] ?? '').toString()
    }))
    .filter(x => x.vendor);

  if (curRows.length === 0) throw new Error('No hay vendors válidos en Current.');

  const HEADER_ROW = 7;
  const START_ROW  = 8;

  const destLastCol = shDest.getLastColumn();
  const headerVals  = shDest
    .getRange(HEADER_ROW, 1, 1, destLastCol)
    .getValues()[0]
    .map(x => (x ?? '').toString().trim());

  const H_OWNER    = 'Analysis Owner';
  const H_REVIEWED = 'Reviewed';
  const H_NOTES    = 'Analysis Notes'; // FIX 5: const (era "cont")
  const H_SAVED    = 'Saved at';

  function ensureCol(headerName) {
    let idx = headerVals.indexOf(headerName);
    if (idx !== -1) return idx + 1;

    const newCol = shDest.getLastColumn() + 1;
    shDest.getRange(HEADER_ROW, newCol).setValue(headerName);
    headerVals.push(headerName);
    return newCol;
  }

  const colOwner    = ensureCol(H_OWNER);
  const colReviewed = ensureCol(H_REVIEWED);
  const colNotes    = ensureCol(H_NOTES);
  const colSaved    = ensureCol(H_SAVED);

  const destLastRow = shDest.getLastRow();
  if (destLastRow < START_ROW) throw new Error(`La tab "${cfg.copyTo}" no tiene datos desde la fila ${START_ROW}.`);

  const destVendorVals = shDest.getRange(START_ROW, 1, destLastRow - START_ROW + 1, 1).getValues();
  const rowsByVendor   = new Map();

  for (let i = 0; i < destVendorVals.length; i++) {
    const vendor = (destVendorVals[i][0] ?? '').toString().trim();
    if (!vendor) continue;
    const absRow = START_ROW + i;
    if (!rowsByVendor.has(vendor)) rowsByVendor.set(vendor, []);
    rowsByVendor.get(vendor).push(absRow);
  }

  const usedCount = new Map();
  const now       = new Date();
  let written     = 0;

  for (const r of curRows) {
    const list    = rowsByVendor.get(r.vendor) || [];
    const used    = usedCount.get(r.vendor) || 0;
    const destRow = list[used];
    if (!destRow) continue;

    usedCount.set(r.vendor, used + 1);

    shDest.getRange(destRow, colOwner).setValue(r.owner);
    shDest.getRange(destRow, colReviewed).setValue(r.reviewed ? 'Yes' : 'No');
    shDest.getRange(destRow, colNotes).setValue(r.notes);
    shDest.getRange(destRow, colSaved).setValue(now);

    written++;
  }

  if (written === 0) throw new Error('No pude matchear ningún Vendor de Current contra la tab semanal (col A).');

  shDest.getRange(START_ROW, colSaved, destLastRow - START_ROW + 1, 1).setNumberFormat('yyyy-mm-dd hh:mm');
  shDest.autoResizeColumns(Math.min(colOwner, colReviewed, colNotes, colSaved), 4);
}
