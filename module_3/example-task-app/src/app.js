import { getTasks } from "./tasks.js";
import { tasksToCsv } from "./csv.js";

export function renderTaskList(root = document.getElementById("task-list")) {
  if (!root) {
    return;
  }

  root.innerHTML = "";

  for (const task of getTasks()) {
    const item = document.createElement("li");
    item.dataset.taskId = String(task.id);
    item.textContent = `${task.title} - ${task.status}`;
    root.appendChild(item);
  }
}

// Exports are built from getTasks() rather than the rendered DOM list.
// These are equivalent today because there's no filtering/search UI that
// would make the visible list a subset of all tasks; revisit this if such a
// UI is ever added.
export function handleExportCsvClick() {
  const csv = tasksToCsv(getTasks());
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "tasks.csv";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  // Defer the revocation to the next tick. Revoking the object URL
  // synchronously right after click() risks invalidating it before some
  // browsers have actually started the download.
  setTimeout(() => URL.revokeObjectURL(url), 0);
}

export function attachExportCsvHandler(
  button = document.getElementById("export-csv-btn")
) {
  if (!button) {
    return;
  }

  button.addEventListener("click", handleExportCsvClick);
}

renderTaskList();
attachExportCsvHandler();
