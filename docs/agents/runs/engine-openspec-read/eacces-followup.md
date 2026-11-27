# I2 post-preflight scan EACCES — supplemental verification

Run engine-openspec-read, supplement to verify-i2-04, not a new role invocation. Tested Engine snapshot `09f59c1940f0eb08f658c9b02a99054afa5a85b153bb644830a8bfd089385d47` via `/tmp/i2-verify-final-04/debug/pentapro`; upstream pinned OpenSpec v2.2.0 f1cd852f4edce22b8df9548a4df889172ca8ff25, Node 26.10.0, Linux UID 1000.

Constructed separate equivalent synthetic project/HOME trees under a temporary parent; each `openspec/specs` had mode 0111. Direct metadata lookup of `.openspec-store` returned ENOENT (errno 2), while readdir returned EACCES (errno 13) in each tree. This establishes the sought effective permission distinction, under this user and filesystem. Both tools ran without interactive input, with isolated HOME/XDG and telemetry/update disabled; temporary fixture-parent prefixes alone were normalized.

All four actual commands produced identical exit/stdout/stderr for Engine and upstream:

- `list --specs`: exit 1, empty stdout, stderr `✖ Error: EACCES: permission denied, scandir '<ROOT>/project/openspec/specs'` followed by LF.
- `list --specs --json`: exit 1, JSON stdout with empty `specs`, null `root`, severity `error`, code `list_error` and the same scandir message; stderr empty.
- `show alpha --type spec`: exit 1, empty stdout and same human diagnostic on stderr.
- `show alpha --type spec --json`: exit 1, JSON stdout with severity `error`, code `show_error` and the same scandir message; stderr empty.

The first attempted one-off probe had a Python syntax error and executed no fixture operations; the corrected probe produced the observations above. Permissions were restored in a finally block before temporary cleanup. No project source/index mutation occurred. The fixture establishes this branch only for Linux UID 1000 on this filesystem; it does not establish other OS/permissions, race-free containment or complete OpenSpec parity.
