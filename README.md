# DiscordBot
Test for discord bot make with python
# How to run
## The easy way:
1 Install uv:
```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```
```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

  Or, from [PyPI](https://pypi.org/project/uv/):

```bash
# With pip.
pip install uv
```

```bash
# Or pipx.
pipx install uv
```

If installed via the standalone installer, uv can update itself to the latest version:

```bash
uv self
```
2 Clone the repo:
```bash
git clone https://github.com/qwertytuan/DiscordBot && cd DiscordBot
```
Edit the [.env_example](.env_example)
Then run:
```bash
uv sync && uv run main.py
```
## The hard way
Run
```bash
pip3 install -r requirements.txt
```
Then run
```bash
python3 main.py
```
