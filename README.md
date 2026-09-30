# Private Network Service Platform — Phase 1 Starter

This repo is shared by the whole team. One person pushes it to GitHub once;
everyone else clones it onto their own Mac and follows the section below
for their assigned role.

## Repo layout

```
backend/      Flask REST API (used by Mac 3 and Mac 4)
nginx/        nginx config template (used by Mac 2)
dnsmasq/      dnsmasq config template (used by Mac 1)
team/         team.env.example -> copy to team.env with today's real IPs
scripts/      get-my-ip.sh, run-backend.sh, smoke-test.sh
evidence/     put your screenshots / Wireshark captures here, organised by task
docs/         topology diagram, architecture notes
```

## 0. One-time: push this repo to GitHub

Do this once, as a team:

```bash
cd cn-project-starter
git init
git add .
git commit -m "Initial Phase 1 scaffold"
gh repo create teamX-cn-project --private --source=. --push
# or, without the gh CLI:
#   create an empty repo on github.com first, then:
git remote add origin https://github.com/<your-org-or-username>/teamX-cn-project.git
git branch -M main
git push -u origin main
```

Add the other 3 members as collaborators (GitHub repo → Settings → Collaborators),
or just have everyone fork/clone if it's public.

## 1. Every Mac: clone the repo

```bash
git clone https://github.com/<your-org-or-username>/teamX-cn-project.git
cd teamX-cn-project
```

## 2. Every Mac, every session: record today's IP

Wi-Fi IPs on a shared/home network usually change each time you reconnect.
At the start of every work session, on EVERY Mac:

```bash
chmod +x scripts/*.sh
./scripts/get-my-ip.sh
```

Copy the IP into a shared note (WhatsApp/Notion/whatever your team uses),
then have ONE person update `team/team.env` (copy from `team.env.example`)
with everyone's current IP and share it back to the group. `team.env` is
git-ignored on purpose — it changes every session and shouldn't clutter
your commit history.

## 3. Mac 1 — Private DNS Server

```bash
brew install dnsmasq
```

Open `dnsmasq/dnsmasq.conf.template`, replace `<MAC1_IP>`, `<MAC2_IP>` and
`teamX` with the real values from `team/team.env`, then copy the result in:

```bash
cp dnsmasq/dnsmasq.conf.template /opt/homebrew/etc/dnsmasq.conf
# (open it and fill in the placeholders — don't just copy the template as-is)
nano /opt/homebrew/etc/dnsmasq.conf
sudo brew services start dnsmasq
```

Verify locally:

```bash
dig @127.0.0.1 app.teamX.test
```

If the DNS Mac should also resolve public internet domains, the supplied
template forwards those queries to `8.8.8.8`. After changing the config, run
`sudo brew services restart dnsmasq` on the DNS Mac. Configure that Mac to use
`127.0.0.1` for DNS; configure other Macs on the LAN to use the DNS Mac's
`MAC1_IP` (not `127.0.0.1`). Avoid adding a public DNS server as a secondary
resolver on clients that need the private `teamX.test` records.

## 4. Mac 3 (Backend A) and Mac 4 (Backend B)

Both machines run the exact same code — only the role differs:

```bash
# On Mac 3:
./scripts/run-backend.sh A

# On Mac 4:
./scripts/run-backend.sh B
```

Leave that terminal window running. In a second terminal on the SAME Mac,
sanity check it locally, then from ANOTHER Mac on the LAN to confirm it's
reachable over the network (not just to itself):

```bash
curl http://localhost:3001/api/status     # on Mac 3 itself
curl http://<MAC3_IP>:3001/api/status     # from Mac 2 or a client Mac
```

## 5. Mac 2 — Edge / Reverse Proxy / Load Balancer

```bash
brew install nginx
```

Fill in `nginx/nginx.conf.template` with real IPs (from `team/team.env`)
and your team's domain, then install it:

```bash
mkdir -p /opt/homebrew/etc/nginx/servers
cp nginx/nginx.conf.template /opt/homebrew/etc/nginx/servers/cn-project.conf
nano /opt/homebrew/etc/nginx/servers/cn-project.conf   # fill in placeholders
sudo brew services restart nginx
```

If port 80 refuses connections, run `sudo lsof -nP -iTCP:80 -sTCP:LISTEN` on
the nginx Mac. If nothing is listening, restart nginx there with
`sudo brew services restart nginx` and check again.

Set the client Mac's DNS resolver to Mac 1's IP (System Settings → Network →
Wi-Fi → Details → DNS), then verify:

```bash
dig app.teamX.test          # should resolve to Mac 2's IP
curl http://app.teamX.test/api/status
```

## 6. Full end-to-end test (run from any client Mac)

Once Mac 1, 2, 3 and 4 are all running:

```bash
./scripts/smoke-test.sh teamX.test
```

Expected output:
- DNS resolves to Mac 2's IP
- Five repeated requests show `X-Backend: A` and `X-Backend: B` alternating
- Headers include `Cache-Control: max-age=60`

If any step fails, diagnose in this order (see Section 3.1/7.6 of the
main project doc): DNS → TCP reachability → HTTP response → headers.

## 7. Add TLS (Task E) once step 6 passes

Don't attempt HTTPS until plain HTTP load balancing already works — TLS
adds one more layer on top and is much easier to debug when everything
below it is already known-good. Follow Task E in the main project
documentation, then uncomment and fill in the HTTPS `server {}` block in
your local `/opt/homebrew/etc/nginx/servers/cn-project.conf`.

## 8. Committing evidence

Screenshots, `dig`/`curl` output, and `.pcapng` captures go under
`evidence/<task-letter>/`. Commit and push regularly — don't wait until
the night before the review:

```bash
git add evidence/
git commit -m "Add Task B/D/E evidence"
git push
```

## 9. Everyday git workflow for the team

```bash
git pull                          # get teammates' latest changes first
# ... make your changes ...
git add <files>
git commit -m "short description"
git push
```

If two people edit `nginx.conf.template` or `dnsmasq.conf.template` at the
same time, `git pull` may show a merge conflict — resolve it by keeping
both sets of changes (these are small text files, easy to merge by hand),
then `git add`, `git commit`, `git push`.
