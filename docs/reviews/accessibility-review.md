# Accessibility review — LocalVoice live website

Scope: five product pages plus the Record tab state. **623 page-specific elements; 694 measurements/classifications; 547 text-contrast checks.**

Verdict: **0 remaining failures in the measured inventory.** Three non-text contrast failures were corrected. This is a scoped browser review, not a WCAG conformance certification.

The user chose the live website. Figma canvas selection, pins, and annotations are outside this run. Shared chrome is counted separately in each rendered state. Measurements include below-fold rendered content and exclude hidden routes. Disabled controls are contrast-exempt; informational progress indicators are not pointer targets; inline prose links use the target-size exception.

## Itemized inventory

| # | Page / element | Checks and verdict |
| --- | --- | --- |
| 1 | #overview · Skip to main content<br>`a:nth-of-type(1)` | text: pass 16.009:1 (needs 4.5:1); control: pass 190.1×46.5 px |
| 2 | #overview · LocalVoice<br>`aside:nth-of-type(1) > a:nth-of-type(1)` | text: pass 15.836:1 (needs 3:1); control: pass 686.4×37.5 px |
| 3 | #overview · .<br>`aside:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(2)` | text: pass 12.615:1 (needs 3:1) |
| 4 | #overview · Overview<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1)` | text: pass 10.755:1 (needs 4.5:1); control: pass 99.9×44 px |
| 5 | #overview · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 6 | #overview · Speech playground<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2)` | text: pass 10.013:1 (needs 4.5:1); control: pass 148.3×44 px |
| 7 | #overview · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 8 | #overview · Experiments<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3)` | text: pass 10.013:1 (needs 4.5:1); control: pass 113.7×44 px |
| 9 | #overview · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 10 | #overview · Dataset<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4)` | text: pass 10.013:1 (needs 4.5:1); control: pass 89.6×44 px |
| 11 | #overview · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 12 | #overview · Research report<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5)` | text: pass 10.013:1 (needs 4.5:1); control: pass 131.5×44 px |
| 13 | #overview · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 14 | #overview · Workspace<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.903:1 (needs 4.5:1) |
| 15 | #overview · /<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.069:1 (needs 4.5:1) |
| 16 | #overview · Overview<br>`#breadcrumb` | text: pass 11.932:1 (needs 4.5:1) |
| 17 | #overview · Local environment<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.073:1 (needs 4.5:1) |
| 18 | #overview · THE SPANISH FINE-TUNING LAB<br>`#page-overview > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.81:1 (needs 4.5:1) |
| 19 | #overview · Fine-tuning, made measurable<br>`#page-overview > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1)` | text: pass 14.337:1 (needs 3:1) |
| 20 | #overview · .<br>`#page-overview > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1) > span:nth-of-type(1)` | text: pass 5.65:1 (needs 3:1) |
| 21 | #overview · Fine-tune Spanish speech recognition. Measure exactly what your training changes.<br>`#page-overview > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.596:1 (needs 4.5:1) |
| 22 | #overview · Track fine-tuning<br>`#page-overview > div:nth-of-type(1) > a:nth-of-type(1)` | text: pass 6.309:1 (needs 4.5:1); control: pass 163.5×44 px |
| 23 | #overview · Decorative icon paired with a text or named control<br>`#page-overview > div:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 24 | #overview · â†—<br>`#page-overview > div:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(2)` | text: pass 6.309:1 (needs 4.5:1) |
| 25 | #overview · SPANISH SPEECH RECOGNITION<br>`#page-overview > div:nth-of-type(2) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 8.832:1 (needs 4.5:1) |
| 26 | #overview · Adapt the model. Measure the difference.<br>`#page-overview > div:nth-of-type(2) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.283:1 (needs 3:1) |
| 27 | #overview · One pretrained model. Five controlled experiments. Discover what fine-tuning changes, one word at a time.<br>`#page-overview > div:nth-of-type(2) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 9.839:1 (needs 4.5:1) |
| 28 | #overview · Explore the experiment plan<br>`#page-overview > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(1)` | text: pass 10.619:1 (needs 4.5:1); control: pass 192.9×28 px |
| 29 | #overview · â†’<br>`#page-overview > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1)` | text: pass 10.619:1 (needs 4.5:1) |
| 30 | #overview · Whisper Tiny<br>`#page-overview > div:nth-of-type(2) > div:nth-of-type(3) > span:nth-of-type(1)` | text: pass 9.448:1 (needs 4.5:1) |
| 31 | #overview · Decorative icon paired with a text or named control<br>`#page-overview > div:nth-of-type(2) > div:nth-of-type(3) > span:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 32 | #overview · Spanish Â· es<br>`#page-overview > div:nth-of-type(2) > div:nth-of-type(3) > span:nth-of-type(2)` | text: pass 9.448:1 (needs 4.5:1) |
| 33 | #overview · Decorative icon paired with a text or named control<br>`#page-overview > div:nth-of-type(2) > div:nth-of-type(3) > span:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 34 | #overview · Dataset size<br>`#overview-metrics > article:nth-of-type(1) > div:nth-of-type(1)` | text: pass 7.138:1 (needs 4.5:1) |
| 35 | #overview · 13.2<br>`#overview-metrics > article:nth-of-type(1) > div:nth-of-type(2)` | text: pass 13.724:1 (needs 3:1) |
| 36 | #overview · hours<br>`#overview-metrics > article:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.075:1 (needs 4.5:1) |
| 37 | #overview · 4,110 prepared clips<br>`#overview-metrics > article:nth-of-type(1) > div:nth-of-type(3)` | text: pass 6.409:1 (needs 4.5:1) |
| 38 | #overview · Experiments evaluated<br>`#overview-metrics > article:nth-of-type(2) > div:nth-of-type(1)` | text: pass 5.992:1 (needs 4.5:1) |
| 39 | #overview · 3<br>`#overview-metrics > article:nth-of-type(2) > div:nth-of-type(2)` | text: pass 11.519:1 (needs 3:1) |
| 40 | #overview · / 5<br>`#overview-metrics > article:nth-of-type(2) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 5.938:1 (needs 4.5:1) |
| 41 | #overview · E4 train Â· live<br>`#overview-metrics > article:nth-of-type(2) > div:nth-of-type(3)` | text: pass 5.379:1 (needs 4.5:1) |
| 42 | #overview · Best tuned WER<br>`#overview-metrics > article:nth-of-type(3) > div:nth-of-type(1)` | text: pass 7.138:1 (needs 4.5:1) |
| 43 | #overview · 20.9<br>`#overview-metrics > article:nth-of-type(3) > div:nth-of-type(2)` | text: pass 13.724:1 (needs 3:1) |
| 44 | #overview · %<br>`#overview-metrics > article:nth-of-type(3) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.075:1 (needs 4.5:1) |
| 45 | #overview · E1 Â· validation split<br>`#overview-metrics > article:nth-of-type(3) > div:nth-of-type(3)` | text: pass 6.409:1 (needs 4.5:1) |
| 46 | #overview · Relative WER reduction<br>`#overview-metrics > article:nth-of-type(4) > div:nth-of-type(1)` | text: pass 5.972:1 (needs 4.5:1) |
| 47 | #overview · -0.6<br>`#overview-metrics > article:nth-of-type(4) > div:nth-of-type(2)` | text: pass 11.482:1 (needs 3:1) |
| 48 | #overview · %<br>`#overview-metrics > article:nth-of-type(4) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 5.919:1 (needs 4.5:1) |
| 49 | #overview · E1 versus E0 Â· regression<br>`#overview-metrics > article:nth-of-type(4) > div:nth-of-type(3)` | text: pass 5.362:1 (needs 4.5:1) |
| 50 | #overview · From baseline to better<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 51 | #overview · Word error rate across the experiment series<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 6.258:1 (needs 4.5:1) |
| 52 | #overview · Lower is better<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6:1 (needs 4.5:1) |
| 53 | #overview · â†“<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6:1 (needs 4.5:1) |
| 54 | #overview · 100%<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(1) > i:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.125:1 (needs 4.5:1) |
| 55 | #overview · 75%<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(1) > i:nth-of-type(2) > span:nth-of-type(1)` | text: pass 6.125:1 (needs 4.5:1) |
| 56 | #overview · 50%<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(1) > i:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.125:1 (needs 4.5:1) |
| 57 | #overview · 25%<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(1) > i:nth-of-type(4) > span:nth-of-type(1)` | text: pass 6.125:1 (needs 4.5:1) |
| 58 | #overview · 0%<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(1) > i:nth-of-type(5) > span:nth-of-type(1)` | text: pass 6.125:1 (needs 4.5:1) |
| 59 | #overview · backgroundColor<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1)` | non-text: pass 6.199:1 (needs 3:1) |
| 60 | #overview · 20.8%<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 9.876:1 (needs 4.5:1) |
| 61 | #overview · E0<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > small:nth-of-type(1)` | text: pass 6.374:1 (needs 4.5:1) |
| 62 | #overview · backgroundColor<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1)` | non-text: pass 4.776:1 (needs 3:1) |
| 63 | #overview · 20.9%<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 9.876:1 (needs 4.5:1) |
| 64 | #overview · E1<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > small:nth-of-type(1)` | text: pass 6.374:1 (needs 4.5:1) |
| 65 | #overview · backgroundColor<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(1)` | non-text: pass 4.776:1 (needs 3:1) |
| 66 | #overview · 21.6%<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 9.876:1 (needs 4.5:1) |
| 67 | #overview · E2<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > small:nth-of-type(1)` | text: pass 6.374:1 (needs 4.5:1) |
| 68 | #overview · E3<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(4) > small:nth-of-type(1)` | text: pass 6.374:1 (needs 4.5:1) |
| 69 | #overview · E4<br>`#overview-chart > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(5) > small:nth-of-type(1)` | text: pass 6.374:1 (needs 4.5:1) |
| 70 | #overview · Pretrained<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(1) > div:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.448:1 (needs 4.5:1) |
| 71 | #overview · Fine-tuned<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(1) > div:nth-of-type(3) > span:nth-of-type(2)` | text: pass 6.448:1 (needs 4.5:1) |
| 72 | #overview · validation split Â· comparable runs only<br>`#chart-split` | text: pass 6.448:1 (needs 4.5:1) |
| 73 | #overview · The path to improvement<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 74 | #overview · A reproducible research workflow<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 6.258:1 (needs 4.5:1) |
| 75 | #overview · 2 / 4<br>`#steps-count` | text: pass 6.272:1 (needs 4.5:1) |
| 76 | #overview · âœ“<br>`#steps > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.959:1 (needs 4.5:1) |
| 77 | #overview · Prepare the data<br>`#steps > div:nth-of-type(1) > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 9.802:1 (needs 4.5:1) |
| 78 | #overview · Validate clips, transcripts, and split integrity<br>`#steps > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.581:1 (needs 4.5:1) |
| 79 | #overview · Complete<br>`#steps > div:nth-of-type(1) > span:nth-of-type(2)` | text: pass 5.449:1 (needs 4.5:1) |
| 80 | #overview · âœ“<br>`#steps > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 6.959:1 (needs 4.5:1) |
| 81 | #overview · Establish the baseline<br>`#steps > div:nth-of-type(2) > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 9.802:1 (needs 4.5:1) |
| 82 | #overview · Measure pretrained recognition quality<br>`#steps > div:nth-of-type(2) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.581:1 (needs 4.5:1) |
| 83 | #overview · Complete<br>`#steps > div:nth-of-type(2) > span:nth-of-type(2)` | text: pass 5.449:1 (needs 4.5:1) |
| 84 | #overview · 3<br>`#steps > div:nth-of-type(3) > span:nth-of-type(1)` | text: pass 4.96:1 (needs 4.5:1) |
| 85 | #overview · Fine-tune & experiment<br>`#steps > div:nth-of-type(3) > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 9.802:1 (needs 4.5:1) |
| 86 | #overview · Compare full tuning, LoRA, and augmentation<br>`#steps > div:nth-of-type(3) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.581:1 (needs 4.5:1) |
| 87 | #overview · In progress<br>`#steps > div:nth-of-type(3) > span:nth-of-type(2)` | text: pass 5.449:1 (needs 4.5:1) |
| 88 | #overview · 4<br>`#steps > div:nth-of-type(4) > span:nth-of-type(1)` | text: pass 4.96:1 (needs 4.5:1) |
| 89 | #overview · Evaluate & understand<br>`#steps > div:nth-of-type(4) > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 9.802:1 (needs 4.5:1) |
| 90 | #overview · Report the changes, costs, and limitations<br>`#steps > div:nth-of-type(4) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.581:1 (needs 4.5:1) |
| 91 | #overview · Pending<br>`#steps > div:nth-of-type(4) > span:nth-of-type(2)` | text: pass 5.449:1 (needs 4.5:1) |
| 92 | #overview · View research notes<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(2) > a:nth-of-type(1)` | text: pass 8.408:1 (needs 4.5:1); control: pass 680.8×47.3 px |
| 93 | #overview · â†—<br>`#page-overview > div:nth-of-type(4) > article:nth-of-type(2) > a:nth-of-type(1) > span:nth-of-type(1)` | text: pass 8.408:1 (needs 4.5:1) |
| 94 | #overview · One model. Five perspectives.<br>`#page-overview > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 95 | #overview · A controlled comparison of strategy and augmentation.<br>`#page-overview > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 6.258:1 (needs 4.5:1) |
| 96 | #overview · All experiments<br>`#page-overview > article:nth-of-type(1) > div:nth-of-type(1) > a:nth-of-type(1)` | text: pass 7.019:1 (needs 4.5:1); control: pass 97.6×28 px |
| 97 | #overview · â†’<br>`#page-overview > article:nth-of-type(1) > div:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1)` | text: pass 7.019:1 (needs 4.5:1) |
| 98 | #overview · Experiment summary, horizontally scrollable<br>`#overview-table` | control: pass 680.8×348.8 px |
| 99 | #overview · EXPERIMENT<br>`#overview-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(1)` | text: pass 5.954:1 (needs 4.5:1) |
| 100 | #overview · STRATEGY<br>`#overview-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(2)` | text: pass 5.954:1 (needs 4.5:1) |
| 101 | #overview · AUGMENTATION<br>`#overview-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(3)` | text: pass 5.954:1 (needs 4.5:1) |
| 102 | #overview · WER â†“<br>`#overview-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(4)` | text: pass 5.954:1 (needs 4.5:1) |
| 103 | #overview · STATUS<br>`#overview-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(5)` | text: pass 5.954:1 (needs 4.5:1) |
| 104 | #overview · Pretrained baseline<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 105 | #overview · E0<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 106 | #overview · Pretrained<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 107 | #overview · â€” None<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 5.275:1 (needs 4.5:1) |
| 108 | #overview · 20.8%<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 109 | #overview · evaluated<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(5) > span:nth-of-type(1)` | text: pass 6.271:1 (needs 4.5:1) |
| 110 | #overview · Full fine-tuning<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 111 | #overview · E1<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 112 | #overview · Full fine-tuning<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 113 | #overview · â€” None<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 5.275:1 (needs 4.5:1) |
| 114 | #overview · 20.9%<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 115 | #overview · evaluated<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(5) > span:nth-of-type(1)` | text: pass 6.271:1 (needs 4.5:1) |
| 116 | #overview · LoRA fine-tuning<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 117 | #overview · E2<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 118 | #overview · LoRA<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 119 | #overview · â€” None<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 5.275:1 (needs 4.5:1) |
| 120 | #overview · 21.6%<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 121 | #overview · evaluated<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(5) > span:nth-of-type(1)` | text: pass 6.271:1 (needs 4.5:1) |
| 122 | #overview · Full + augmentation<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 123 | #overview · E3<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 124 | #overview · Full fine-tuning<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 125 | #overview · âœ§ Enabled<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.732:1 (needs 4.5:1) |
| 126 | #overview · â€”<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 127 | #overview · planned<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(5) > span:nth-of-type(1)` | text: pass 5.856:1 (needs 4.5:1) |
| 128 | #overview · LoRA + augmentation<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 129 | #overview · E4<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 130 | #overview · LoRA<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 131 | #overview · âœ§ Enabled<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.732:1 (needs 4.5:1) |
| 132 | #overview · â€”<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 133 | #overview · running<br>`#overview-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(5) > span:nth-of-type(1)` | text: pass 5.856:1 (needs 4.5:1) |
| 134 | #overview · LocalVoice   Built for measurable progress.<br>`#page-overview > footer:nth-of-type(1) > span:nth-of-type(1)` | text: pass 5.557:1 (needs 4.5:1) |
| 135 | #overview · /<br>`#page-overview > footer:nth-of-type(1) > span:nth-of-type(1) > span:nth-of-type(1)` | text: pass 5.557:1 (needs 4.5:1) |
| 136 | #overview · No improvement claims without evaluation.<br>`#page-overview > footer:nth-of-type(1) > span:nth-of-type(2)` | text: pass 5.557:1 (needs 4.5:1) |
| 137 | #overview · Word error rate by experiment, percentages shown above bars<br>`[role=img] measured graphic 1` | graphic-label: pass |
| 138 | #playground · Skip to main content<br>`a:nth-of-type(1)` | text: pass 16.009:1 (needs 4.5:1); control: pass 190.1×46.5 px |
| 139 | #playground · LocalVoice<br>`aside:nth-of-type(1) > a:nth-of-type(1)` | text: pass 15.836:1 (needs 3:1); control: pass 686.4×37.5 px |
| 140 | #playground · .<br>`aside:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(2)` | text: pass 12.615:1 (needs 3:1) |
| 141 | #playground · Overview<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1)` | text: pass 10.013:1 (needs 4.5:1); control: pass 97.2×44 px |
| 142 | #playground · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 143 | #playground · Speech playground<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2)` | text: pass 10.755:1 (needs 4.5:1); control: pass 153.4×44 px |
| 144 | #playground · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 145 | #playground · Experiments<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3)` | text: pass 10.013:1 (needs 4.5:1); control: pass 113.7×44 px |
| 146 | #playground · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 147 | #playground · Dataset<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4)` | text: pass 10.013:1 (needs 4.5:1); control: pass 89.6×44 px |
| 148 | #playground · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 149 | #playground · Research report<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5)` | text: pass 10.013:1 (needs 4.5:1); control: pass 131.5×44 px |
| 150 | #playground · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 151 | #playground · Workspace<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.903:1 (needs 4.5:1) |
| 152 | #playground · /<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.069:1 (needs 4.5:1) |
| 153 | #playground · Speech playground<br>`#breadcrumb` | text: pass 11.932:1 (needs 4.5:1) |
| 154 | #playground · Local environment<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.073:1 (needs 4.5:1) |
| 155 | #playground · LISTEN. TRANSCRIBE. COMPARE.<br>`#page-playground > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.81:1 (needs 4.5:1) |
| 156 | #playground · Speech playground<br>`#page-playground > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1)` | text: pass 14.337:1 (needs 3:1) |
| 157 | #playground · .<br>`#page-playground > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1) > span:nth-of-type(1)` | text: pass 5.65:1 (needs 3:1) |
| 158 | #playground · Hear what your model can do. Compare the same clip across experiments.<br>`#page-playground > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.596:1 (needs 4.5:1) |
| 159 | #playground · Spanish Â· up to 30 seconds<br>`#page-playground > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6:1 (needs 4.5:1) |
| 160 | #playground · Give your voice a place<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 161 | #playground · Decorative icon paired with a text or named control<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 162 | #playground · Upload audio<br>`#upload-tab` | text: pass 10.019:1 (needs 4.5:1); control: pass 291.7×41 px |
| 163 | #playground · Record speech<br>`#record-tab` | text: pass 5.261:1 (needs 4.5:1); control: pass 291.7×41 px |
| 164 | #playground · borderTopColor<br>`#drop-zone` | non-text: pass 5.878:1 (needs 3:1) |
| 165 | #playground · Decorative icon paired with a text or named control<br>`#drop-zone > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 166 | #playground · Drop your audio here<br>`#drop-zone > strong:nth-of-type(1)` | text: pass 9.048:1 (needs 4.5:1) |
| 167 | #playground · or   to get started<br>`#drop-zone > span:nth-of-type(2)` | text: pass 5.71:1 (needs 4.5:1) |
| 168 | #playground · browse files<br>`#drop-zone > span:nth-of-type(2) > u:nth-of-type(1)` | text: pass 5.71:1 (needs 4.5:1) |
| 169 | #playground · WAV, FLAC, OGG Â· max 12 MB Â· 30 seconds<br>`#audio-hint` | text: pass 5.13:1 (needs 4.5:1) |
| 170 | #playground · Drop your audio hereor browse files to get startedWAV, FLAC, OGG Â· max 12 MB Â· 30 seconds<br>`#audio-file` | control: pass 596.8×208.4 px |
| 171 | #playground · Try a Spanish dataset sample<br>`#sample-button` | text: pass 6.545:1 (needs 4.5:1); control: pass 598.4×44 px |
| 172 | #playground · â†—<br>`#sample-button > span:nth-of-type(1)` | text: pass 6.545:1 (needs 4.5:1) |
| 173 | #playground · Model to test<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > label:nth-of-type(1)` | text: pass 8.872:1 (needs 4.5:1) |
| 174 | #playground · Model to test<br>`#model-select` | control: pass 598.4×46 px; non-text: pass 6.199:1 (needs 3:1) |
| 175 | #playground · Compare with pretrained baseline<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > label:nth-of-type(2)` | text: pass 7.524:1 (needs 4.5:1) |
| 176 | #playground · Compare with pretrained baseline<br>`#compare-models` | control: pass 24×24 px |
| 177 | #playground · Reference transcript<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > label:nth-of-type(3)` | text: pass 8.872:1 (needs 4.5:1) |
| 178 | #playground · optional<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > label:nth-of-type(3) > span:nth-of-type(1)` | text: pass 5.392:1 (needs 4.5:1) |
| 179 | #playground · Reference transcript optional<br>`#reference` | control: pass 598.4×99.7 px; non-text: pass 6.199:1 (needs 3:1) |
| 180 | #playground · Use the exact Spanish words spoken in the clip. Accents and Ã± are preserved.<br>`#reference-hint` | text: pass 6.441:1 (needs 4.5:1) |
| 181 | #playground · Transcribe audio<br>`#transcribe-button` | text: exempt 6.309:1 (needs 4.5:1); control: disabled 598.4×44 px |
| 182 | #playground · Decorative icon paired with a text or named control<br>`#transcribe-button > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 183 | #playground · GPU reserved for the experiment series. Speech testing resumes when the series finishes.<br>`#inference-availability` | text: pass 6.441:1 (needs 4.5:1) |
| 184 | #playground · Audio stays on this machine. Models download on first use.<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > p:nth-of-type(2)` | text: pass 6.441:1 (needs 4.5:1) |
| 185 | #playground · Decorative icon paired with a text or named control<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > p:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 186 | #playground · The words behind the sound<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 187 | #playground · Your transcription will appear here<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 6.258:1 (needs 4.5:1) |
| 188 | #playground · Copy transcript<br>`#copy-transcript` | control: pass 40×40 px |
| 189 | #playground · Copy transcript<br>`#copy-transcript > span:nth-of-type(1) > svg:nth-of-type(1)` | meaningful-icon: pass 6.409:1 (needs 3:1) |
| 190 | #playground · Decorative icon paired with a text or named control<br>`#transcript-results > div:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 191 | #playground · Ready when you are.<br>`#transcript-results > div:nth-of-type(1) > h3:nth-of-type(1)` | text: pass 7.299:1 (needs 4.5:1) |
| 192 | #playground · Upload or record a clip, select a model, and turn speech into something you can study.<br>`#transcript-results > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.41:1 (needs 4.5:1) |
| 193 | #playground · Decorative icon paired with a text or named control<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 194 | #playground · A playground is a starting point.<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(2) > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 6.875:1 (needs 4.5:1) |
| 195 | #playground · Single-clip scores help inspect errors. Use the fixed evaluation split to make research claims. Model loading and inference time are reported separately.<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(2) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.206:1 (needs 4.5:1) |
| 196 | #experiments · Skip to main content<br>`a:nth-of-type(1)` | text: pass 16.009:1 (needs 4.5:1); control: pass 190.1×46.5 px |
| 197 | #experiments · LocalVoice<br>`aside:nth-of-type(1) > a:nth-of-type(1)` | text: pass 15.836:1 (needs 3:1); control: pass 686.4×37.5 px |
| 198 | #experiments · .<br>`aside:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(2)` | text: pass 12.615:1 (needs 3:1) |
| 199 | #experiments · Overview<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1)` | text: pass 10.013:1 (needs 4.5:1); control: pass 97.2×44 px |
| 200 | #experiments · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 201 | #experiments · Speech playground<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2)` | text: pass 10.013:1 (needs 4.5:1); control: pass 148.3×44 px |
| 202 | #experiments · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 203 | #experiments · Experiments<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3)` | text: pass 10.755:1 (needs 4.5:1); control: pass 117.7×44 px |
| 204 | #experiments · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 205 | #experiments · Dataset<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4)` | text: pass 10.013:1 (needs 4.5:1); control: pass 89.6×44 px |
| 206 | #experiments · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 207 | #experiments · Research report<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5)` | text: pass 10.013:1 (needs 4.5:1); control: pass 131.5×44 px |
| 208 | #experiments · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 209 | #experiments · Workspace<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.903:1 (needs 4.5:1) |
| 210 | #experiments · /<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.069:1 (needs 4.5:1) |
| 211 | #experiments · Experiments<br>`#breadcrumb` | text: pass 11.932:1 (needs 4.5:1) |
| 212 | #experiments · Local environment<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.073:1 (needs 4.5:1) |
| 213 | #experiments · CONTROLLED EXPERIMENTS<br>`#page-experiments > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.81:1 (needs 4.5:1) |
| 214 | #experiments · Make the difference measurable<br>`#page-experiments > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1)` | text: pass 14.337:1 (needs 3:1) |
| 215 | #experiments · .<br>`#page-experiments > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1) > span:nth-of-type(1)` | text: pass 5.65:1 (needs 3:1) |
| 216 | #experiments · A live view of model updates, validation checkpoints, and measured improvements.<br>`#page-experiments > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.596:1 (needs 4.5:1) |
| 217 | #experiments · Export results<br>`#page-experiments > div:nth-of-type(1) > a:nth-of-type(1)` | text: pass 11.259:1 (needs 4.5:1); control: pass 129.8×44 px |
| 218 | #experiments · Decorative icon paired with a text or named control<br>`#page-experiments > div:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 219 | #experiments · The fine-tuning board<br>`#page-experiments > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.606:1 (needs 4.5:1) |
| 220 | #experiments · Real optimizer updates, learning curves, and validation-selected checkpoints.<br>`#page-experiments > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 6.07:1 (needs 4.5:1) |
| 221 | #experiments · Whisper Â· Spanish<br>`#page-experiments > article:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6:1 (needs 4.5:1) |
| 222 | #experiments · Â· E4 train<br>`#training-progress > p:nth-of-type(1)` | text: pass 6.526:1 (needs 4.5:1) |
| 223 | #experiments · Experiment series: running<br>`#training-progress > p:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 11.274:1 (needs 4.5:1) |
| 224 | #experiments · Full tuning updates every model parameter. LoRA updates query/value adapters. Augmentation is applied only to training audio. The best checkpoint is selected by validation WER.<br>`#training-progress > p:nth-of-type(2)` | text: pass 6.526:1 (needs 4.5:1) |
| 225 | #experiments · E1 Â· Full fine-tuning<br>`#training-progress > div:nth-of-type(1) > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 11.274:1 (needs 4.5:1) |
| 226 | #experiments · evaluated Â· completed<br>`#training-progress > div:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.362:1 (needs 4.5:1) |
| 227 | #experiments · E1 completed progress<br>`#training-progress > div:nth-of-type(1) > div:nth-of-type(2)` | control: pass 630.8×7 px; Informational progress indicator, not a pointer target |
| 228 | #experiments · Epoch 3 / 5<br>`#training-progress > div:nth-of-type(1) > div:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.362:1 (needs 4.5:1) |
| 229 | #experiments · 1050 optimizer updates<br>`#training-progress > div:nth-of-type(1) > div:nth-of-type(3) > span:nth-of-type(2)` | text: pass 6.362:1 (needs 4.5:1) |
| 230 | #experiments · Loss 0.898<br>`#training-progress > div:nth-of-type(1) > div:nth-of-type(3) > span:nth-of-type(3)` | text: pass 6.362:1 (needs 4.5:1) |
| 231 | #experiments · Best validation WER 20.9%<br>`#training-progress > div:nth-of-type(1) > div:nth-of-type(3) > span:nth-of-type(4)` | text: pass 6.362:1 (needs 4.5:1) |
| 232 | #experiments · Validation word error rate. Epoch 1: 20.9 percent. Epoch 2: 21.3 percent. Epoch 3: 21.2 percent. Lower is better.<br>`#training-progress > div:nth-of-type(1) > svg:nth-of-type(1)` | graphic: pass |
| 233 | #experiments · Validation WER by epoch Â· lower is better Â· see exact values below<br>`#training-progress > div:nth-of-type(1) > small:nth-of-type(1)` | text: pass 6.113:1 (needs 4.5:1) |
| 234 | #experiments · E2 Â· LoRA fine-tuning<br>`#training-progress > div:nth-of-type(2) > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 11.274:1 (needs 4.5:1) |
| 235 | #experiments · evaluated Â· completed<br>`#training-progress > div:nth-of-type(2) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.362:1 (needs 4.5:1) |
| 236 | #experiments · E2 completed progress<br>`#training-progress > div:nth-of-type(2) > div:nth-of-type(2)` | control: pass 630.8×7 px; Informational progress indicator, not a pointer target |
| 237 | #experiments · Epoch 5 / 5<br>`#training-progress > div:nth-of-type(2) > div:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.362:1 (needs 4.5:1) |
| 238 | #experiments · 1750 optimizer updates<br>`#training-progress > div:nth-of-type(2) > div:nth-of-type(3) > span:nth-of-type(2)` | text: pass 6.362:1 (needs 4.5:1) |
| 239 | #experiments · Loss 1.453<br>`#training-progress > div:nth-of-type(2) > div:nth-of-type(3) > span:nth-of-type(3)` | text: pass 6.362:1 (needs 4.5:1) |
| 240 | #experiments · Best validation WER 21.6%<br>`#training-progress > div:nth-of-type(2) > div:nth-of-type(3) > span:nth-of-type(4)` | text: pass 6.362:1 (needs 4.5:1) |
| 241 | #experiments · Validation word error rate. Epoch 1: 168.9 percent. Epoch 2: 51.7 percent. Epoch 3: 21.6 percent. Epoch 4: 21.7 percent. Epoch 5: 21.8 percent. Lower is better.<br>`#training-progress > div:nth-of-type(2) > svg:nth-of-type(1)` | graphic: pass |
| 242 | #experiments · Validation WER by epoch Â· lower is better Â· see exact values below<br>`#training-progress > div:nth-of-type(2) > small:nth-of-type(1)` | text: pass 6.113:1 (needs 4.5:1) |
| 243 | #experiments · E4 Â· LoRA + augmentation<br>`#training-progress > div:nth-of-type(3) > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 11.274:1 (needs 4.5:1) |
| 244 | #experiments · running Â· validation<br>`#training-progress > div:nth-of-type(3) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.362:1 (needs 4.5:1) |
| 245 | #experiments · E4 validation progress<br>`#training-progress > div:nth-of-type(3) > div:nth-of-type(2)` | control: pass 630.8×7 px; Informational progress indicator, not a pointer target |
| 246 | #experiments · Epoch 2 / 5<br>`#training-progress > div:nth-of-type(3) > div:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.362:1 (needs 4.5:1) |
| 247 | #experiments · 700 optimizer updates<br>`#training-progress > div:nth-of-type(3) > div:nth-of-type(3) > span:nth-of-type(2)` | text: pass 6.362:1 (needs 4.5:1) |
| 248 | #experiments · Loss 1.798<br>`#training-progress > div:nth-of-type(3) > div:nth-of-type(3) > span:nth-of-type(3)` | text: pass 6.362:1 (needs 4.5:1) |
| 249 | #experiments · Best validation WER 179.6%<br>`#training-progress > div:nth-of-type(3) > div:nth-of-type(3) > span:nth-of-type(4)` | text: pass 6.362:1 (needs 4.5:1) |
| 250 | #experiments · Validation word error rate. Epoch 1: 179.6 percent. Lower is better.<br>`#training-progress > div:nth-of-type(3) > svg:nth-of-type(1)` | graphic: pass |
| 251 | #experiments · Validation WER by epoch Â· lower is better Â· see exact values below<br>`#training-progress > div:nth-of-type(3) > small:nth-of-type(1)` | text: pass 6.113:1 (needs 4.5:1) |
| 252 | #experiments · Dataset size<br>`#experiment-metrics > article:nth-of-type(1) > div:nth-of-type(1)` | text: pass 7.138:1 (needs 4.5:1) |
| 253 | #experiments · 13.2<br>`#experiment-metrics > article:nth-of-type(1) > div:nth-of-type(2)` | text: pass 13.724:1 (needs 3:1) |
| 254 | #experiments · hours<br>`#experiment-metrics > article:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.075:1 (needs 4.5:1) |
| 255 | #experiments · 4,110 prepared clips<br>`#experiment-metrics > article:nth-of-type(1) > div:nth-of-type(3)` | text: pass 6.409:1 (needs 4.5:1) |
| 256 | #experiments · Experiments evaluated<br>`#experiment-metrics > article:nth-of-type(2) > div:nth-of-type(1)` | text: pass 5.992:1 (needs 4.5:1) |
| 257 | #experiments · 3<br>`#experiment-metrics > article:nth-of-type(2) > div:nth-of-type(2)` | text: pass 11.519:1 (needs 3:1) |
| 258 | #experiments · / 5<br>`#experiment-metrics > article:nth-of-type(2) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 5.938:1 (needs 4.5:1) |
| 259 | #experiments · E4 train Â· live<br>`#experiment-metrics > article:nth-of-type(2) > div:nth-of-type(3)` | text: pass 5.379:1 (needs 4.5:1) |
| 260 | #experiments · Best tuned WER<br>`#experiment-metrics > article:nth-of-type(3) > div:nth-of-type(1)` | text: pass 7.138:1 (needs 4.5:1) |
| 261 | #experiments · 20.9<br>`#experiment-metrics > article:nth-of-type(3) > div:nth-of-type(2)` | text: pass 13.724:1 (needs 3:1) |
| 262 | #experiments · %<br>`#experiment-metrics > article:nth-of-type(3) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.075:1 (needs 4.5:1) |
| 263 | #experiments · E1 Â· validation split<br>`#experiment-metrics > article:nth-of-type(3) > div:nth-of-type(3)` | text: pass 6.409:1 (needs 4.5:1) |
| 264 | #experiments · Relative WER reduction<br>`#experiment-metrics > article:nth-of-type(4) > div:nth-of-type(1)` | text: pass 5.972:1 (needs 4.5:1) |
| 265 | #experiments · -0.6<br>`#experiment-metrics > article:nth-of-type(4) > div:nth-of-type(2)` | text: pass 11.482:1 (needs 3:1) |
| 266 | #experiments · %<br>`#experiment-metrics > article:nth-of-type(4) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 5.919:1 (needs 4.5:1) |
| 267 | #experiments · E1 versus E0 Â· regression<br>`#experiment-metrics > article:nth-of-type(4) > div:nth-of-type(3)` | text: pass 5.362:1 (needs 4.5:1) |
| 268 | #experiments · Experiment matrix<br>`#page-experiments > article:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 269 | #experiments · Actual evaluation results are loaded directly from local run artifacts.<br>`#page-experiments > article:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 6.258:1 (needs 4.5:1) |
| 270 | #experiments · Refresh<br>`#refresh-results` | text: pass 11.259:1 (needs 4.5:1); control: pass 105.4×44 px |
| 271 | #experiments · Decorative icon paired with a text or named control<br>`#refresh-results > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 272 | #experiments · Detailed experiment measurements, horizontally scrollable<br>`#experiment-table` | control: pass 680.8×359.2 px |
| 273 | #experiments · EXPERIMENT<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(1)` | text: pass 5.954:1 (needs 4.5:1) |
| 274 | #experiments · STRATEGY<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(2)` | text: pass 5.954:1 (needs 4.5:1) |
| 275 | #experiments · AUGMENTATION<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(3)` | text: pass 5.954:1 (needs 4.5:1) |
| 276 | #experiments · WER â†“<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(4)` | text: pass 5.954:1 (needs 4.5:1) |
| 277 | #experiments · CER â†“<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(5)` | text: pass 5.954:1 (needs 4.5:1) |
| 278 | #experiments · TRAIN TIME<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(6)` | text: pass 5.954:1 (needs 4.5:1) |
| 279 | #experiments · GPU MEMORY<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(7)` | text: pass 5.954:1 (needs 4.5:1) |
| 280 | #experiments · TRAINABLE<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(8)` | text: pass 5.954:1 (needs 4.5:1) |
| 281 | #experiments · LATENCY<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(9)` | text: pass 5.954:1 (needs 4.5:1) |
| 282 | #experiments · SPLIT<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(10)` | text: pass 5.954:1 (needs 4.5:1) |
| 283 | #experiments · STATUS<br>`#experiment-table > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(11)` | text: pass 5.954:1 (needs 4.5:1) |
| 284 | #experiments · Pretrained baseline<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 285 | #experiments · E0<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 286 | #experiments · Pretrained<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 287 | #experiments · â€” None<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 5.275:1 (needs 4.5:1) |
| 288 | #experiments · 20.8%<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 289 | #experiments · 6.5%<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(5)` | text: pass 6.905:1 (needs 4.5:1) |
| 290 | #experiments · 0.0 min<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(6)` | text: pass 6.905:1 (needs 4.5:1) |
| 291 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(7)` | text: pass 6.905:1 (needs 4.5:1) |
| 292 | #experiments · 0<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(8)` | text: pass 6.905:1 (needs 4.5:1) |
| 293 | #experiments · 0.31 s<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(9)` | text: pass 6.905:1 (needs 4.5:1) |
| 294 | #experiments · validation<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(10)` | text: pass 6.905:1 (needs 4.5:1) |
| 295 | #experiments · evaluated<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(11) > span:nth-of-type(1)` | text: pass 6.271:1 (needs 4.5:1) |
| 296 | #experiments · Full fine-tuning<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 297 | #experiments · E1<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 298 | #experiments · Full fine-tuning<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 299 | #experiments · â€” None<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 5.275:1 (needs 4.5:1) |
| 300 | #experiments · 20.9%<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 301 | #experiments · 6.7%<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(5)` | text: pass 6.905:1 (needs 4.5:1) |
| 302 | #experiments · 8.5 min<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(6)` | text: pass 6.905:1 (needs 4.5:1) |
| 303 | #experiments · 1006 MB<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(7)` | text: pass 6.905:1 (needs 4.5:1) |
| 304 | #experiments · 37,184,640<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(8)` | text: pass 6.905:1 (needs 4.5:1) |
| 305 | #experiments · 0.23 s<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(9)` | text: pass 6.905:1 (needs 4.5:1) |
| 306 | #experiments · validation<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(10)` | text: pass 6.905:1 (needs 4.5:1) |
| 307 | #experiments · evaluated<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(11) > span:nth-of-type(1)` | text: pass 6.271:1 (needs 4.5:1) |
| 308 | #experiments · LoRA fine-tuning<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 309 | #experiments · E2<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 310 | #experiments · LoRA<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 311 | #experiments · â€” None<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 5.275:1 (needs 4.5:1) |
| 312 | #experiments · 21.6%<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 313 | #experiments · 6.9%<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(5)` | text: pass 6.905:1 (needs 4.5:1) |
| 314 | #experiments · 20.0 min<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(6)` | text: pass 6.905:1 (needs 4.5:1) |
| 315 | #experiments · 673 MB<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(7)` | text: pass 6.905:1 (needs 4.5:1) |
| 316 | #experiments · 147,456<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(8)` | text: pass 6.905:1 (needs 4.5:1) |
| 317 | #experiments · 0.27 s<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(9)` | text: pass 6.905:1 (needs 4.5:1) |
| 318 | #experiments · validation<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(10)` | text: pass 6.905:1 (needs 4.5:1) |
| 319 | #experiments · evaluated<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(11) > span:nth-of-type(1)` | text: pass 6.271:1 (needs 4.5:1) |
| 320 | #experiments · Full + augmentation<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 321 | #experiments · E3<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 322 | #experiments · Full fine-tuning<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 323 | #experiments · âœ§ Enabled<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.732:1 (needs 4.5:1) |
| 324 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 325 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(5)` | text: pass 6.905:1 (needs 4.5:1) |
| 326 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(6)` | text: pass 6.905:1 (needs 4.5:1) |
| 327 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(7)` | text: pass 6.905:1 (needs 4.5:1) |
| 328 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(8)` | text: pass 6.905:1 (needs 4.5:1) |
| 329 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(9)` | text: pass 6.905:1 (needs 4.5:1) |
| 330 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(10)` | text: pass 6.905:1 (needs 4.5:1) |
| 331 | #experiments · planned<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(11) > span:nth-of-type(1)` | text: pass 5.856:1 (needs 4.5:1) |
| 332 | #experiments · LoRA + augmentation<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(1)` | text: pass 11.312:1 (needs 4.5:1) |
| 333 | #experiments · E4<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.034:1 (needs 4.5:1) |
| 334 | #experiments · LoRA<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 335 | #experiments · âœ§ Enabled<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.732:1 (needs 4.5:1) |
| 336 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 337 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(5)` | text: pass 6.905:1 (needs 4.5:1) |
| 338 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(6)` | text: pass 6.905:1 (needs 4.5:1) |
| 339 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(7)` | text: pass 6.905:1 (needs 4.5:1) |
| 340 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(8)` | text: pass 6.905:1 (needs 4.5:1) |
| 341 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(9)` | text: pass 6.905:1 (needs 4.5:1) |
| 342 | #experiments · â€”<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(10)` | text: pass 6.905:1 (needs 4.5:1) |
| 343 | #experiments · running<br>`#experiment-table > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(11) > span:nth-of-type(1)` | text: pass 5.856:1 (needs 4.5:1) |
| 344 | #experiments · What changed, and by how much?<br>`#page-experiments > div:nth-of-type(3) > article:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 345 | #experiments · Baseline WER:   on the   split. Positive reductions mean fewer errors; negative values are regressions.<br>`#improvement-details > p:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 346 | #experiments · 20.8%<br>`#improvement-details > p:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 347 | #experiments · validation<br>`#improvement-details > p:nth-of-type(1) > strong:nth-of-type(2)` | text: pass 11.623:1 (needs 4.5:1) |
| 348 | #experiments · E1 Â· Full fine-tuning<br>`#improvement-details > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 349 | #experiments · -0.1 pp WER Â· -0.2 pp CER<br>`#improvement-details > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 350 | #experiments · E2 Â· LoRA fine-tuning<br>`#improvement-details > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 351 | #experiments · -0.8 pp WER Â· -0.4 pp CER<br>`#improvement-details > div:nth-of-type(2) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 352 | #experiments · Augmentation effect: compare E3 with E1 and E4 with E2. LoRA effect: compare E2 with E1 and E4 with E3.<br>`#improvement-details > p:nth-of-type(2)` | text: pass 6.728:1 (needs 4.5:1) |
| 353 | #experiments · LoRA versus full<br>`#improvement-details > div:nth-of-type(3) > span:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 354 | #experiments · -0.7 pp WER reduction<br>`#improvement-details > div:nth-of-type(3) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 355 | #experiments · Run an experiment<br>`#page-experiments > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 356 | #experiments · Run these commands in the project terminal. Training uses the settings in  .<br>`#page-experiments > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(2) > p:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 357 | #experiments · configs/training.json<br>`#page-experiments > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(2) > p:nth-of-type(1) > code:nth-of-type(1)` | text: pass 7.538:1 (needs 4.5:1) |
| 358 | #experiments · .venv\Scripts\localvoice train E2 .venv\Scripts\localvoice evaluate E2<br>`#page-experiments > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(2) > pre:nth-of-type(1)` | text: pass 7.535:1 (needs 4.5:1) |
| 359 | #experiments · Start with validation results. Freeze experiment choices before unlocking test evaluation.<br>`#page-experiments > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(2) > p:nth-of-type(2)` | text: pass 6.728:1 (needs 4.5:1) |
| 360 | #experiments · Look inside the results<br>`#page-experiments > article:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 361 | #experiments · Error patterns, training history, and labeled subgroups.<br>`#page-experiments > article:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 6.258:1 (needs 4.5:1) |
| 362 | #experiments · E0 Â· Pretrained baseline<br>`#diagnostics > details:nth-of-type(1) > summary:nth-of-type(1)` | text: pass 8.123:1 (needs 4.5:1); control: pass 630.8×28 px |
| 363 | #experiments · 1547 substitutions Â· 186 deletions Â· 359 insertions across 10062 reference words.<br>`#diagnostics > details:nth-of-type(1) > p:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 364 | #experiments · : de â†’ del (6) Â· caza â†’ casa (6) Â· de â†’ en (5) Â· ello â†’ ellos (5) Â· del â†’ la (5)<br>`#diagnostics > details:nth-of-type(1) > p:nth-of-type(2)` | text: pass 6.728:1 (needs 4.5:1) |
| 365 | #experiments · substitutions<br>`#diagnostics > details:nth-of-type(1) > p:nth-of-type(2) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 366 | #experiments · : de (17) Â· a (17) Â· en (6) Â· la (5) Â· al (4)<br>`#diagnostics > details:nth-of-type(1) > p:nth-of-type(3)` | text: pass 6.728:1 (needs 4.5:1) |
| 367 | #experiments · deletions<br>`#diagnostics > details:nth-of-type(1) > p:nth-of-type(3) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 368 | #experiments · : de (28) Â· a (23) Â· en (13) Â· y (12) Â· me (7)<br>`#diagnostics > details:nth-of-type(1) > p:nth-of-type(4)` | text: pass 6.728:1 (needs 4.5:1) |
| 369 | #experiments · insertions<br>`#diagnostics > details:nth-of-type(1) > p:nth-of-type(4) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 370 | #experiments · condition:read speech Â· 407 clips Â· WER 20.8% Â· CER 6.5%<br>`#diagnostics > details:nth-of-type(1) > p:nth-of-type(5)` | text: pass 6.728:1 (needs 4.5:1) |
| 371 | #experiments · E1 Â· Full fine-tuning<br>`#diagnostics > details:nth-of-type(2) > summary:nth-of-type(1)` | text: pass 8.123:1 (needs 4.5:1); control: pass 630.8×28 px |
| 372 | #experiments · 1531 substitutions Â· 156 deletions Â· 417 insertions across 10062 reference words.<br>`#diagnostics > details:nth-of-type(2) > p:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 373 | #experiments · : una â†’ un (7) Â· caza â†’ casa (6) Â· al â†’ el (5) Â· polo â†’ pueblo (4) Â· vÃ­ctima â†’ vÃ­ctimas (3)<br>`#diagnostics > details:nth-of-type(2) > p:nth-of-type(2)` | text: pass 6.728:1 (needs 4.5:1) |
| 374 | #experiments · substitutions<br>`#diagnostics > details:nth-of-type(2) > p:nth-of-type(2) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 375 | #experiments · : a (19) Â· de (14) Â· en (7) Â· la (4) Â· antigua (4)<br>`#diagnostics > details:nth-of-type(2) > p:nth-of-type(3)` | text: pass 6.728:1 (needs 4.5:1) |
| 376 | #experiments · deletions<br>`#diagnostics > details:nth-of-type(2) > p:nth-of-type(3) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 377 | #experiments · : de (37) Â· a (30) Â· en (19) Â· y (15) Â· se (10)<br>`#diagnostics > details:nth-of-type(2) > p:nth-of-type(4)` | text: pass 6.728:1 (needs 4.5:1) |
| 378 | #experiments · insertions<br>`#diagnostics > details:nth-of-type(2) > p:nth-of-type(4) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 379 | #experiments · Best checkpoint: epoch 1. Successful optimizer updates: 1050. Skipped updates: 0.<br>`#diagnostics > details:nth-of-type(2) > p:nth-of-type(5)` | text: pass 6.728:1 (needs 4.5:1) |
| 380 | #experiments · EPOCH<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(1)` | text: pass 5.954:1 (needs 4.5:1) |
| 381 | #experiments · TRAIN LOSS<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(2)` | text: pass 5.954:1 (needs 4.5:1) |
| 382 | #experiments · VALIDATION WER<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(3)` | text: pass 5.954:1 (needs 4.5:1) |
| 383 | #experiments · VALIDATION CER<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(4)` | text: pass 5.954:1 (needs 4.5:1) |
| 384 | #experiments · 1<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1)` | text: pass 6.905:1 (needs 4.5:1) |
| 385 | #experiments · 1.878<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 386 | #experiments · 20.9%<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(3)` | text: pass 6.905:1 (needs 4.5:1) |
| 387 | #experiments · 6.7%<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 388 | #experiments · 2<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(1)` | text: pass 6.905:1 (needs 4.5:1) |
| 389 | #experiments · 1.145<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 390 | #experiments · 21.3%<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(3)` | text: pass 6.905:1 (needs 4.5:1) |
| 391 | #experiments · 7.0%<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 392 | #experiments · 3<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(1)` | text: pass 6.905:1 (needs 4.5:1) |
| 393 | #experiments · 0.898<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 394 | #experiments · 21.2%<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(3)` | text: pass 6.905:1 (needs 4.5:1) |
| 395 | #experiments · 7.1%<br>`#diagnostics > details:nth-of-type(2) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 396 | #experiments · condition:read speech Â· 407 clips Â· WER 20.9% Â· CER 6.7%<br>`#diagnostics > details:nth-of-type(2) > p:nth-of-type(6)` | text: pass 6.728:1 (needs 4.5:1) |
| 397 | #experiments · E2 Â· LoRA fine-tuning<br>`#diagnostics > details:nth-of-type(3) > summary:nth-of-type(1)` | text: pass 8.123:1 (needs 4.5:1); control: pass 630.8×28 px |
| 398 | #experiments · 1581 substitutions Â· 156 deletions Â· 433 insertions across 10062 reference words.<br>`#diagnostics > details:nth-of-type(3) > p:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 399 | #experiments · : caza â†’ casa (6) Â· al â†’ el (6) Â· de â†’ del (5) Â· del â†’ el (5) Â· una â†’ un (5)<br>`#diagnostics > details:nth-of-type(3) > p:nth-of-type(2)` | text: pass 6.728:1 (needs 4.5:1) |
| 400 | #experiments · substitutions<br>`#diagnostics > details:nth-of-type(3) > p:nth-of-type(2) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 401 | #experiments · : a (17) Â· de (9) Â· en (7) Â· la (5) Â· al (4)<br>`#diagnostics > details:nth-of-type(3) > p:nth-of-type(3)` | text: pass 6.728:1 (needs 4.5:1) |
| 402 | #experiments · deletions<br>`#diagnostics > details:nth-of-type(3) > p:nth-of-type(3) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 403 | #experiments · : de (38) Â· a (36) Â· en (17) Â· y (13) Â· la (5)<br>`#diagnostics > details:nth-of-type(3) > p:nth-of-type(4)` | text: pass 6.728:1 (needs 4.5:1) |
| 404 | #experiments · insertions<br>`#diagnostics > details:nth-of-type(3) > p:nth-of-type(4) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 405 | #experiments · Best checkpoint: epoch 3. Successful optimizer updates: 1750. Skipped updates: 0.<br>`#diagnostics > details:nth-of-type(3) > p:nth-of-type(5)` | text: pass 6.728:1 (needs 4.5:1) |
| 406 | #experiments · EPOCH<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(1)` | text: pass 5.954:1 (needs 4.5:1) |
| 407 | #experiments · TRAIN LOSS<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(2)` | text: pass 5.954:1 (needs 4.5:1) |
| 408 | #experiments · VALIDATION WER<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(3)` | text: pass 5.954:1 (needs 4.5:1) |
| 409 | #experiments · VALIDATION CER<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(4)` | text: pass 5.954:1 (needs 4.5:1) |
| 410 | #experiments · 1<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1)` | text: pass 6.905:1 (needs 4.5:1) |
| 411 | #experiments · 2.244<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 412 | #experiments · 168.9%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(3)` | text: pass 6.905:1 (needs 4.5:1) |
| 413 | #experiments · 92.5%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 414 | #experiments · 2<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(1)` | text: pass 6.905:1 (needs 4.5:1) |
| 415 | #experiments · 1.736<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 416 | #experiments · 51.7%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(3)` | text: pass 6.905:1 (needs 4.5:1) |
| 417 | #experiments · 22.4%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(2) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 418 | #experiments · 3<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(1)` | text: pass 6.905:1 (needs 4.5:1) |
| 419 | #experiments · 1.555<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 420 | #experiments · 21.6%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(3)` | text: pass 6.905:1 (needs 4.5:1) |
| 421 | #experiments · 6.9%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(3) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 422 | #experiments · 4<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(1)` | text: pass 6.905:1 (needs 4.5:1) |
| 423 | #experiments · 1.476<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 424 | #experiments · 21.7%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(3)` | text: pass 6.905:1 (needs 4.5:1) |
| 425 | #experiments · 7.0%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(4) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 426 | #experiments · 5<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(1)` | text: pass 6.905:1 (needs 4.5:1) |
| 427 | #experiments · 1.453<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 428 | #experiments · 21.8%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(3)` | text: pass 6.905:1 (needs 4.5:1) |
| 429 | #experiments · 7.0%<br>`#diagnostics > details:nth-of-type(3) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(5) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 430 | #experiments · condition:read speech Â· 407 clips Â· WER 21.6% Â· CER 6.9%<br>`#diagnostics > details:nth-of-type(3) > p:nth-of-type(6)` | text: pass 6.728:1 (needs 4.5:1) |
| 431 | #experiments · E4 Â· LoRA + augmentation<br>`#diagnostics > details:nth-of-type(4) > summary:nth-of-type(1)` | text: pass 8.123:1 (needs 4.5:1); control: pass 630.8×28 px |
| 432 | #experiments · Best checkpoint: epoch 1. Successful optimizer updates: 350. Skipped updates: 0.<br>`#diagnostics > details:nth-of-type(4) > p:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 433 | #experiments · EPOCH<br>`#diagnostics > details:nth-of-type(4) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(1)` | text: pass 5.954:1 (needs 4.5:1) |
| 434 | #experiments · TRAIN LOSS<br>`#diagnostics > details:nth-of-type(4) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(2)` | text: pass 5.954:1 (needs 4.5:1) |
| 435 | #experiments · VALIDATION WER<br>`#diagnostics > details:nth-of-type(4) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(3)` | text: pass 5.954:1 (needs 4.5:1) |
| 436 | #experiments · VALIDATION CER<br>`#diagnostics > details:nth-of-type(4) > div:nth-of-type(1) > table:nth-of-type(1) > thead:nth-of-type(1) > tr:nth-of-type(1) > th:nth-of-type(4)` | text: pass 5.954:1 (needs 4.5:1) |
| 437 | #experiments · 1<br>`#diagnostics > details:nth-of-type(4) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1)` | text: pass 6.905:1 (needs 4.5:1) |
| 438 | #experiments · 2.302<br>`#diagnostics > details:nth-of-type(4) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(2)` | text: pass 6.905:1 (needs 4.5:1) |
| 439 | #experiments · 179.6%<br>`#diagnostics > details:nth-of-type(4) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(3)` | text: pass 6.905:1 (needs 4.5:1) |
| 440 | #experiments · 98.6%<br>`#diagnostics > details:nth-of-type(4) > div:nth-of-type(1) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(4)` | text: pass 6.905:1 (needs 4.5:1) |
| 441 | #experiments · Validation word error rate. Epoch 1: 20.9 percent. Epoch 2: 21.3 percent. Epoch 3: 21.2 percent. Lower is better.<br>`[role=img] measured graphic 1` | graphic-label: pass |
| 442 | #experiments · Validation word error rate. Epoch 1: 168.9 percent. Epoch 2: 51.7 percent. Epoch 3: 21.6 percent. Epoch 4: 21.7 percent. Epoch 5: 21.8 percent. Lower is better.<br>`[role=img] measured graphic 2` | graphic-label: pass |
| 443 | #experiments · Validation word error rate. Epoch 1: 179.6 percent. Epoch 2: 191.6 percent. Lower is better.<br>`[role=img] measured graphic 3` | graphic-label: pass |
| 444 | #dataset · Skip to main content<br>`a:nth-of-type(1)` | text: pass 16.009:1 (needs 4.5:1); control: pass 190.1×46.5 px |
| 445 | #dataset · LocalVoice<br>`aside:nth-of-type(1) > a:nth-of-type(1)` | text: pass 15.836:1 (needs 3:1); control: pass 686.4×37.5 px |
| 446 | #dataset · .<br>`aside:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(2)` | text: pass 12.615:1 (needs 3:1) |
| 447 | #dataset · Overview<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1)` | text: pass 10.013:1 (needs 4.5:1); control: pass 97.2×44 px |
| 448 | #dataset · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 449 | #dataset · Speech playground<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2)` | text: pass 10.013:1 (needs 4.5:1); control: pass 148.3×44 px |
| 450 | #dataset · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 451 | #dataset · Experiments<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3)` | text: pass 10.013:1 (needs 4.5:1); control: pass 113.7×44 px |
| 452 | #dataset · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 453 | #dataset · Dataset<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4)` | text: pass 10.755:1 (needs 4.5:1); control: pass 92.1×44 px |
| 454 | #dataset · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 455 | #dataset · Research report<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5)` | text: pass 10.013:1 (needs 4.5:1); control: pass 131.5×44 px |
| 456 | #dataset · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 457 | #dataset · Workspace<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.903:1 (needs 4.5:1) |
| 458 | #dataset · /<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.069:1 (needs 4.5:1) |
| 459 | #dataset · Dataset<br>`#breadcrumb` | text: pass 11.932:1 (needs 4.5:1) |
| 460 | #dataset · Local environment<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.073:1 (needs 4.5:1) |
| 461 | #dataset · THE FOUNDATION<br>`#page-dataset > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.81:1 (needs 4.5:1) |
| 462 | #dataset · Better models start with data<br>`#page-dataset > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1)` | text: pass 14.337:1 (needs 3:1) |
| 463 | #dataset · .<br>`#page-dataset > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1) > span:nth-of-type(1)` | text: pass 5.65:1 (needs 3:1) |
| 464 | #dataset · Spanish speech, consistent transcripts, and auditable evaluation splits.<br>`#page-dataset > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.596:1 (needs 4.5:1) |
| 465 | #dataset · Google FLEURS Â· es_419<br>`#page-dataset > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6:1 (needs 4.5:1) |
| 466 | #dataset · Prepared clips<br>`#dataset-metrics > article:nth-of-type(1) > div:nth-of-type(1)` | text: pass 7.138:1 (needs 4.5:1) |
| 467 | #dataset · 4110<br>`#dataset-metrics > article:nth-of-type(1) > div:nth-of-type(2)` | text: pass 13.724:1 (needs 3:1) |
| 468 | #dataset · clips<br>`#dataset-metrics > article:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.075:1 (needs 4.5:1) |
| 469 | #dataset · Validated audioâ€“transcript pairs<br>`#dataset-metrics > article:nth-of-type(1) > div:nth-of-type(3)` | text: pass 6.409:1 (needs 4.5:1) |
| 470 | #dataset · Train split<br>`#dataset-metrics > article:nth-of-type(2) > div:nth-of-type(1)` | text: pass 5.992:1 (needs 4.5:1) |
| 471 | #dataset · 8.8<br>`#dataset-metrics > article:nth-of-type(2) > div:nth-of-type(2)` | text: pass 11.519:1 (needs 3:1) |
| 472 | #dataset · hours<br>`#dataset-metrics > article:nth-of-type(2) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 5.938:1 (needs 4.5:1) |
| 473 | #dataset · 2796 clips<br>`#dataset-metrics > article:nth-of-type(2) > div:nth-of-type(3)` | text: pass 5.379:1 (needs 4.5:1) |
| 474 | #dataset · Validation split<br>`#dataset-metrics > article:nth-of-type(3) > div:nth-of-type(1)` | text: pass 7.138:1 (needs 4.5:1) |
| 475 | #dataset · 1.3<br>`#dataset-metrics > article:nth-of-type(3) > div:nth-of-type(2)` | text: pass 13.724:1 (needs 3:1) |
| 476 | #dataset · hours<br>`#dataset-metrics > article:nth-of-type(3) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.075:1 (needs 4.5:1) |
| 477 | #dataset · 407 clips<br>`#dataset-metrics > article:nth-of-type(3) > div:nth-of-type(3)` | text: pass 6.409:1 (needs 4.5:1) |
| 478 | #dataset · Test split<br>`#dataset-metrics > article:nth-of-type(4) > div:nth-of-type(1)` | text: pass 5.972:1 (needs 4.5:1) |
| 479 | #dataset · 3.1<br>`#dataset-metrics > article:nth-of-type(4) > div:nth-of-type(2)` | text: pass 11.482:1 (needs 3:1) |
| 480 | #dataset · hours<br>`#dataset-metrics > article:nth-of-type(4) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 5.919:1 (needs 4.5:1) |
| 481 | #dataset · 907 clips<br>`#dataset-metrics > article:nth-of-type(4) > div:nth-of-type(3)` | text: pass 5.362:1 (needs 4.5:1) |
| 482 | #dataset · Dataset readiness<br>`#page-dataset > div:nth-of-type(3) > article:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 483 | #dataset · Manifest ready<br>`#dataset-details > p:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 11.623:1 (needs 4.5:1) |
| 484 | #dataset · Format: mono WAV Â· 16,000 Hz Â· clips up to 30 seconds. Transcript normalization: Unicode NFC, lowercase, punctuation removal, and collapsed whitespace.<br>`#dataset-details > p:nth-of-type(2)` | text: pass 6.728:1 (needs 4.5:1) |
| 485 | #dataset · Manifest fields: audio_path, transcript, speaker_id, split, duration_seconds.<br>`#dataset-details > p:nth-of-type(3)` | text: pass 6.728:1 (needs 4.5:1) |
| 486 | #dataset · Speaker IDs are missing: speaker independence cannot be verified.<br>`#dataset-details > div:nth-of-type(1)` | text: pass 6.495:1 (needs 4.5:1) |
| 487 | #dataset · License: CC-BY-4.0. FLEURS Â· Google, 2022. Speaker IDs may be unavailable; the report must disclose that speaker independence cannot be verified.<br>`#dataset-details > p:nth-of-type(4)` | text: pass 6.728:1 (needs 4.5:1) |
| 488 | #dataset · The dashboard checks manifest structure. Run   for the full audio and duplicate-content audit.<br>`#dataset-details > p:nth-of-type(5)` | text: pass 6.728:1 (needs 4.5:1) |
| 489 | #dataset · localvoice validate<br>`#dataset-details > p:nth-of-type(5) > code:nth-of-type(1)` | text: pass 7.538:1 (needs 4.5:1) |
| 490 | #dataset · Prepare the dataset<br>`#page-dataset > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 491 | #dataset · Download the official Spanish parquet exports and convert clips to mono 16 kHz WAV. Original splits are retained.<br>`#page-dataset > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(2) > p:nth-of-type(1)` | text: pass 6.728:1 (needs 4.5:1) |
| 492 | #dataset · .venv\Scripts\localvoice prepare .venv\Scripts\localvoice validate<br>`#page-dataset > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(2) > pre:nth-of-type(1)` | text: pass 7.535:1 (needs 4.5:1) |
| 493 | #dataset · FLEURS is read speech. Results will not establish performance on spontaneous speech or every Spanish dialect.<br>`#page-dataset > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(2) > p:nth-of-type(2)` | text: pass 6.728:1 (needs 4.5:1) |
| 494 | #dataset · View source & license â†—<br>`#page-dataset > div:nth-of-type(3) > article:nth-of-type(2) > div:nth-of-type(2) > a:nth-of-type(1)` | text: pass 7.019:1 (needs 4.5:1); control: pass 122.7×28 px |
| 495 | #report · Skip to main content<br>`a:nth-of-type(1)` | text: pass 16.009:1 (needs 4.5:1); control: pass 190.1×46.5 px |
| 496 | #report · LocalVoice<br>`aside:nth-of-type(1) > a:nth-of-type(1)` | text: pass 15.836:1 (needs 3:1); control: pass 686.4×37.5 px |
| 497 | #report · .<br>`aside:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(2)` | text: pass 12.615:1 (needs 3:1) |
| 498 | #report · Overview<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1)` | text: pass 10.013:1 (needs 4.5:1); control: pass 97.2×44 px |
| 499 | #report · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 500 | #report · Speech playground<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2)` | text: pass 10.013:1 (needs 4.5:1); control: pass 148.3×44 px |
| 501 | #report · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 502 | #report · Experiments<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3)` | text: pass 10.013:1 (needs 4.5:1); control: pass 113.7×44 px |
| 503 | #report · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 504 | #report · Dataset<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4)` | text: pass 10.013:1 (needs 4.5:1); control: pass 89.6×44 px |
| 505 | #report · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 506 | #report · Research report<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5)` | text: pass 10.755:1 (needs 4.5:1); control: pass 136.1×44 px |
| 507 | #report · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 508 | #report · Workspace<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.903:1 (needs 4.5:1) |
| 509 | #report · /<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.069:1 (needs 4.5:1) |
| 510 | #report · Research report<br>`#breadcrumb` | text: pass 11.932:1 (needs 4.5:1) |
| 511 | #report · Local environment<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.073:1 (needs 4.5:1) |
| 512 | #report · THE RESEARCH JOURNAL<br>`#page-report > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.81:1 (needs 4.5:1) |
| 513 | #report · Evidence behind every improvement<br>`#page-report > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1)` | text: pass 14.337:1 (needs 3:1) |
| 514 | #report · .<br>`#page-report > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1) > span:nth-of-type(1)` | text: pass 5.65:1 (needs 3:1) |
| 515 | #report · The decisions, methods, measured findings, and limitations behind this project.<br>`#page-report > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.596:1 (needs 4.5:1) |
| 516 | #report · Export evidence<br>`#page-report > div:nth-of-type(1) > a:nth-of-type(1)` | text: pass 11.259:1 (needs 4.5:1); control: pass 142.1×44 px |
| 517 | #report · Decorative icon paired with a text or named control<br>`#page-report > div:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 518 | #report · View the LocalVoice brand board â†—<br>`#page-report > p:nth-of-type(1) > a:nth-of-type(1)` | text: pass 6.286:1 (needs 4.5:1); control: pass 212.1×32 px |
| 519 | #report · Fine-tuning Spanish speech recognition with limited labeled data<br>`#report-content > h2:nth-of-type(1)` | text: pass 12.005:1 (needs 3:1) |
| 520 | #report · Objective<br>`#report-content > h3:nth-of-type(1)` | text: pass 9.659:1 (needs 4.5:1) |
| 521 | #report · Measure how full fine-tuning, LoRA, and speech augmentation change Spanish transcription accuracy and adaptation cost. Spanish is the target language; the low-resource condition is<br>`#report-content > p:nth-of-type(1)` | text: pass 7.199:1 (needs 4.5:1) |
| 522 | #report · Current evidence<br>`#report-content > h3:nth-of-type(2)` | text: pass 9.659:1 (needs 4.5:1) |
| 523 | #report · The Spanish experiment series uses its own dataset and run artifacts. Superseded results from the earlier language choice are archived and never compared with Spanish. Live results<br>`#report-content > p:nth-of-type(2)` | text: pass 7.199:1 (needs 4.5:1) |
| 524 | #report · Data and checkpoint<br>`#report-content > h3:nth-of-type(3)` | text: pass 9.659:1 (needs 4.5:1) |
| 525 | #report · Dataset: Google FLEURS, Latin American Spanish configuration  , licensed CC-BY-4.0. Official train, validation, and test splits are retained. Audio becomes mono 16 kHz WAV; empty o<br>`#report-content > p:nth-of-type(3)` | text: pass 7.199:1 (needs 4.5:1) |
| 526 | #report · es_419<br>`#report-content > p:nth-of-type(3) > code:nth-of-type(1)` | text: pass 7.538:1 (needs 4.5:1) |
| 527 | #report · Model: multilingual  , fixed repository revision  , Apache-2.0. Keeping the family, size, and revision fixed makes the initial strategy comparison interpretable. Tiny fits the avai<br>`#report-content > p:nth-of-type(4)` | text: pass 7.199:1 (needs 4.5:1) |
| 528 | #report · openai/whisper-tiny<br>`#report-content > p:nth-of-type(4) > code:nth-of-type(1)` | text: pass 7.538:1 (needs 4.5:1) |
| 529 | #report · 169d4a4341b33bc18d8881c4b69c2e104e1cc0af<br>`#report-content > p:nth-of-type(4) > code:nth-of-type(2)` | text: pass 7.538:1 (needs 4.5:1) |
| 530 | #report · Exact adaptation methods<br>`#report-content > h3:nth-of-type(4)` | text: pass 9.659:1 (needs 4.5:1) |
| 531 | #report · E0 is the untouched pretrained baseline. E1 updates all model parameters. E2 freezes the base weights and trains rank-eight LoRA updates on query and value projections ( ,  ), alph<br>`#report-content > p:nth-of-type(5)` | text: pass 7.199:1 (needs 4.5:1) |
| 532 | #report · q_proj<br>`#report-content > p:nth-of-type(5) > code:nth-of-type(1)` | text: pass 7.538:1 (needs 4.5:1) |
| 533 | #report · v_proj<br>`#report-content > p:nth-of-type(5) > code:nth-of-type(2)` | text: pass 7.538:1 (needs 4.5:1) |
| 534 | #report · Every tuned run has a maximum five-epoch budget, batch size eight, one gradient accumulation step, seed 42, AdamW, weight decay 0.01, gradient clipping 1.0, 10% warmup, and linear <br>`#report-content > p:nth-of-type(6)` | text: pass 7.199:1 (needs 4.5:1) |
| 535 | #report · CUDA uses bfloat16 when supported, otherwise scaled float16, with gradient checkpointing. Successful and skipped updates are counted. Non-finite loss stops training. Unaugmented fe<br>`#report-content > p:nth-of-type(7)` | text: pass 7.199:1 (needs 4.5:1) |
| 536 | #report · Augmentation and text handling<br>`#report-content > h3:nth-of-type(5)` | text: pass 9.659:1 (needs 4.5:1) |
| 537 | #report · Training-only speed perturbation samples 0.95â€“1.05; additive Gaussian noise samples 20â€“35 dB SNR. Clips near thirty seconds are not slowed past the model context limit, avoidin<br>`#report-content > p:nth-of-type(8)` | text: pass 7.199:1 (needs 4.5:1) |
| 538 | #report · All references and predictions share Unicode NFC, lowercase, Unicode punctuation removal, and whitespace normalization. Spanish accents and Ã± are preserved. Generation is fixed at<br>`#report-content > p:nth-of-type(9)` | text: pass 7.199:1 (needs 4.5:1) |
| 539 | #report · What is compared<br>`#report-content > h3:nth-of-type(6)` | text: pass 9.659:1 (needs 4.5:1) |
| 540 | #report · E1 versus E0 measures full adaptation. E2 versus E0 measures adapter adaptation. E3 versus E1 and E4 versus E2 measure augmentation under each strategy. E2 versus E1 and E4 versus <br>`#report-content > p:nth-of-type(10)` | text: pass 7.199:1 (needs 4.5:1) |
| 541 | #report · WER and CER are computed using JiWER. Absolute WER reduction is baseline minus tuned WER in percentage points. Relative reduction divides that difference by baseline WER; it is und<br>`#report-content > p:nth-of-type(11)` | text: pass 7.199:1 (needs 4.5:1) |
| 542 | #report · Cost includes training wall time, peak PyTorch GPU allocation, trainable weights, and warmed generation latency. Peak allocation is not total board memory. Baseline trainable param<br>`#report-content > p:nth-of-type(12)` | text: pass 7.199:1 (needs 4.5:1) |
| 543 | #report · Checkpoint and test policy<br>`#report-content > h3:nth-of-type(7)` | text: pass 9.659:1 (needs 4.5:1) |
| 544 | #report · Checkpoints are independently loadable full models or LoRA adapters with their processor files. The experiment series evaluates only validation data. The held-out test set requires<br>`#report-content > p:nth-of-type(13)` | text: pass 7.199:1 (needs 4.5:1) |
| 545 | #report · --split test --final-test<br>`#report-content > p:nth-of-type(13) > code:nth-of-type(1)` | text: pass 7.538:1 (needs 4.5:1) |
| 546 | #report · Artifacts and progress<br>`#report-content > h3:nth-of-type(8)` | text: pass 9.659:1 (needs 4.5:1) |
| 547 | #report · Each run retains  ,  ,  ,  ,  , and   as applicable. The website shows optimizer updates, training loss, validation curves, selected epochs, recognition errors, baseline difference<br>`#report-content > p:nth-of-type(14)` | text: pass 7.199:1 (needs 4.5:1) |
| 548 | #report · training.json<br>`#report-content > p:nth-of-type(14) > code:nth-of-type(1)` | text: pass 7.538:1 (needs 4.5:1) |
| 549 | #report · progress.json<br>`#report-content > p:nth-of-type(14) > code:nth-of-type(2)` | text: pass 7.538:1 (needs 4.5:1) |
| 550 | #report · history.json<br>`#report-content > p:nth-of-type(14) > code:nth-of-type(3)` | text: pass 7.538:1 (needs 4.5:1) |
| 551 | #report · checkpoint/<br>`#report-content > p:nth-of-type(14) > code:nth-of-type(4)` | text: pass 7.538:1 (needs 4.5:1) |
| 552 | #report · metrics-validation.json<br>`#report-content > p:nth-of-type(14) > code:nth-of-type(5)` | text: pass 7.538:1 (needs 4.5:1) |
| 553 | #report · predictions-validation.json<br>`#report-content > p:nth-of-type(14) > code:nth-of-type(6)` | text: pass 7.538:1 (needs 4.5:1) |
| 554 | #report · Limitations<br>`#report-content > h3:nth-of-type(9)` | text: pass 9.659:1 (needs 4.5:1) |
| 555 | #report · FLEURS is read speech; results do not establish conversational or dialect-wide Spanish performance.<br>`#report-content > ul:nth-of-type(1) > li:nth-of-type(1)` | text: pass 7.199:1 (needs 4.5:1) |
| 556 | #report · Missing speaker IDs prevent an independent audit of speaker separation.<br>`#report-content > ul:nth-of-type(1) > li:nth-of-type(2)` | text: pass 7.199:1 (needs 4.5:1) |
| 557 | #report · One seed and one model size support an initial controlled study, not a universal ranking.<br>`#report-content > ul:nth-of-type(1) > li:nth-of-type(3)` | text: pass 7.199:1 (needs 4.5:1) |
| 558 | #report · Augmentation and LoRA can worsen accuracy; all measured outcomes must be reported.<br>`#report-content > ul:nth-of-type(1) > li:nth-of-type(4)` | text: pass 7.199:1 (needs 4.5:1) |
| 559 | #report · Training-set playground clips are diagnostic and cannot support evaluation claims.<br>`#report-content > ul:nth-of-type(1) > li:nth-of-type(5)` | text: pass 7.199:1 (needs 4.5:1) |
| 560 | #report · Sources<br>`#report-content > h3:nth-of-type(10)` | text: pass 9.659:1 (needs 4.5:1) |
| 561 | #report · ,  ,  , and  .<br>`#report-content > p:nth-of-type(15)` | text: pass 7.199:1 (needs 4.5:1) |
| 562 | #report · FLEURS dataset and license<br>`#report-content > p:nth-of-type(15) > a:nth-of-type(1)` | text: pass 7.019:1 (needs 4.5:1); control: pass 179×17.6 px; Inline prose link target exception |
| 563 | #report · Whisper Tiny<br>`#report-content > p:nth-of-type(15) > a:nth-of-type(2)` | text: pass 7.019:1 (needs 4.5:1); control: pass 83.6×17.6 px; Inline prose link target exception |
| 564 | #report · Whisper fine-tuning guide<br>`#report-content > p:nth-of-type(15) > a:nth-of-type(3)` | text: pass 7.019:1 (needs 4.5:1); control: pass 169.5×17.6 px; Inline prose link target exception |
| 565 | #report · PEFT LoRA<br>`#report-content > p:nth-of-type(15) > a:nth-of-type(4)` | text: pass 7.019:1 (needs 4.5:1); control: pass 68.1×17.6 px; Inline prose link target exception |
| 566 | #report · ## Current local results<br>`#report-content > p:nth-of-type(16)` | text: pass 7.199:1 (needs 4.5:1) |
| 567 | #report · E0 Â· Pretrained baseline: WER 20.79%, CER 6.50%, 407 clips on the validation split.<br>`#report-content > ul:nth-of-type(2) > li:nth-of-type(1)` | text: pass 7.199:1 (needs 4.5:1) |
| 568 | #report · E1 Â· Full fine-tuning: WER 20.91%, CER 6.71%, 407 clips on the validation split.<br>`#report-content > ul:nth-of-type(2) > li:nth-of-type(2)` | text: pass 7.199:1 (needs 4.5:1) |
| 569 | #report · E2 Â· LoRA fine-tuning: WER 21.57%, CER 6.90%, 407 clips on the validation split.<br>`#report-content > ul:nth-of-type(2) > li:nth-of-type(3)` | text: pass 7.199:1 (needs 4.5:1) |
| 570 | #playground:record · Skip to main content<br>`a:nth-of-type(1)` | text: pass 16.009:1 (needs 4.5:1); control: pass 190.1×46.5 px |
| 571 | #playground:record · LocalVoice<br>`aside:nth-of-type(1) > a:nth-of-type(1)` | text: pass 15.836:1 (needs 3:1); control: pass 339.2×37.5 px |
| 572 | #playground:record · .<br>`aside:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(2)` | text: pass 12.615:1 (needs 3:1) |
| 573 | #playground:record · Overview<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1)` | text: pass 10.013:1 (needs 4.5:1); control: pass 97.2×44 px |
| 574 | #playground:record · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 575 | #playground:record · Speech playground<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2)` | text: pass 10.755:1 (needs 4.5:1); control: pass 153.4×44 px |
| 576 | #playground:record · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 577 | #playground:record · Experiments<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3)` | text: pass 10.013:1 (needs 4.5:1); control: pass 113.7×44 px |
| 578 | #playground:record · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(3) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 579 | #playground:record · Dataset<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4)` | text: pass 10.013:1 (needs 4.5:1); control: pass 89.6×44 px |
| 580 | #playground:record · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(4) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 581 | #playground:record · Research report<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5)` | text: pass 10.013:1 (needs 4.5:1); control: pass 131.5×44 px |
| 582 | #playground:record · Decorative icon paired with a text or named control<br>`aside:nth-of-type(1) > nav:nth-of-type(1) > a:nth-of-type(5) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 583 | #playground:record · Workspace<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.903:1 (needs 4.5:1) |
| 584 | #playground:record · /<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1)` | text: pass 6.069:1 (needs 4.5:1) |
| 585 | #playground:record · Speech playground<br>`#breadcrumb` | text: pass 11.932:1 (needs 4.5:1) |
| 586 | #playground:record · Local environment<br>`div:nth-of-type(1) > header:nth-of-type(1) > div:nth-of-type(2) > span:nth-of-type(1)` | text: pass 7.073:1 (needs 4.5:1) |
| 587 | #playground:record · LISTEN. TRANSCRIBE. COMPARE.<br>`#page-playground > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1)` | text: pass 5.81:1 (needs 4.5:1) |
| 588 | #playground:record · Speech playground<br>`#page-playground > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1)` | text: pass 14.337:1 (needs 3:1) |
| 589 | #playground:record · .<br>`#page-playground > div:nth-of-type(1) > div:nth-of-type(1) > h1:nth-of-type(1) > span:nth-of-type(1)` | text: pass 5.65:1 (needs 3:1) |
| 590 | #playground:record · Hear what your model can do. Compare the same clip across experiments.<br>`#page-playground > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.596:1 (needs 4.5:1) |
| 591 | #playground:record · Give your voice a place<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 592 | #playground:record · Decorative icon paired with a text or named control<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > div:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 593 | #playground:record · Upload audio<br>`#upload-tab` | text: pass 5.261:1 (needs 4.5:1); control: pass 138.3×41 px |
| 594 | #playground:record · Record speech<br>`#record-tab` | text: pass 10.019:1 (needs 4.5:1); control: pass 138.3×41 px |
| 595 | #playground:record · Start recording<br>`#record-button` | control: pass 60×60 px |
| 596 | #playground:record · Record audio<br>`#record-button > span:nth-of-type(1) > svg:nth-of-type(1)` | meaningful-icon: pass 6.747:1 (needs 3:1) |
| 597 | #playground:record · Your voice, in your language<br>`#record-label` | text: pass 7.828:1 (needs 4.5:1) |
| 598 | #playground:record · Press to record. Press again to stop.<br>`#record-pane > div:nth-of-type(1) > small:nth-of-type(1)` | text: pass 5.345:1 (needs 4.5:1) |
| 599 | #playground:record · 00:00 / 00:30<br>`#record-timer` | text: pass 5.345:1 (needs 4.5:1) |
| 600 | #playground:record · Try a Spanish dataset sample<br>`#sample-button` | text: pass 6.545:1 (needs 4.5:1); control: pass 291.6×44 px |
| 601 | #playground:record · â†—<br>`#sample-button > span:nth-of-type(1)` | text: pass 6.545:1 (needs 4.5:1) |
| 602 | #playground:record · Model to test<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > label:nth-of-type(1)` | text: pass 8.872:1 (needs 4.5:1) |
| 603 | #playground:record · Model to test<br>`#model-select` | control: pass 291.6×48 px; non-text: pass 6.199:1 (needs 3:1) |
| 604 | #playground:record · Compare with pretrained baseline<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > label:nth-of-type(2)` | text: pass 7.524:1 (needs 4.5:1) |
| 605 | #playground:record · Compare with pretrained baseline<br>`#compare-models` | control: pass 24×24 px |
| 606 | #playground:record · Reference transcript<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > label:nth-of-type(3)` | text: pass 8.872:1 (needs 4.5:1) |
| 607 | #playground:record · optional<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > label:nth-of-type(3) > span:nth-of-type(1)` | text: pass 5.392:1 (needs 4.5:1) |
| 608 | #playground:record · Reference transcript optional<br>`#reference` | control: pass 291.6×116.8 px; non-text: pass 6.199:1 (needs 3:1) |
| 609 | #playground:record · Use the exact Spanish words spoken in the clip. Accents and Ã± are preserved.<br>`#reference-hint` | text: pass 6.441:1 (needs 4.5:1) |
| 610 | #playground:record · Transcribe audio<br>`#transcribe-button` | text: pass 6.309:1 (needs 4.5:1); control: pass 291.6×44 px |
| 611 | #playground:record · Decorative icon paired with a text or named control<br>`#transcribe-button > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 612 | #playground:record · Audio stays on this machine. Models download on first use.<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > p:nth-of-type(2)` | text: pass 6.441:1 (needs 4.5:1) |
| 613 | #playground:record · Decorative icon paired with a text or named control<br>`#page-playground > div:nth-of-type(2) > article:nth-of-type(1) > p:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 614 | #playground:record · The words behind the sound<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > h2:nth-of-type(1)` | text: pass 12.997:1 (needs 4.5:1) |
| 615 | #playground:record · Your transcription will appear here<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 6.258:1 (needs 4.5:1) |
| 616 | #playground:record · Copy transcript<br>`#copy-transcript` | control: pass 44×44 px |
| 617 | #playground:record · Copy transcript<br>`#copy-transcript > span:nth-of-type(1) > svg:nth-of-type(1)` | meaningful-icon: pass 6.409:1 (needs 3:1) |
| 618 | #playground:record · Decorative icon paired with a text or named control<br>`#transcript-results > div:nth-of-type(1) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 619 | #playground:record · Ready when you are.<br>`#transcript-results > div:nth-of-type(1) > h3:nth-of-type(1)` | text: pass 7.299:1 (needs 4.5:1) |
| 620 | #playground:record · Upload or record a clip, select a model, and turn speech into something you can study.<br>`#transcript-results > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.41:1 (needs 4.5:1) |
| 621 | #playground:record · Decorative icon paired with a text or named control<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(2) > span:nth-of-type(1) > svg:nth-of-type(1)` | decorative-icon: decorative |
| 622 | #playground:record · A playground is a starting point.<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(2) > div:nth-of-type(1) > strong:nth-of-type(1)` | text: pass 6.875:1 (needs 4.5:1) |
| 623 | #playground:record · Single-clip scores help inspect errors. Use the fixed evaluation split to make research claims. Model loading and inference time are reported separately.<br>`#page-playground > div:nth-of-type(2) > div:nth-of-type(1) > article:nth-of-type(2) > div:nth-of-type(1) > p:nth-of-type(1)` | text: pass 5.206:1 (needs 4.5:1) |

## Resolved findings

| Element | Before | After |
| --- | --- | --- |
| Baseline bar on white | 2.921:1 | 6.199:1 |
| Select/textarea boundary on white | 1.547:1 | 6.199:1 |
| Sidebar focus outline on dark surface | 2.678:1 | 12.615:1 |

Heading hierarchy, form descriptions, invalid-field ownership, actionable microphone feedback, dismissible notifications, 16px mobile inputs, and reduced-motion behavior were also inspected and improved. Record tab keyboard selection was exercised without granting microphone permission. Spanish text retains its language metadata.

## Standing runtime advisories

1. Screen-reader speech output, operating-system zoom, and forced-colors rendering were not exercised; semantics and forced-colors CSS were inspected.
2. Microphone capture and permission-denial paths were reviewed in source; no microphone permission was granted for this audit.
3. Completed transcription was not repeated while the training matrix held the GPU. The busy state and its explanation were reviewed.

Evidence: `accessibility-inventory.json`, `accessibility-additional-checks.json`, and `../community-review-preview.png`. The board is a separate presentation artifact, outside the product-UI element inventory.
