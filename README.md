# ligmafinder

Finds Unicode characters that normalize to ASCII according to PEP 3131.

## Usage

Basic compilation:
```bash
python ligmafinder.py flag

[+] Compiling: 'flag'

    |ﬂªᵍ|	(3 chars)

────────────────────────────────────────
Generated 1 candidates for 'flag'
```

Compile with multiple candidates:
```bash
python ligmafinder.py -m 5 'print(flag)'
```

Get all possible candidates:
```bash
python ligmafinder.py --all flag
```

Disable greedy mode (strict char-by-char):
```bash
python ligmafinder.py --no-greedy 'print(flag)'
```

View available Unicode variants:
```bash
python ligmafinder.py --table
python ligmafinder.py --lookup
```

Check available slices for a word:
```bash
python ligmafinder.py --slices flag
```
