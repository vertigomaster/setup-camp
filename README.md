# Disclaimer
This VERY simple personal utility assumes you already have the following installed and accessible from your PATH env:
- Git
- GitHub CLI
- Python (3)

So far this has only been tested on Windows 11 (specifically in cmd and Git Bash), 
but the setup-camp file is written in .sh syntax that SHOULD work on Mac/Linux.
Be sure to do your usual chmod shenanigans.

# Instructions
To call from anywhere in your shell, add this repo's folder to your system PATH, relaunch your shell, and run `setup-camp`, `setup-camp.bat` or `python setup-camp.py`
The first two internally call `python setup-camp.py` in some fashion.

## Usage Example:

`python setup_repo.py --org <org> --repo <repo>`

`python setup_repo.py --url <full_git_url>`
