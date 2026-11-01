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

- Route: Chrome. Not yet edited.
- Bio: `meta[name=description]` on the profile page. About: `https://medium.com/@xbill999/about`.

## Google Developers profile

- Route: Chrome. Not yet edited. `g.dev/xbill` redirects to `me.developers.google.com/u/xbill`.
- Title and summary are separate fields.

## AWS Builder Center

- Route: Chrome, as in the publishing kit. Not yet edited. Profile: `https://builder.aws.com/community/@xbill9`.
- Tagline and About are separate fields.

## Advocu

- Route: Chrome. Not yet edited.
- The page displays the login email. Keep it out of the repo.

## Google Skills

- Formerly Skills Boost. Account page: `https://www.skills.google/my_account/profile`.
- The public profile link returned a 500 error on 2026-10-31.
