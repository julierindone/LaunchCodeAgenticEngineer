#!/bin/bash
set -eu

AUTH_DIR=/claude-auth
GMAIL_AUTH_DIR="$AUTH_DIR/gmail-mcp"
mkdir -p "$AUTH_DIR" "$GMAIL_AUTH_DIR" /root/.claude /root/.gmail-mcp

# A persisted credential means this is NOT the first run: restore it and mark
# onboarding complete so Claude skips the first-run flow (theme, login, trust).
# On the first run there is no credential, so onboarding runs once and the
# background saver below persists the resulting credential.
if [ -f "$AUTH_DIR/.credentials.json" ]; then
  cp "$AUTH_DIR/.credentials.json" /root/.claude/.credentials.json
  chmod 600 /root/.claude/.credentials.json
  echo '{ "hasCompletedOnboarding": true, "projects": { "/workspace": { "hasTrustDialogAccepted": true } } }' > /root/.claude.json
fi

# Likewise restore the Gmail OAuth client keys and token, if this isn't the
# first run, so the Gmail MCP server doesn't need the browser auth flow again.
for f in gcp-oauth.keys.json credentials.json; do
  if [ -f "$GMAIL_AUTH_DIR/$f" ]; then
    cp "$GMAIL_AUTH_DIR/$f" "/root/.gmail-mcp/$f"
    chmod 600 "/root/.gmail-mcp/$f"
  fi
done

# Register this image's MCP servers (merged into /root/.claude.json).
claude mcp add slack \
  node /usr/local/lib/node_modules/@modelcontextprotocol/server-slack/dist/index.js \
  -e SLACK_BOT_TOKEN="$SLACK_BOT_TOKEN" \
  -e SLACK_TEAM_ID="$SLACK_TEAM_ID"

claude mcp add gmail \
  node /usr/local/lib/node_modules/@gongrzhe/server-gmail-autoauth-mcp/dist/index.js

# Module 3 course tools server (lives in the mounted workspace, not the image).
claude mcp add coursetools \
  python /workspace/mcp/coursetools_server.py

# Save the credential whenever it changes, so login survives any exit. Save
# when the persisted copy is missing (first login) or differs from the live one.
# Compare contents, not mtimes: WSL2 clock jumps after sleep can make a
# refreshed token look "older" and leave a stale copy on the volume.
# temp-file + chmod + atomic mv keeps the copy safe on the shared volume.
( set +e
  while true; do
    if [ -f /root/.claude/.credentials.json ] && \
      ! cmp -s /root/.claude/.credentials.json "$AUTH_DIR/.credentials.json"; then
      tmp=$(mktemp "$AUTH_DIR/.credentials.json.tmp.XXXXXX")
      cp /root/.claude/.credentials.json "$tmp"
      chmod 600 "$tmp"
      mv -f "$tmp" "$AUTH_DIR/.credentials.json"
    fi
    for f in gcp-oauth.keys.json credentials.json; do
      if [ -f "/root/.gmail-mcp/$f" ] && \
        ! cmp -s "/root/.gmail-mcp/$f" "$GMAIL_AUTH_DIR/$f"; then
        tmp=$(mktemp "$GMAIL_AUTH_DIR/$f.tmp.XXXXXX")
        cp "/root/.gmail-mcp/$f" "$tmp"
        chmod 600 "$tmp"
        mv -f "$tmp" "$GMAIL_AUTH_DIR/$f"
      fi
    done
    sleep 5
  done ) &

# exec so the command runs as PID 1 (correct signal handling / reaping).
exec "$@"
