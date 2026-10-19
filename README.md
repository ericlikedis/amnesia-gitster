# amnesia-gitster

An [oh-my-zsh](https://ohmyz.sh) theme based on `lambda-gitster`. The prompt shows
a colored `amnesia` label, a `λ` that is green on success and red on failure, the
current directory (relative to the git root), and git status.

```
 amnesia λ my-repo/src ✓
```

## Install

```sh
git clone <this repo> && cd amnesia-gitster
./install.sh
```

Then set the theme in `~/.zshrc` and open a new terminal:

```sh
ZSH_THEME="amnesia-gitster"
```

## Choosing the label color

Run:

```sh
prompt-color-picker
```

A color picker opens in your browser. Click **Save** and the next prompt uses the
color, which is stored in `~/.config/amnesia-color` (defaults to green). The
picker runs a small local server bound to `127.0.0.1`; press Ctrl-C to stop it.

Exact hex colors need a truecolor terminal (e.g. iTerm2); macOS Terminal.app
approximates them.

## Requirements

- zsh + oh-my-zsh
- Python 3 and `open` or `xdg-open` (for the color picker)

## Credits

Based on the `lambda-gitster` theme.
https://github.com/ergenekonyigit/lambda-gitster
