# LinkedIn MCP

<p align="left">
  <a href="https://github.com/thoughtpivot/linkedin-mcp/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/badge/License-Apache%202.0-%233fb950?labelColor=32383f" alt="License"></a>
</p>

An MCP server that connects AI assistants to LinkedIn through your own logged-in browser session. Maintained by [ThoughtPivot](https://github.com/thoughtpivot), the intelligence layer for the built world.

This is a public fork of [Daniel Sticker's linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server). It keeps upstream's read tools and adds the engagement tools the released upstream server does not ship: react, comment, and repost.

There is no published package, bundle, or image. The repository is the artifact: clone it or fork it, run it with `uv`, and send a pull request when you push it further.

> This is an independent open-source project, not affiliated with, authorized by, endorsed by, or sponsored by LinkedIn or Microsoft. LinkedIn is a trademark of LinkedIn Corporation and is used here only to identify the service this software interacts with.

## What it is for

- **Build in public.** Read the home feed and search posts, then react, comment, or repost one post at a time. Comment and repost publish only after an explicit confirmation flag. A reaction this account already gave is refused, because clicking it again would remove it.
- **Work the network.** Look up people and companies, pull sidebar profile recommendations, and send or accept a connection request.
- **Hold the conversation.** Read the inbox, search threads, and send a message.
- **Research the built world.** Read company pages, employees, and people for partnership and industry outreach.

## Tools

| Tool | Description |
|------|-------------|
| `get_person_profile` | Read profile sections such as experience, education, skills, projects and posts. |
| `get_my_profile` | Read your own profile using the same selectable sections. |
| `connect_with_person` | Send or accept a connection request, with an optional note. |
| `get_sidebar_profiles` | Find recommended profile links in a person's sidebar. |
| `get_inbox` | List recent messaging conversations from your LinkedIn inbox. |
| `get_conversation` | Read a conversation by username or thread ID. |
| `search_conversations` | Search messages by keyword across your conversations. |
| `send_message` | Send after confirmation. Targeting a profile may start a separate DM instead of replying in a thread. |
| `get_company_profile` | Read posts and jobs; about references can include a `company_urn` for the `currentCompany` search facet. |
| `get_company_posts` | Read recent posts published on a company's LinkedIn page. |
| `search_companies` | Find LinkedIn company profiles matching a keyword search. |
| `get_company_employees` | List company employees, optionally filtered by keyword. |
| `search_jobs` | Find LinkedIn job postings by keyword and location. |
| `get_saved_jobs` | List the job postings you have saved on LinkedIn. |
| `search_people` | Search by keyword, location, connection degree or company. |
| `get_job_details` | Read the details of a LinkedIn job posting by its job ID. |
| `get_feed` | Read recent home-feed posts, with links in `references`. |
| `search_posts` | Search posts by keyword with optional recency filters; `references` contains unordered candidate post links. |
| `react_to_post` | React to one post (like, celebrate, support, love, insightful, funny); refuses to click a reaction this account already gave, since that click would remove it |
| `comment_on_post` | Publish a comment on one post (`confirm_comment=true`; `false` is a dry run) |
| `repost_post` | Reshare one post, bare or with commentary (`confirm_repost=true`; `false` is a dry run) |
| `close_session` | Close the active browser session and release its resources. |

<details>
<summary><strong>Post engagement (write tools)</strong></summary>

These three tools are public, account-attributed writes on **one** post. Discover posts with `get_feed` or `search_posts`, then pass a `feed_post` permalink as `post` (`/feed/update/<urn>/` or `/posts/<slug>`).

**Confirmation**

- `react_to_post` has no confirmation flag. If this account has already reacted, it returns `already_reacted` without clicking — that click would remove the reaction. Change or remove a reaction in LinkedIn.
- `comment_on_post` publishes only when `confirm_comment=true`. `false` checks that the post loads and a comment box exists, and types nothing.
- `repost_post` publishes only when `confirm_repost=true`. `false` checks that a repost control exists. Optional `commentary` adds text above the reshare. Either form is confirmed by the source post's own count strings changing — not by finding the commentary text on that post, because the reshare publishes to the actor's feed.

**Return shape (not `{url, sections}`)**

`{url, status, message, acted, retry_safe}`; `react_to_post` also returns `reaction`.

- `acted` means the server observed the expected UI transition. It is not proof LinkedIn kept or showed the action.
- `retry_safe` is the only field to key a retry on. While it is `false`, do not call again: a reaction retry can remove the reaction, and a comment or repost retry can duplicate public content.

Comment and commentary text may include newlines. Other control characters are rejected before a browser opens. Finding posts is not permission to engage; authorize each post and action explicitly.

</details>

## Get it from GitHub

**Prerequisites:** [Git](https://git-scm.com/downloads) and [uv](https://docs.astral.sh/uv/getting-started/installation/). Python 3.12.4 or newer; `uv` installs one if needed.

### MCP clients

`uvx` clones this repository, builds it on first run, and caches the result. The command name stays `mcp-server-linkedin` because that is the Python package name inside the repository. Pin a branch, tag, or commit with `git+https://github.com/thoughtpivot/linkedin-mcp@<ref>`.

#### Cursor

Create [`~/.cursor/mcp.json`](https://cursor.com/docs/mcp) for every project, or `.cursor/mcp.json` in one project. Cursor Settings → Tools & MCP edits the same file.

```json
{
  "mcpServers": {
    "linkedin-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/thoughtpivot/linkedin-mcp",
        "mcp-server-linkedin"
      ],
      "env": { "UV_HTTP_TIMEOUT": "300" }
    }
  }
}
```

Toggle the server in Tools & MCP if it does not appear.

#### Claude Desktop

Claude Desktop uses that same JSON. On macOS it lives in `~/Library/Application Support/Claude/claude_desktop_config.json`. On Windows it lives in `%APPDATA%\Claude\claude_desktop_config.json`. Restart Claude Desktop after saving.

#### Codex

The Codex CLI and the IDE extension share [`~/.codex/config.toml`](https://developers.openai.com/codex/config-reference). A project file at `.codex/config.toml` applies to that project once the directory is trusted.

```toml
[mcp_servers.linkedin-mcp]
command = "uvx"
args = ["--from", "git+https://github.com/thoughtpivot/linkedin-mcp", "mcp-server-linkedin"]

[mcp_servers.linkedin-mcp.env]
UV_HTTP_TIMEOUT = "300"
```

Or from a terminal: `codex mcp add linkedin-mcp --env UV_HTTP_TIMEOUT=300 -- uvx --from git+https://github.com/thoughtpivot/linkedin-mcp mcp-server-linkedin`.

#### VS Code

VS Code reads [`.vscode/mcp.json`](https://code.visualstudio.com/docs/agent-customization/mcp-servers) in a workspace, or the user file opened by **MCP: Open User Configuration**. The key is `servers`.

```json
{
  "servers": {
    "linkedin-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/thoughtpivot/linkedin-mcp",
        "mcp-server-linkedin"
      ],
      "env": { "UV_HTTP_TIMEOUT": "300" }
    }
  }
}
```

### Clone or fork

This is the path for anyone who wants to change the server. Fork on GitHub first if you plan to send a pull request, then clone your fork.

```bash
git clone https://github.com/thoughtpivot/linkedin-mcp
cd linkedin-mcp

uv sync                                # runtime dependencies
uv sync --group dev                    # tests, lint, type check
uv run pre-commit install              # hooks that keep the repo consistent
uv run patchright install chromium     # the browser the server drives

uv run -m linkedin_mcp_server --login  # sign in once; the session is saved
uv run -m linkedin_mcp_server          # start the server on stdio
```

To run the clone instead of `uvx`, use the same client file and swap the launcher. Cursor and Claude Desktop:

```json
{
  "mcpServers": {
    "linkedin-mcp": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/linkedin-mcp", "run", "-m", "linkedin_mcp_server"]
    }
  }
}
```

Codex uses `command = "uv"` and `args = ["--directory", "/absolute/path/to/linkedin-mcp", "run", "-m", "linkedin_mcp_server"]`. VS Code keeps `"type": "stdio"` and uses that same `uv` command under `servers`. Spell the path out in full. A client does not expand `~`.

### Signing in

On the first tool call that needs authentication, the server reuses a LinkedIn session from a signed-in local browser (Chrome, Chromium, Brave, Edge, Arc, Vivaldi, Helium, Yandex, Whale, Cốc Cốc, Opera, Opera GX) if it finds one, and otherwise opens a LinkedIn login window. On macOS the keychain may prompt once. Early tool calls may return an authentication-in-progress error until that finishes; retry once it does.

To create the session explicitly, run `--login`. To reuse a specific browser's session, run `--import-from-browser brave` (or another browser name). The saved session lives at `~/.linkedin-mcp/profile/`; managed browser downloads are cached at `~/.linkedin-mcp/patchright-browsers/`. `--status` checks the stored session and `--logout` clears it.

### HTTP transport

The default transport is stdio. For a web-based MCP client:

```bash
uv run -m linkedin_mcp_server --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp
```

Tool calls are serialized to protect the one LinkedIn browser session, both within a server process and across several. If you run more than one MCP client, each starts its own server process; only one uses the browser at a time and the others wait briefly, then take over. A client that waits too long gets a "browser is busy" message and can retry.

## Build the Docker image yourself

The repository carries a `Dockerfile`. Nothing is published; build it from your clone.

**Prerequisites:** [Docker](https://www.docker.com/get-started/) installed and running.

```bash
cd linkedin-mcp
docker build -t linkedin-mcp .
```

### Authentication

Log in once. The container opens a LinkedIn login browser that you drive from your own browser tab.

```bash
# Create the directory first so the container can save your session into it
mkdir -p ~/.linkedin-mcp
docker run -it --rm \
  -v ~/.linkedin-mcp:/home/pwuser/.linkedin-mcp \
  -p 127.0.0.1:6080:6080 \
  linkedin-mcp \
  --login --login-viewer
```

Open the full URL the command prints (it carries the access token) and sign in. The viewer closes itself afterwards; let the command exit on its own so the session is stored completely. It gives up after 30 minutes.

Keep the same host directory mounted at `/home/pwuser/.linkedin-mcp` on every later `docker run`, otherwise the server cannot find the session. If an older rootful Docker run created that directory as root, fix it with `sudo chown -R "$(id -u):$(id -g)" ~/.linkedin-mcp`.

### MCP client configuration

Spell the host path out in full. A client runs `docker` directly rather than through a shell, so a leading `~` reaches Docker unexpanded and it refuses the mount. On Windows use a forward-slash path such as `C:/Users/Alice/.linkedin-mcp`; a backslash path fails JSON parsing.

```json
{
  "mcpServers": {
    "linkedin-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "/absolute/path/to/.linkedin-mcp:/home/pwuser/.linkedin-mcp",
        "linkedin-mcp"
      ]
    }
  }
}
```

### HTTP transport in Docker

```bash
docker run -it --rm \
  -v ~/.linkedin-mcp:/home/pwuser/.linkedin-mcp \
  -p 127.0.0.1:8080:8080 \
  linkedin-mcp \
  --transport streamable-http --host 0.0.0.0 --port 8080 --path /mcp
```

Both halves of that are needed. `--host 0.0.0.0` makes the server reachable *inside* the container; a process bound to `127.0.0.1` in there cannot be reached through a published port. The `127.0.0.1:` in front of `-p` limits it *outside*, to this machine. Drop that prefix and Docker publishes an endpoint with no authentication on every interface of your network.

The HTTP server answers requests addressed to `localhost` or its bound address and refuses others with `421`. To serve it under another name, set `FASTMCP_HTTP_ALLOWED_HOSTS='["mcp.example"]'`. The endpoint still has no authentication, so anything reachable beyond your own machine belongs behind something that provides it.

> [!NOTE]
> Plain `--login` has no visible window in Docker; add `--login-viewer` and publish `127.0.0.1:6080:6080` only for the one-shot login command. Sessions expire over time. When tool calls start asking for authentication, repeat the login command, or run `--login` from a clone on the host. Do not run `--login` or `--logout` on the host while a container is running against the same `~/.linkedin-mcp`.

## Configuration

<details>
<summary><b>CLI options</b></summary>

Most options have environment-variable equivalents; see [`.env.example`](.env.example).

**Session**

- `--login` - Open a browser to sign in and save the session
- `--import-from-browser [BROWSER]` - Reuse a session from a locally signed-in Chromium browser (`chrome`, `chromium`, `brave`, `edge`, `arc`, `vivaldi`, `helium`, `yandex`, `whale`, `coccoc`, `opera`, `opera_gx`, `auto`). Bare flag picks `auto`, the most recently used browser with a live LinkedIn session.
- `--auto-import` / `--no-auto-import` - Import a session from a signed-in local browser on the first tool call that needs one, before falling back to manual login (default: on). Skipped in Docker, behind a proxy, and on a non-loopback HTTP bind.
- `--status` - Check whether the stored session is valid, then exit
- `--logout` - Clear the stored session
- `--login-viewer` - Docker only: with `--login`, show the login browser at a token-protected URL on port 6080
- `--user-data-dir PATH` - Browser profile directory (default: `~/.linkedin-mcp/profile`). Rotating or clearing a session deletes this directory *and its parent*, which holds the stored cookies and derived profiles.
- `--claim-profile-root` - Take over a profile directory the server will not claim on its own, such as one whose parent already holds other files. Needed once per directory.

**Transport**

- `--transport {stdio,streamable-http}` - Force the transport mode (default: stdio)
- `--host HOST` / `--port PORT` / `--path PATH` - HTTP server address (defaults: 127.0.0.1, 8000, /mcp)

**Timeouts**

- `--timeout MS` - Timeout for a single page operation (default: 5000)
- `--tool-timeout SECONDS` - Timeout for a whole tool call (default: 180). Raise it for heavy scrapes, slow networks, or a cold-start browser.
- `--login-timeout SECONDS` - How long the login browser waits for you to finish signing in (default: 1800; 0 = no limit). `--login-viewer` ends the session after 30 minutes either way.
- `--login-inline-wait SECONDS` - How long a tool call waits for a login to finish before telling the model to retry (default: 25, max 45; 0 = return at once)

**Shared browser**

- `--browser-wait SECONDS` - How long to wait for another server process to hand over the shared browser (default: 25, max 45; 0 = report busy at once)
- `--browser-min-hold SECONDS` - Shortest time this process keeps the shared browser before handing it over (default: 20). Clamped to 3 seconds below `--browser-wait`.
- `--browser-idle-timeout SECONDS` - Close an idle browser and release the profile after this long without a tool call (default: 600; 0 = keep it open)

**Browser**

- `--no-headless` - Show the browser window (useful for debugging)
- `--slow-mo MS` - Delay between browser actions (default: 0)
- `--viewport WxH` - Viewport size (default: 1280x720). Windowless mode only; a headed launch uses the real window size.
- `--chrome-path PATH` - Path to a Chrome/Chromium executable
- `--installer-temp-dir PATH` - Parent directory for temporary files created during browser installation (default: system temporary directory)
- `--proxy-server URL` - Route browser traffic through a proxy, as `scheme://host:port`. Set it up **before** `--login`; see below.

**Other**

- `--log-level {DEBUG,INFO,WARNING,ERROR}` - Logging level (default: WARNING)
- `--help` - Show help

</details>

<details>
<summary><b>Using a proxy</b></summary>

LinkedIn scores the address a session signs in from. Your account's usual IP address is the safe one. Use a proxy in your country when the server cannot use that address: a VPS, another country, or a second account that must not share the first one's address. With a paid provider, use a sticky residential session that holds one address, never per-request rotation. A WireGuard full tunnel or Tailscale exit node on your home network works when the server should use your usual home address.

- Set the proxy up **before** `--login`. Moving an existing session to a new address triggers a LinkedIn checkpoint. That includes a session from `--import-from-browser`, which was created on your real address.
- `--proxy-server scheme://host:port` or `PROXY_SERVER`, with `http`, `https`, `socks4` or `socks5`. Only browser traffic is routed, not the MCP transport.
- Pass credentials through `PROXY_USERNAME` and `PROXY_PASSWORD`, or include them in `PROXY_SERVER` as `http://user:pass@host:port`. The combined form is not accepted by the `--proxy-server` CLI option.
- `PROXY_BYPASS=localhost,127.0.0.1,::1` reaches local targets directly. With a proxy set, Chromium routes `localhost` through it too.
- Chromium cannot authenticate to a SOCKS proxy, so credentials require an `http(s)` endpoint. If your provider only offers authenticated SOCKS5, run a local relay that holds the credentials and point the server at that.
- A wrong proxy password shows up as a timeout or a failed sign-in, because Chromium retries the authentication challenge until the page times out. If sessions stop working right after you add a proxy, check the credentials first.
- Auto-import is skipped while a proxy is configured, because the imported session would move from your real address to the proxy. Use `--login`.
- Inside a container `127.0.0.1` is the container itself, so a relay on the host is `host.docker.internal`; native Linux Docker also needs `--add-host=host.docker.internal:host-gateway`.

</details>

<details>
<summary><b>Troubleshooting</b></summary>

**Login**

- Keep only one active LinkedIn session at a time.
- LinkedIn may require a login confirmation in the LinkedIn mobile app, or show a captcha. `--login` opens a browser where you can complete either by hand.
- If Docker authentication goes stale after you re-login on the host, restart the container once so it picks up the new session.

**Timeouts**

- *Page operations failing* (elements not found, navigation hangs): raise the page-op timeout with `--timeout 10000` or `TIMEOUT=10000` (milliseconds, default 5000).
- *Whole tool calls timing out* (multi-section profiles, cold-start Chromium, slow containers): raise the per-tool timeout with `--tool-timeout 300` or `TOOL_TIMEOUT=300` (seconds, default 180).
- *First tool call with no session*: the server auto-imports a live session from a local browser if it can, otherwise opens a login window and waits up to `--login-inline-wait` seconds (default 25, max 45). If the wait elapses, the tool returns a pending signal and the model retries in about 30 seconds. Neither applies under Docker or on a non-loopback HTTP bind; create the session with `--login` first.

**Session and browser cache**

- Browser profile: `~/.linkedin-mcp/profile/`. Managed browser downloads: `~/.linkedin-mcp/patchright-browsers/`.
- *The browser cache keeps growing*: Patchright keeps an old Chromium revision for as long as any installed version still references it, and a `uv` archive or a second worktree is such a reference. The server logs a warning naming what it holds. Stop every server instance, delete `~/.linkedin-mcp/patchright-browsers/`, and let the next launch download the current browser.
- `--logout` clears the profile and starts fresh.

**Told to run `--login` on the host when you already did**

- If tool calls answer "No valid LinkedIn session is available in Docker" on a machine that is *not* a container, the runtime was misdetected. This has happened on Linux hosts running a Docker daemon for unrelated services. Set `LINKEDIN_MCP_CONTAINER=false` to override the detection; `true` forces the opposite.

**Custom Chrome path**

- If Chrome is installed in a non-standard location, use `--chrome-path /path/to/chrome` or `CHROME_PATH=/path/to/chrome`.
- On macOS and Linux the browser must be at least as new as the one that last opened your profile, and the server refuses the launch otherwise. An older browser can silently drop stores a newer one wrote, the saved session among them, and the failure then looks exactly like an expired login. The message names both versions. Either run the newer browser again, or run `--login`, which moves the stored session aside and signs in fresh with the browser you have. Only Chrome, Chromium and Chrome for Testing are compared this way; forks number themselves differently, so pointing `CHROME_PATH` at one turns the check off.
- The check is off on Windows, where a browser cannot be asked its version without starting one.

**Python and Patchright**

- Check the Python version: `python --version` (3.12.4 or newer).
- Reinstall the browser: `uv run patchright install chromium`.
- Reinstall dependencies: `uv sync --reinstall`.
- *Windows, `DLL load failed while importing _greenlet`*: move to greenlet 3.5.5 or newer with `uv lock --upgrade-package greenlet`, or install the [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist). See [greenlet#525](https://github.com/python-greenlet/greenlet/issues/525).

**Scraping**

- Use `--no-headless` to watch the browser, and `--log-level DEBUG` for detailed logging.

</details>

## Contributing

Pull requests are welcome, and the ones we want most are the ones that extend what this server can do on LinkedIn. Fork the repository, branch from `main`, and open a pull request against [`thoughtpivot/linkedin-mcp`](https://github.com/thoughtpivot/linkedin-mcp). The repository is the release: there is no package to publish and no version to wait for, so a merged pull request is live for everyone on the next `git pull` or `uvx` refresh.

Before you start, read [CONTRIBUTING.md](CONTRIBUTING.md) for the scraping architecture and the checks a pull request has to pass (`uv run ruff check .`, `uv run ty check`, `uv run pytest`). Search the [issues](https://github.com/thoughtpivot/linkedin-mcp/issues) before filing a new one. AI agents filing or commenting on issues follow the [issue-packet skill](.agents/skills/issue-packet/SKILL.md).

> [!IMPORTANT]
> **FAQ**
>
> **Is this safe to use? Will I get banned?**
> This tool controls a real browser session; it doesn't exploit undocumented APIs or bypass authentication. LinkedIn's User Agreement prohibits automated access, and accounts using automated tools can be restricted or banned. Use at your own risk; there is no guarantee of account safety.
>
> **What if my agents execute too many actions?**
> Tool calls run sequentially through a queue. You are responsible for the volume of automation you run; use it sparingly and prompt your agents responsibly.

## Acknowledgements

This repository is ThoughtPivot's fork of [Daniel Sticker's linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server). Copyright 2025-2026 Daniel Sticker; see [NOTICE](NOTICE).

Built with [FastMCP](https://gofastmcp.com/) and [Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python).

Use in accordance with [LinkedIn's User Agreement](https://www.linkedin.com/legal/user-agreement). Automated access may violate LinkedIn's terms and can lead to account restrictions. This tool is for personal use only and comes with no warranty of any kind.

## License

Apache 2.0. See [LICENSE](LICENSE) for terms and [NOTICE](NOTICE) for attribution.
