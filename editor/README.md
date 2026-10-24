# Private prose editor

The book pages include an **Edit** link for the content pages listed in `etb-live/manifest.json`. The editor is served at `/editor/`; Cloudflare Access must protect `learning.benjaminpacini.com/editor/*`. The Worker also validates the Access JWT and allows only the three email addresses in `feedback/worker.js`.

For each Worker, set these top-level Worker variables and secrets in Cloudflare:

- Text variable `ACCESS_TEAM_DOMAIN`: the full Access team origin, such as `https://your-team.cloudflareaccess.com`.
- Text variable `ACCESS_AUD`: the Application Audience tag for that book's `/editor/*` Access application.
- Secret `EDITOR_GITHUB_TOKEN`: a fine-grained token with Contents: Read and write for this textbook repository only.

The two repositories use the same `feedback/worker.js` and `editor/index.html`, but each has its own Access application audience and its own Worker secret. The token is never stored in Git or sent to the browser.

The editor writes to `main` when Benjamin selects **Save and publish**. EDCOR's Worker updates both `etb-live/<page>.html` and its generated `site/<page>.html` in one Git commit. Cloudflare deploys the commit through the repository's existing deployment connection.
