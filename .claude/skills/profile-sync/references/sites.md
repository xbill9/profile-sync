# Site reference

One entry per site, measured on 2026-10-31. A property of one site is evidence about that site only; check a new site's form before assuming anything.

Use an API when one can do the job. A site's read route and write route can differ, so check both.

## GitHub

- Route: Chrome, `https://github.com/settings/profile`.
- Field: `#user_profile_bio`.
- Save: "Update profile", far below the field. Read its position after scrolling to it.
- Verify: `check-live.py GitHub`.

## dev.to

- Read route: API, key in `~/.devto.key`, or `DEV_TO_API_KEY`.
- Write route: Chrome, `https://dev.to/settings/profile`. `PUT` and `PATCH` on `/api/users/me` and `/api/users/update` return 404.
- Field: textarea `profile[summary]`, labelled Bio, 200 characters.
- Save: "Save Profile Information", at the bottom of the page.
- Verify: `check-live.py dev.to`.

## Substack

- Route: Chrome.
- Profile bio: `https://substack.com/profile/edit`, textarea `#profile-bio`. A Save button appears under the field once it has text. The Done button at the top does not save the bio.
- Danger: focus the field with JS first. A click can miss, and typed text then scrolls the page, which puts "Make all public" where the Done button was.
- About page: on `https://xbill9.substack.com/about`, Edit page opens a ProseMirror editor with Save at top right. A newline starts a paragraph.
- Verify: `check-live.py Substack` for the bio; read the About page for Long.

## LinkedIn

- Route: Chrome.
- About: `https://www.linkedin.com/in/xbill/edit/forms/summary/new/`, a contenteditable box, 2,600 characters. Read `innerText`, since it has no `value`.
- Certification: `/in/xbill/edit/forms/certification/new/`. Issuer is a typeahead, and it has no exact "Google Cloud" organization; use "Google". Expiry and issue dates are selects.
- After adding a certification LinkedIn offers a share post. Click Skip unless the user asked for a post.
- Credential URL: typed text dropped a digit twice. Compare the field exactly, and insert a missing character at its position.
- The main profile lazy-loads sections, so text extraction misses Experience. Use `/details/experience/`, `/details/certifications/` and the like.
- Verify: read the edit form or details page. Decode any link and compare it whole.

## Credly

- Route: Chrome, `https://www.credly.com/users/xbill/edit`. Click Edit beside Personal Summary, then textarea `#bio`, 600 characters. Save replaces the Edit button.
- Text: Summary.
- Verify: `https://www.credly.com/users/xbill`, compare page text.
- Dashboard URL is private. Tracker uses the public profile URL.

## Medium

- Route: Chrome.
- Short bio: `https://medium.com/me/settings/account`, Profile information opens a dialog with a textarea, 160 characters. Its Save position shifts with the window height, so read it just before clicking.
- About: `https://medium.com/@xbill999/about`, Edit button below the text opens a contenteditable editor. A newline starts a paragraph.
- Verify: read the About page and the profile sidebar.

## Google Developers profile

- Route: Chrome. `g.dev/xbill` redirects to `me.developers.google.com/u/xbill`. Edit profile opens a dialog.
- Bio: textarea, 750 characters.
- Title: a fixed list with no CTO option. It stays Architect.
- Verify: reload the profile and compare page text.

## AWS Builder Center

- Route: Chrome, as in the publishing kit. Edit from `https://builder.aws.com/profile`, not the public URL, which shows a Follow button and no edit controls. Edit about section opens a textarea, 255 characters, and Save stays disabled over the limit.
- Text: Tagline stays as the site's tagline; Short goes in About.
- Verify: `https://builder.aws.com/community/@xbill9`.

## Advocu

- Route: Chrome. From the member page, the menu beside the name leads to `/settings/user-profile/<id>/about`. Biography is a contenteditable editor; Save changes is at the top right.
- The page displays the login email. Keep it out of the repo.
- Verify: member page, after clicking Read more.

## Luma

- Measured 2026-11-01.
- Route: Chrome, `https://luma.com/settings`.
- Field: textarea with the placeholder "Share a little about your background and interests.", labelled Bio, 140 characters. It has no id or name, so find it by placeholder.
- Save: "Save Changes", below Social Links, above the private account fields.
- The page displays the login email and phone number. Keep them out of the repo.
- Username: `xbill`, 15 characters at most. The public URL is `https://luma.com/user/xbill`; `https://luma.com/xbill` returns 404. The user id URL still works.
- Verify: `check-live.py Luma`, which reads `bio_short` from `https://api.lu.ma/user/profile?username=xbill`.

## Google Skills

- Formerly Skills Boost. Account page: `https://www.skills.google/my_account/profile`. It has no bio field, only language and a games name.
- The public profile link returns a 500 error and then navigates back, so it cannot be read.
