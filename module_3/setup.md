# Setup

## Commands/paths
- Docker build command: `docker build -t agentic_engineer_3 .`
- Build context: `cd /mnt/c/programming/automation/agentic_engineer/LaunchCodeAgenticEngineer/module_3` (project root, same folder as the Dockerfile), passed as `.` in `docker build -t agentic_engineer_3 .`
- Files copied from the context:
  - `requirements.txt`
  - `.claude/` (skills)
  - `.claude/agents/`
  - `settings.json`
  - `statusline.sh`
  - `.memory/reference/`
  - `docker-entrypoint.sh`
- Excluded via .dockerignore: `.env`, `node_modules`
  - 
- Docker run command:
  ```bash
  docker run -it --rm \
   --network agent-internal \
   -v $(pwd):/workspace:rw \
   -v $(pwd)/.memory:/memory:rw \
   -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY \
   -e SLACK_BOT_TOKEN=dummy \
   -e SLACK_TEAM_ID=dummy \
   agentic_engineer_3 bash
  ```
- Mounted path: `/mnt/c/programming/automation/agentic_engineer/LaunchCodeAgenticEngineer/module_3`
- Mount flags:
  - `-v $(pwd):/workspace:rw`: mounts the repo into the container at `/workspace`, read/write.
  - `-v $(pwd)/.memory:/memory:rw`: mounts the persistent memory directory at `/memory`, where the storage server's audit log and the retrieval server's reference corpus live, so they survive the container exiting.
  - `-e OPENROUTER_API_KEY=$OPENROUTER_API_KEY`: passes the API key in for the harness's own use. The container still can't reach the internet on its own.
  - `-e SLACK_BOT_TOKEN=dummy -e SLACK_TEAM_ID=dummy`: placeholder values. Without them the container fails at startup with a Slack error.

## Network mode:
The container runs on `agent-internal`, a user-defined Docker bridge network created with `--internal`. This replaces `--network none`: loopback and container-to-container traffic work, so the agent can reach MCP servers on `localhost`, but there's no route to the outside world.

### Step 1: Confirm the current configuration blocks localhost
Start a throwaway container with no network:
```bash
docker run -it --rm --network none \
-e SLACK_BOT_TOKEN=dummy -e SLACK_TEAM_ID=dummy -e OPENROUTER_API_KEY=dummy \
agentic_engineer_3 bash
```
Note: the lesson's `docker run -it --rm --network none agentic_engineer_3 bash` gave a Slack error, so I passed in dummy env vars.

Inside the container:
```bash
python3 -m http.server 8000 &
curl http://localhost:8000
```
Expected: `curl` fails ("Connection refused" / "Couldn't connect to server").
```

```
Exit the container (`exit`) to discard it.

### Step 2: Create the internal bridge network
On the host (one-time; the network persists until removed):
`docker network create --internal agent-internal`

Confirm it exists:
`docker network ls`
Expected: `agent-internal` listed with driver `bridge`.
```
NETWORK ID     NAME                             DRIVER    SCOPE
d25e0acb90bd   agent-internal                   bridge    local
b188de071f2b   bridge                           bridge    local
40b24a464709   host                             host      local
64a542f50844   mochoa_pgadmin4-docker-ext-etc   bridge    local
```

### Step 3: Start the container on the new network
Use the Docker run command from Commands/paths above (`--network agent-internal`).

### Step 4: Loopback check (localhost works)
Inside the container:
```bash
python3 -m http.server 8000 &
sleep 2
curl http://127.0.0.1:8000
```
Note: the lesson uses `curl http://localhost:8000` with no pause. I had to add `sleep 2` so the server finishes starting, and use `127.0.0.1` instead of `localhost`.

Expected: `curl` succeeds and prints an HTML directory listing.
```

```
Stop the test server: `kill %1`

### Step 5: Network egress check (external access still blocked)
Inside the container:
`curl https://example.com`

Expected: fails with "Could not resolve host" or a connection timeout.
```

```

If `localhost` still fails, check that the container was started with `--network agent-internal`.
If `example.com` succeeds, the network wasn't created with `--internal`. Remove it with `docker network rm agent-internal` and recreate it with the flag.

### Step 6: Record the change and commit
`git commit -am "infra: update container network to agent-internal bridge — allows localhost MCP communication"`


#### Build-time:
- Base: `python:3.12-slim`
- System packages via apt-get: curl, git, bash, ca-certificates, nano, procps, nodejs, npm, gettext-base, build-essential, python3-dev, sqlite3, jq, unzip, less, tree, iproute2, net-tools, lsof, dnsutils, make
- Python packages from `requirements.txt` (import-checked at build: fastmcp, mcp, aiosqlite, chromadb, sentence_transformers, sklearn, pydantic, httpx, rank_bm25, sqlite_vec)
- Global npm packages: `@anthropic-ai/claude-code`, `opencode-ai`, `@modelcontextprotocol/server-slack`, `@gongrzhe/server-gmail-autoauth-mcp`
- ngrok
- Claude Code config files (skills, agents, `settings.json`, `statusline.sh`) and the entrypoint script
