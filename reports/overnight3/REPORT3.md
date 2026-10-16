# Night-3 report: The Libre Reconstruction
Generated 2026-10-16 00:56:30 after 175 min.
Artifact: reports/overnight3/recon/ (machine-reconstructed clean C with provenance headers).

## G1 mass generation
# G1 mass generation
- candidates: 588, compiles: 370

## G2 dual-judge
# G2 dual-judge audit
- candidates judged: 370
- real: 256  contested: 18  junk: 90  error: 6
- distill dataset (>= 80 needed): 256

## G3 distill
# g3 distilled (r=16, 5ep, verified targets)
- panel: strict 26/60, any-compile 26/60
- dataset: 197 judge-verified pairs

## G4 corpus
# G4 corpus
- emitted 235 files to recon/
- verdicts: {'contested': 7, 'judge-error': 1, 'real': 64, 'not-judged': 138, 'junk': 25}

## Verdict on the distillation hypothesis
- corpus size: 235/294, verdicts: {'contested': 7, 'judge-error': 1, 'real': 64, 'not-judged': 138, 'junk': 25}
- Night-2 F3 said ~2/3 of the small model's compiles were junk when trained on Ghidra pseudocode. G3 retrains it on judge-verified clean C instead; G4's judge sample is the answer.
- Compile != semantics remains: only dual-agreement 'real' verdicts count as preserved source.
