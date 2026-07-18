# Local runtime

This workspace runs on Windows 10, where Codex Workspace dependencies are not
available. Use the locally installed runtimes exposed on `PATH` instead:

- Python: `python` (currently Python 3.12)
- Node.js: `node` (currently Node.js 20)

Before running Python or Node-based work, verify the relevant runtime with
`python --version` or `node --version`. Do not attempt to install or reset
Codex Workspace dependencies for this repository.

Run Python tests with `python -m pytest` when the task includes tests.
