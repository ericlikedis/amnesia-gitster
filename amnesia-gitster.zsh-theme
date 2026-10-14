local ret_status="%(?:%{$fg_bold[green]%}λ :%{$fg_bold[red]%}λ %s)"

# Color of the "amnesia" label; set it with `prompt-color-picker`.
_amnesia_color_file=~/.config/amnesia-color
_amnesia_color_precmd() {
  _AMNESIA_COLOR=green
  [[ -r $_amnesia_color_file ]] && _AMNESIA_COLOR=${$(<$_amnesia_color_file):-green}
}
autoload -Uz add-zsh-hook
add-zsh-hook precmd _amnesia_color_precmd

function get_pwd(){
  git_root=$PWD
  while [[ $git_root != / && ! -e $git_root/.git ]]; do
    git_root=$git_root:h
  done
  if [[ $git_root = / ]]; then
    unset git_root
    prompt_short_dir=%~
  else
    parent=${git_root%\/*}
    prompt_short_dir=${PWD#$parent/}
  fi
  echo $prompt_short_dir
}

PROMPT=' %{%B%F{$_AMNESIA_COLOR}%}amnesia%{%f%b%} $ret_status %{$fg[white]%}$(get_pwd) $(git_prompt_info)%{$reset_color%}%{$reset_color%} '

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg[cyan]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY=" %{$fg[yellow]%}✗%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_CLEAN=" %{$fg[green]%}✓%{$reset_color%}"

