import assert from "node:assert/strict";
import { test } from "node:test";
import { tasksToCsv } from "../src/csv.js";

test("header row has the correct columns in order", () => {
  const csv = tasksToCsv([]);
  const [headerLine] = csv.split("\r\n");

  assert.equal(headerLine, "id,title,status,dueDate,completed");
});

test("empty task list still produces a file with just the header row", () => {
  const csv = tasksToCsv([]);

  assert.equal(csv, "id,title,status,dueDate,completed\r\n");
});

test("a normal task row is mapped to the right columns", () => {
  const csv = tasksToCsv([
    {
      id: 1,
      title: "Write report",
      status: "todo",
      dueDate: "2026-06-01",
      completed: false
    }
  ]);

  assert.equal(
    csv,
    "id,title,status,dueDate,completed\r\n" +
      "1,Write report,todo,2026-06-01,false\r\n"
  );
});

test("multiple tasks produce one row per task in order", () => {
  const csv = tasksToCsv([
    { id: 1, title: "A", status: "todo", dueDate: "2026-01-01", completed: false },
    { id: 2, title: "B", status: "done", dueDate: "2026-01-02", completed: true }
  ]);
  assert.equal(
    csv,
    "id,title,status,dueDate,completed\r\n" +
      "1,A,todo,2026-01-01,false\r\n" +
      "2,B,done,2026-01-02,true\r\n"
  );
});

test("a field containing a comma is wrapped in double quotes", () => {
  const csv = tasksToCsv([
    {
      id: 2,
      title: "Buy milk, eggs, and bread",
      status: "todo",
      dueDate: "2026-06-02",
      completed: false
    }
  ]);

  assert.equal(
    csv,
    "id,title,status,dueDate,completed\r\n" +
      '2,"Buy milk, eggs, and bread",todo,2026-06-02,false\r\n'
  );
});

test("a field containing a double quote is wrapped and the quote is doubled", () => {
  const csv = tasksToCsv([
    {
      id: 3,
      title: 'Say "hello" to the client',
      status: "todo",
      dueDate: "2026-06-03",
      completed: false
    }
  ]);

  assert.equal(
    csv,
    "id,title,status,dueDate,completed\r\n" +
      '3,"Say ""hello"" to the client",todo,2026-06-03,false\r\n'
  );
});

test("a field containing a line break is wrapped in double quotes", () => {
  const csv = tasksToCsv([
    {
      id: 4,
      title: "Line one\nLine two",
      status: "todo",
      dueDate: "2026-06-04",
      completed: false
    }
  ]);

  assert.equal(
    csv,
    "id,title,status,dueDate,completed\r\n" +
      '4,"Line one\nLine two",todo,2026-06-04,false\r\n'
  );
});

test("a field containing a CRLF line break is wrapped in double quotes", () => {
  const csv = tasksToCsv([
    {
      id: 5,
      title: "Line one\r\nLine two",
      status: "todo",
      dueDate: "2026-06-05",
      completed: false
    }
  ]);

  assert.equal(
    csv,
    "id,title,status,dueDate,completed\r\n" +
      '5,"Line one\r\nLine two",todo,2026-06-05,false\r\n'
  );
});

test("a field needing escaping for both a comma and a double quote at once is handled correctly", () => {
  const csv = tasksToCsv([
    {
      id: 6,
      title: 'Buy "milk", eggs, and bread',
      status: "todo",
      dueDate: "2026-06-06",
      completed: false
    }
  ]);

  assert.equal(
    csv,
    "id,title,status,dueDate,completed\r\n" +
      '6,"Buy ""milk"", eggs, and bread",todo,2026-06-06,false\r\n'
  );
});

test("a missing/undefined field is rendered as an empty string, not the text \"undefined\"", () => {
  const csv = tasksToCsv([
    { id: 7, title: "No due date", status: "todo", completed: false }
  ]);

  assert.equal(
    csv,
    "id,title,status,dueDate,completed\r\n" +
      "7,No due date,todo,,false\r\n"
  );
});

test("non-array input is treated as an empty task list instead of throwing", () => {
  assert.equal(tasksToCsv(), "id,title,status,dueDate,completed\r\n");
  assert.equal(tasksToCsv(null), "id,title,status,dueDate,completed\r\n");
  assert.equal(
    tasksToCsv("not an array"),
    "id,title,status,dueDate,completed\r\n"
  );
});
