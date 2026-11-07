# Find Animation Opportunities — report only

Source: https://www.figma.com/community/skill/68151/find-animation-opportunities

This skill produced recommendations only. The separate user-authorized interface implementation pass applied the two accepted recipes. Frequency, purpose, speed and function were considered before proposing motion.

| # | Location | Today | Purpose | Frequency | Suggested exact recipe |
| --- | --- | --- | --- | --- | --- |
| 1 | `frontend/bento.css:47`, enabled action buttons | Native immediate action with hover color | Confirm deliberate press | Occasional pointer presses; no navigation entrance | Scale 1 → .96 on active press, 150ms ease-out; release returns to 1; no travel; reduced motion keeps scale 1 |
| 2 | `frontend/bento.css:48`, `.transcript-result` | Result appears after processing | Mark arrival of a new result | Once per completed transcription | Opacity 0 → 1, 180ms ease-out, no translate; reduced motion appears instantly |

## Rejected candidates

| Candidate | Gate result |
| --- | --- |
| Page/navigation entrance | Repeated navigation and keyboard work need immediate stable content; no motion |
| Metric values, WER bars and training progress | Data readability matters more than interpolation; avoid ambiguity during polling |
| Decorative waveform and static card hover | No functional state change or affordance; remain static |

Verdict: two small feedback opportunities suffice. No entrance choreography, looping decoration, parallax or animated numbers are justified. The implementation handoff is to Better Interface / Superfuture; no source mutation is attributed to this report-only skill. Reduced-motion overrides cover both recipes.
