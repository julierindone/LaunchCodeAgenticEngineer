const CSV_HEADERS = ["id", "title", "status", "dueDate", "completed"];

// RFC4180-style escaping: wrap a field in double quotes if it contains a
// comma, a double quote, or a line break; double any internal double quotes.
// Null/undefined values are treated as an empty field rather than the
// literal text "undefined"/"null".
function escapeField(value) {
  const str = String(value ?? "");
  if (/[",\r\n]/.test(str)) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

function rowToLine(values) {
  return values.map(escapeField).join(",");
}

/**
 * Build a CSV string for the given tasks, per the Export CSV PRD:
 * - headers: id, title, status, dueDate, completed (in that order)
 * - one row per task
 * - RFC4180-style escaping for commas, double quotes, and line breaks
 * - CRLF ("\r\n") row separators, including after the header row and after
 *   the last row (so an empty task list still yields a header row plus a
 *   trailing CRLF)
 *
 * `tasks` defaults to an empty list, and any non-array input (null,
 * undefined, or otherwise) is treated as an empty list as well, so callers
 * get a predictable header-only CSV instead of a raw TypeError.
 *
 * Pure function: no DOM or browser APIs, safe to run under Node's test
 * runner.
 */
export function tasksToCsv(tasks = []) {
  const taskList = Array.isArray(tasks) ? tasks : [];
  const lines = [rowToLine(CSV_HEADERS)];

  for (const task of taskList) {
    lines.push(rowToLine(CSV_HEADERS.map((key) => task[key])));
  }

  return lines.join("\r\n") + "\r\n";
}
