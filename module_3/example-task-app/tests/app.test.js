import assert from "node:assert/strict";
import { test, before, after } from "node:test";
import { JSDOM } from "jsdom";

// app.js has top-level side effects (it calls renderTaskList() and
// attachExportCsvHandler() as soon as it's imported), so we need a DOM in
// place (via jsdom) *before* importing it. We stub URL.createObjectURL /
// URL.revokeObjectURL since jsdom doesn't implement the Blob-URL APIs.

let dom;
let attachExportCsvHandler;
const createObjectURLCalls = [];
const revokeObjectURLCalls = [];

before(async () => {
  dom = new JSDOM(
    `<!doctype html>
    <html>
      <body>
        <ul id="task-list"></ul>
        <button id="export-csv-btn">Export CSV</button>
      </body>
    </html>`,
    { url: "http://localhost/" }
  );

  globalThis.window = dom.window;
  globalThis.document = dom.window.document;

  globalThis.URL.createObjectURL = (blob) => {
    createObjectURLCalls.push(blob);
    return "blob:mock-url";
  };
  globalThis.URL.revokeObjectURL = (url) => {
    revokeObjectURLCalls.push(url);
  };

  ({ attachExportCsvHandler } = await import("../src/app.js"));
});

after(() => {
  delete globalThis.window;
  delete globalThis.document;
});

test("clicking the export button creates a tasks.csv download anchor and clicks it", () => {
  createObjectURLCalls.length = 0;
  revokeObjectURLCalls.length = 0;

  // Replace the button with a clean clone so this test only exercises the
  // listener we attach explicitly below, not the one app.js's own top-level
  // attachExportCsvHandler() call already added on import.
  const existingButton = document.getElementById("export-csv-btn");
  const button = existingButton.cloneNode(true);
  existingButton.replaceWith(button);

  attachExportCsvHandler(button);

  let anchor = null;
  const originalCreateElement = document.createElement.bind(document);
  document.createElement = (tagName) => {
    const element = originalCreateElement(tagName);
    if (tagName === "a") {
      anchor = element;
      element.click = () => {
        element.clicked = true;
      };
    }
    return element;
  };

  button.dispatchEvent(new dom.window.Event("click"));

  document.createElement = originalCreateElement;

  assert.ok(anchor, "an anchor element should have been created");
  assert.equal(anchor.download, "tasks.csv");
  assert.equal(anchor.clicked, true, "the anchor's click() should have been called");

  assert.equal(createObjectURLCalls.length, 1);
  assert.equal(createObjectURLCalls[0].type, "text/csv");
});
