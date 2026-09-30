# Repost submit is the one unlabeled button

- Date: 2026-09-29
- Supersedes: `2026-09-29-repost-submit-enabled.md`

The comment rules are unchanged: a comment submit is the one enabled
`type="submit"`, or the one control produced by the exact three-to-four
transition. A generic "only enabled button" fallback stays forbidden.

A commentary repost on the current composer reports three visible buttons, all
enabled before typing, all `type="button"`, none `type="submit"`. Two are
labelled and contain an SVG. One is neither. Requiring that button to be
absent before typing, or disabled before typing, misses it: the reshared post
is already attached, so the control is enabled when the dialog opens.

The repost submit is that one visible enabled `type="button"` in the pinned
dialog with no `aria-label`, no `aria-expanded`, no `aria-pressed`, and no
SVG. Zero matches refuses. Two matches refuses.
