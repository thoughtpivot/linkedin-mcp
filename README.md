# ThoughtPivot LinkedIn MCP

<p align="left">
  <a href="https://github.com/thoughtpivot/linkedin-mcp/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/badge/License-Apache%202.0-%233fb950?labelColor=32383f" alt="License"></a>
</p>

An MCP server that connects an AI assistant to LinkedIn through your own logged-in browser session. Maintained by [ThoughtPivot](https://github.com/thoughtpivot). This is a public fork of [Daniel Sticker's linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server), with the engagement tools react, comment, and repost.

Fork the repository and run one server. Cursor, Claude Code, and VS Code in this repo already point at it. Any other assistant that can reach that HTTP address can use the same server.

> This is an independent open-source project, not affiliated with, authorized by, endorsed by, or sponsored by LinkedIn or Microsoft. LinkedIn is a trademark of LinkedIn Corporation and is used here only to identify the service this software interacts with.

## On your machine

**Prerequisites:** [Git](https://git-scm.com/downloads) and [uv](https://docs.astral.sh/uv/getting-started/installation/). Python 3.12.4 or newer; `uv` installs one if needed.

Fork [thoughtpivot/linkedin-mcp](https://github.com/thoughtpivot/linkedin-mcp), then clone your fork:

```bash
git clone https://github.com/YOUR_USER/linkedin-mcp
cd linkedin-mcp

uv sync
uv run patchright install chromium
uv run -m linkedin_mcp_server --login
```

`--login` opens a browser. Sign in once. The session is saved under `~/.linkedin-mcp/profile/`. On a later start the server reuses that session, and on the first tool call it can also import one from a local Chromium browser (Chrome, Brave, Edge, Arc, and the others named by `--import-from-browser`).

Leave the server running:

```bash
uv run -m linkedin_mcp_server --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp
```

It listens at `http://127.0.0.1:8000/mcp`. Open this repo in Cursor, Claude Code, or VS Code. The configs below are already in the tree, so the client connects when the server is up.

| Client | File |
| --- | --- |
| Cursor | [`.cursor/mcp.json`](.cursor/mcp.json) |
| Claude Code | [`.mcp.json`](.mcp.json) |
| VS Code | [`.vscode/mcp.json`](.vscode/mcp.json) |

After you pull new code, restart this process. A running server keeps the code it started with.

## In Docker

**Prerequisite:** [Docker](https://www.docker.com/get-started/) installed and running.

Sign in once. The container opens a LinkedIn login page that you drive from your own browser.

```bash
mkdir -p ~/.linkedin-mcp
docker build -t linkedin-mcp .
docker run -it --rm \
  -v ~/.linkedin-mcp:/home/pwuser/.linkedin-mcp \
  -p 127.0.0.1:6080:6080 \
  linkedin-mcp \
  --login --login-viewer
```

Open the full URL the command prints (it carries the access token) and sign in. Let the command exit on its own so the session is stored. It gives up after 30 minutes.

Keep `~/.linkedin-mcp` mounted at `/home/pwuser/.linkedin-mcp` on every later run. If an older rootful Docker run created that directory as root, fix it with `sudo chown -R "$(id -u):$(id -g)" ~/.linkedin-mcp`.

Then start the server:

```bash
docker compose up --build
```

That builds this repo and serves `http://127.0.0.1:8080/mcp`. Point a client at that URL. The files in the repo use port `8000`, which is the `uv` server; change the port to `8080` when Docker is what is running.

The same server, written as `docker run`:

```bash
docker run -it --rm \
  -v ~/.linkedin-mcp:/home/pwuser/.linkedin-mcp \
  -p 127.0.0.1:8080:8080 \
  linkedin-mcp \
  --transport streamable-http --host 0.0.0.0 --port 8080 --path /mcp
```

Both halves of that are needed. `--host 0.0.0.0` makes the server reachable inside the container; a process bound to `127.0.0.1` in there cannot be reached through a published port. The `127.0.0.1:` in front of `-p` limits `127.0.0.1:8080:8080` to this machine. Drop that prefix and Docker publishes an endpoint with no authentication on every interface of your network.

Do not run `--login` or `--logout` on the host while a container is using the same `~/.linkedin-mcp`. When tool calls start asking for authentication, repeat the login command.

## From another machine

The default bind is this machine only. The HTTP endpoint has no authentication, so anything that can open it can use your LinkedIn session.

To let another assistant on your network connect, start the `uv` server with `--host 0.0.0.0` and give that assistant `http://<this-machine>:8000/mcp`. For Docker, publishing without the `127.0.0.1:` prefix does the same thing, and it exposes the endpoint on every interface.

A tunnel (ngrok, Cloudflare Tunnel, Tailscale Funnel) does the same for a client that is not on the network, including a remote assistant such as Grok. The server answers requests for `localhost` or its bound address and refuses other Host headers with `421`. Set the tunnel hostname before you share the URL:

```bash
FASTMCP_HTTP_ALLOWED_HOSTS='["your-tunnel.example"]' \
  uv run -m linkedin_mcp_server --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp
```

Put authentication in front of a tunnel. The server does not provide it.

## Tools

An assistant calls these by name. Comment and repost publish only when `confirm_comment` or `confirm_repost` is true. A reaction this account already gave is refused, because clicking it again would remove it. `send_message` targets a profile and can open a new conversation.

- **People:** `get_person_profile`, `get_my_profile`, `search_people`, `get_sidebar_profiles`, `connect_with_person`
- **Messages:** `get_inbox`, `get_conversation`, `search_conversations`, `send_message`
- **Companies:** `get_company_profile`, `get_company_posts`, `search_companies`, `get_company_employees`
- **Jobs:** `search_jobs`, `get_saved_jobs`, `get_job_details`
- **Feed:** `get_feed`, `search_posts`, `react_to_post`, `comment_on_post`, `repost_post`
- **Session:** `close_session`

`acted` on a write means the server saw the UI change. `retry_safe` is the only field to key a retry on. While it is false, do not call again.

## Contributing

Pull requests are welcome. Fork the repository, branch from `main`, and open a pull request against [`thoughtpivot/linkedin-mcp`](https://github.com/thoughtpivot/linkedin-mcp). Read [CONTRIBUTING.md](CONTRIBUTING.md) for the checks a pull request has to pass. AI agents filing or commenting on issues follow the [issue-packet skill](.agents/skills/issue-packet/SKILL.md).

LinkedIn's User Agreement prohibits automated access, and accounts using automated tools can be restricted. Use it for your own account, sparingly.

## Acknowledgements

Copyright 2025-2026 Daniel Sticker; see [NOTICE](NOTICE). Built with [FastMCP](https://gofastmcp.com/) and [Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python).

## License

Apache 2.0. See [LICENSE](LICENSE).
