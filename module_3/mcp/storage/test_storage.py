import asyncio
from fastmcp import Client


async def main():
    async with Client("http://localhost:8001/mcp") as c:
        tools = await c.list_tools()
        print("tools:", [t.name for t in tools])

        ok = await c.call_tool(
            "write_entry",
            {
                "project_id": "proj-csv",
                "entry_type": "decision",
                "title": "test",
                "content": "test content",
                "classification": "internal",
                "calling_role": "implementer",
            },
        )
        print("write:", ok)

        # NEW: read back the entry we just wrote
        r = await c.call_tool(
            "read_entry", {"project_id": "proj-csv", "entry_id": ok.data["entry_id"]}
        )
        print("read:", r.data)

        try:
            await c.call_tool(
                "write_entry",
                {
                    "project_id": "proj-csv",
                    "entry_type": "decision",
                    "title": "bad",
                    "content": "x",
                    "classification": "secret",
                    "calling_role": "implementer",
                },
            )
            print("secret write: UNEXPECTEDLY SUCCEEDED")
        except Exception as e:
            print("secret write rejected:", e)


asyncio.run(main())
