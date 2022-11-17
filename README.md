# Requirements

python3 with the dependency `dolphin-memory-engine`

`pip install --user dolphin-memory-engine`

# Usage

```bash
./loaded_rels.py list
./loaded_rels.py 80f3f438
```

# additional stuff for linux

```bash
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
sudo setcap CAP_SYS_PTRACE=+ep heap_info.py
```
