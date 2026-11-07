# Superfuture Design Review — LocalVoice

Source: https://www.figma.com/community/skill/65434/superfuture-design-review

Scope: live product, source, empty transcript, upload/record tab, training/GPU-busy state, results and research report. Existing visual identity is retained. User authorized implementation; all ranked fixes below are applied.

| Rank | What | Why | Fix |
| --- | --- | --- | --- |
| Blocking | Meaningful chart mark, field boundaries and sidebar focus missed 3:1 contrast | Users can lose the control or comparison | Reuse neutral and lime tokens; post-fix 6.199:1 / 12.615:1 |
| Important | Heading levels and form-error relationships were inconsistent | Assistive navigation and recovery become harder | Sequential headings, associated persistent hints, correct invalid ownership and explicit recovery |
| Important | Mobile fields and long research lines were uncomfortable | The lab requires both editing and sustained reading | 16px mobile controls, 70ch report paragraphs, balanced headlines |
| Important | Decoration competed with repeated research navigation | Monitoring values calls for stability | Remove route entrance, decorative hover and chart movement; preserve finite task feedback |
| Polish | Card outlines and changing proportional numerals added visual noise | Grouping and progress should be easy to scan | Quiet elevation, tabular numbers, clearer hierarchy |

## Rubric coverage

Hierarchy and type: page title → task panels → measured values → supporting metadata. Spacing: consistent existing grid with stacked mobile cards. Contrast: itemized rendered checks and non-text fixes. Motion: frequency-gated report with reduced-motion fallbacks. States: empty/loading/busy/error and actual regressive metrics remain explicit. Responsive: contained table/navigation scrolling and mobile inputs. Accessibility: semantic headings, labels, keyboard tabs, visible focus and feedback. Content: Spanish fine-tuning and actual baseline comparisons lead. Brand: green, lime and blue with source-derived typography and logo.

## Strengths

- The overview gives fine-tuning and measured comparisons the primary hierarchy.
- Regressions and pending experiments remain visible instead of implying success.
- The live experiment history offers a useful bridge from a polished interface to reproducible research.

The highest-leverage changes were non-text contrast and form recovery; both are complete. Screen-reader output, OS zoom and microphone permission behavior remain runtime checks, not certified results. See the accessibility report for the precise limits.
