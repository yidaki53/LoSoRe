import pathlib, re, os
rec = pathlib.Path('reports/overnight3/recon')
files = list(rec.glob('*.c'))
print('recon files:', len(files))
vers = {}
bad = []
for p in files:
    t = p.read_text()
    m = re.search(r'Dual-judge: qwen=(\S+) phi=(\S+) verdict=(\S+)', t)
    if m:
        vers[m.group(3)] = vers.get(m.group(3), 0) + 1
    else:
        bad.append(p.name)
print('verdicts:', vers)
print('unparsed:', len(bad), bad[:5])
cov = sum(1 for p in files
          if os.path.exists('targets/liero-dos/decomp/' + p.stem + '.c'))
print('with ghidra decomp:', cov)
