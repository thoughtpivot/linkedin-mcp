# Repost submit is the one unlabeled button not set in prose

- Date: 2026-09-30
- Supersedes: `2026-09-29-repost-submit-unlabeled.md`

The comment rules are unchanged: a comment submit is the one enabled
`type="submit"`, or the one control produced by the exact three-to-four
transition. A generic "only enabled button" fallback stays forbidden.

The unlabeled-button rule of the superseded record was measured against a
composer whose reshared preview had not rendered its text expander. With the
preview rendered, the pinned dialog holds two visible enabled `type="button"`
controls with no `aria-label`, no `aria-expanded`, no `aria-pressed` and no
SVG: the submit, and the preview's "… more" expander. Both carry six
characters of text. One live attempt clicked one of them and reported the
composer still open with nothing on the account's activity; a click on the
expander does exactly that.

The two differ in where they sit. The expander is the last child of the
truncated paragraph, so its parent element carries the paragraph's own text
nodes, over a thousand characters of them. The submit's parent holds only
controls and no text of its own. A button whose parent has text of its own is
part of that text, not a form action, and is excluded. This is structure, not a
label: no attribute value and no text value is compared.

The repost submit is therefore the one visible enabled `type="button"` in the
pinned dialog with no `aria-label`, no `aria-expanded`, no `aria-pressed`, no
SVG, and no text node beside it in its parent. Zero matches refuses. Two
matches refuses.

Two further readings change with this record.

The chosen dialog control is not clicked by the program that found it. It is
handed back and clicked with a real pointer event, as the editor is focused,
because the composer is drawn by handlers that see the event and a scripted
`click()` is the one kind of click that cannot be told apart from one LinkedIn
ignored. Playwright dispatches that click only after its actionability checks
pass, so a timeout raised by it means no event was sent, and that outcome is
reported retry-safe with the typed text taken back.

Whether the composer closed is asked of the dialog handle that was typed into,
never of the dialog selector. The page carries other dialogs — the messaging
panel is one — and a selector-wide wait for "hidden" can time out on a dialog
that was never the composer, which reads exactly like a submit that failed.

## The activity page lags by minutes

Two commentary reposts were published on 2026-09-30 while this was being
measured, and both were meant to be one. The first attempt reported the
composer still open (the selector-wide wait above, timing out on the messaging
panel) and an activity read ten seconds later found nothing; the repost was in
fact live, and the activity page rendered it later. Read as a failure, the
attempt was repeated, and the second composer closed, was polled for nine
seconds, and was reported unconfirmed the same way; a read four minutes later
showed two copies.

So the activity page is the confirmation surface for commentary but not a
prompt one. A composer LinkedIn closed after the submit click — this server
sends no Escape, and the dismiss control is excluded by its label — is
reported as `repost_submitted` with `acted` true and `retry_safe` false,
and its message says the activity page lags and that a retry made on an empty
read published a duplicate. `reposted` remains the status for commentary
actually found rendered. A composer that stayed open remains
`repost_unconfirmed` with `acted` false.
