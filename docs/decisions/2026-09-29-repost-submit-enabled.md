# Repost submit is the control that becomes enabled

- Date: 2026-09-29
- Supersedes: the repost-dialog bullet of `2026-09-23-current-comment-submit.md`

The comment rules in that record are unchanged: a comment submit is the one
enabled `type="submit"`, or the one control produced by the exact three-to-four
transition. A generic "only enabled button" fallback stays forbidden.

The repost-dialog bullet does not survive the current composer. A commentary
repost typed its text and then reported no submit control: the previous
identity only accepts a button that was absent from the dialog before typing.
A Post control that is already there, and only becomes enabled once the editor
holds text, fails that test. That is the shape this rule now accepts.

The repost submit is therefore the one visible `type="button"` in the pinned
dialog that is enabled at submit time, was not enabled when the editor was
pinned, has no SVG, and carries neither `aria-expanded` nor `aria-pressed`.
Zero matches refuses. Two matches refuses. A control that was already enabled
is never it, which is what keeps a pre-existing close or photo control from
being the candidate.
