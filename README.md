# Notational FZF

[![Actively Maintained](https://img.shields.io/badge/status-actively%20maintained-brightgreen)](https://github.com/alok/notational-fzf-vim/issues)

***Loosen the mental blockages to recording information. Scrape away the
tartar of convention that handicaps its retrieval.***

--- [Notational Velocity home page](http://notational.net/)

Notational Velocity is a note-taking app where searching for a note and
creating one are the same operation.

You search for a query, and if no note matches, it creates a new note
with that query as the title.

## Usage

See the following GIF or watch this
[asciinema](https://asciinema.org/a/oXAsE6lDnywkrSSH5xuOIVQuO):

![Usage](/screenshots/usage.gif?raw=true "Usage")

## Installation

``` {.vim}
" with vim-plug
Plug 'https://github.com/alok/notational-fzf-vim'
```

## Changes

Read `CHANGELOG.md`.

## Description

Vim is great for writing. But it isn't optimized for note-taking, where
you often create lots of little notes and frequently change larger notes
in a separate directory from the one you're working in. For years I used
[nvALT](http://brettterpstra.com/projects/nvalt/) and whenever I had to
do serious editing, I would open the file in Vim.

But some things about nvALT bugged me.

-   It's not meant for large text files, and opening them will cause it
    to lag *a lot*.

-   I can't use splits

-   I do most of my work in Vim, so why have another window open,
    wasting precious screen space with its inferior editing
    capabilities. Sorry Brett, but nvALT can't match Vim's editing
    speed.

-   I also disagree with some parts of Notational Velocity's philosophy.

Plugins like [vim-pad](https://github.com/fmoralesc/vim-pad) didn't do
it for me either, because:

-   I don't want to archive my notes. I should be able to just search
    for them.
-   I don't want to use the first line as the title since I have notes
    with duplicated titles in different directories, like `README.md`.
-   I just want to be able to search a set of directories and create
    notes in one of them, ***quickly***.

When [Junegunn](https://github.com/junegunn/) created
[`fzf`](https://github.com/junegunn/fzf), I realized that I could have
all that, in Vim.

This plugin allows you to define a list of directories that you want to
search. The first directory in the list is used as the main directory,
unless you set `g:nv_main_directory`. If you press `control-x` after
typing some words, it will use those words as the filename to create a
file in the main directory. It will then open that file in a vertical
split. If that file already exists, don't worry, it won't overwrite it.
This plugin never modifies your files at any point. It can only read,
open, and create them.

You can define relative links, so adding `./docs` and `./notes` will
work. Keep in mind that it's relative to your current working directory
(as Vim interprets it).

## Dependencies

-   [`rg`](https://github.com/BurntSushi/ripgrep) is required for its
    fast search.

-   [`fzf`](https://github.com/junegunn/fzf).

-   `fzf` Vim plugin. Install the Vim plugin that comes with `fzf`,
    which can be done like so if you use
    [vim-plug](https://github.com/junegunn/vim-plug).

    ``` {.vim}
    Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
    ```

-   Python 3.5 or higher, for the preview window and filepath
    shortening.

## Optional dependencies

-   Pypy 3, for a potential speedup

## Required Settings

You have to define a list of directories **or** files (which all must be
strings) to search. This setting is named `g:nv_search_paths`.

Remember that these can be relative links.

``` {.vim}
" example
let g:nv_search_paths = ['~/wiki', '~/writing', '~/code', 'docs.md' , './notes.md']
```

## Detailed Usage

This plugin unites searching and file creation. It defines two commands:

### `:NV` - Line-based Search (Original)

The original command that searches content line-by-line. When you select a
result, it opens the file and jumps to the matching line. Best for finding
specific content within notes.

Type `:NV` or bind it to a mapping to bring up a fuzzy search menu. Type
in your search terms and it will fuzzy search for them. Adding an
exclamation mark to the command (`:NV!`), will run it fullscreen.

You can type `:NV` to see all results, and then filter them with FZF.
You can type `:NV python` to restrict your initial search to lines that
contain the phrase `python`. `:NV [0-9] [0-9]` will find all numbers
separated by a space. You know, regexes.

It does not search in a fully fuzzy fashion because that's less useful
for prose. It looks for full words, but they don't have to be next to
each other, just on the same line. You can use the arrow keys or `c-p`
and `c-n` to scroll through the search results, and then hit one of
these keys to open up a file:

Note that the following options can be customized.

-   `c-x`: Use search string as filename and open in vertical split.
-   `c-v`: Open in vertical split
-   `c-s`: Open in horizontal split
-   `c-t`: Open in new tab
-   `c-y`: Yank the selected filenames
-   `<Enter>`: Open highlighted search result in current buffer

Additional built-in keybindings:

-   `alt-a`: Select all results
-   `alt-q`: Deselect all
-   `alt-p`: Toggle preview window
-   `alt-w`: Toggle preview line wrapping
-   `alt-u`/`alt-d`: Page up/down in results
-   `c-w`: Delete word backward
-   `c-/`: Cycle preview window position (right → down → hidden → right)

The lines around the selected file will be visible in a preview window.

### `:NVFiles` - Unique File Search (New)

An alternative command that shows unique files instead of individual lines.
Files are sorted by modification time (most recent first), and both filenames
and file contents are searched. This is closer to the original Notational
Velocity behavior.

```vim
:NVFiles        " Show all files sorted by mtime, filter interactively
:NVFiles python " Pre-filter to files matching 'python'
:NVFiles!       " Fullscreen mode
```

**Key differences from `:NV`:**
- Shows each file only once (no duplicates)
- Sorted by modification time (most recent first)
- Searches both filenames and content
- Opens file at the beginning (no line jumping)
- Interactive filtering re-searches as you type

**Use `:NV` when:** You need to find a specific line or jump to exact content.

**Use `:NVFiles` when:** You're looking for a note by name or topic and don't
need to jump to a specific line.

## Mappings

This plugin defines `:NV` and `:NVFiles` commands. If you want mappings
for them, you can define them yourself. This is intentionally not done
by default. You should use whatever mapping(s) work best for you.

For example,

``` {.vim}
nnoremap <silent> <c-s> :NV<CR>
nnoremap <silent> <c-n> :NVFiles<CR>
```

## Optional Settings and Their Defaults

You can display the full path by setting `g:nv_use_short_pathnames = 0`.

You can toggle displaying the preview window by pressing `alt-p`. This
is handy on smaller screens. If you don't want to show the preview by
default, set `g:nv_show_preview = 0`.

``` {.vim}
" String. Set to '' (the empty string) if you don't want an extension appended by default.
" Don't forget the dot, unless you don't want one.
let g:nv_default_extension = '.md'

" String. Default is first directory found in `g:nv_search_paths`. Error thrown
" if no directory found and g:nv_main_directory is not specified.
" NOTE: If you set g:nv_main_directory, it must ALSO appear in g:nv_search_paths
" for its contents to be searchable.
"let g:nv_main_directory = g:nv_main_directory or (first directory in g:nv_search_paths)

" Dictionary with string keys and values. Must be in the form 'ctrl-KEY':
" 'command' or 'alt-KEY' : 'command'. See examples below.
let g:nv_keymap = {
                    \ 'ctrl-s': 'split ',
                    \ 'ctrl-v': 'vertical split ',
                    \ 'ctrl-t': 'tabedit ',
                    \ })

" String. Must be in the form 'ctrl-KEY' or 'alt-KEY'
let g:nv_create_note_key = 'ctrl-x'

" String. Controls how new note window is created.
let g:nv_create_note_window = 'vertical split'

" Boolean. Show preview. Set by default. Pressing Alt-p in FZF will toggle this for the current search.
let g:nv_show_preview = 1

" Boolean. Respect .*ignore files in or above nv_search_paths. Set by default.
let g:nv_use_ignore_files = 1

" Boolean. Include hidden files and folders in search. Disabled by default.
let g:nv_include_hidden = 0

" Boolean. Wrap text in preview window.
let g:nv_wrap_preview_text = 1

" String. Width of window as a percentage of screen's width.
let g:nv_window_width = '40%'

" String. Determines where the window is. Valid options are: 'right', 'left', 'up', 'down'.
let g:nv_window_direction = 'down'

" String. Command to open the window (e.g. `vertical` `aboveleft` `30new` `call my_function()`).
let g:nv_window_command = 'call my_function()'

" Float. Width of preview window as a percentage of screen's width. 50% by default.
let g:nv_preview_width = 50

" String. Determines where the preview window is. Valid options are: 'right', 'left', 'up', 'down'.
let g:nv_preview_direction = 'right'

" String. Preview window border style. Options: 'border-left', 'border-rounded', 'border-sharp', 'noborder'.
" Requires fzf 0.35+.
let g:nv_preview_border = 'border-left'

" Boolean. Use tmux popup window instead of vim split (requires fzf 0.53+ and tmux).
let g:nv_use_tmux_popup = 0

" String. Yanks the selected filenames to the default register.
let g:nv_yank_key = 'ctrl-y'

" String. Separator used between yanked filenames.
let g:nv_yank_separator = "\n"

" Boolean. If set, will truncate each path element to a single character. If
" you have colons in your pathname, this will fail. Set by default.
let g:nv_use_short_pathnames = 1

"List of Strings. Shell glob patterns. Ignore all filenames that match any of
" the patterns.
let g:nv_ignore_pattern = ['summarize-*', 'misc*']

" List of Strings. Key mappings like above in case you want to define your own
" handler function. Most users won't want to set this to anything.

let g:nv_expect_keys = []

" Boolean. If set, automatically create a note when no results match and you
" press Enter. Disabled by default to preserve original behavior.
let g:nv_create_if_no_results = 0

" Dictionary. Map keys to directories for creating notes in specific locations.
" Each key creates a note in the corresponding directory instead of g:nv_main_directory.
" Example: let g:nv_create_dirs = {'ctrl-1': '~/notes', 'ctrl-2': '~/work'}
let g:nv_create_dirs = {}
```

### bat config

If `bat` is in the PATH then it will be used. It will use `$BAT_THEME` if it's set.

You can also define your own handler function, in case you don't like
how this plugin handles input but like how it wraps everything else. It
*must* be called `NV_note_handler`.

Integration with Goyo and other plugins may be accomplished by intercepting
the `User#NVLeave` event:

``` {.vim}
autocmd! User NVLeave Goyo
```


## Potential Use Cases

-   Add `~/notes` and `~/wiki` so your notes are only one key binding
    away.
-   Add relative links like `./notes`, `./doc`, etc. to
    `g:nv_search_paths` so you can always see/update the documentation
    of your current project and keep up-to-date personal notes.

## Philosophy

To quote [scrod](https://github.com/scrod/nv/issues/22),

> The reasoning behind Notational Velocity's present lack of
> multi-database support is that storing notes in separate databases
> would 1) Require the same kinds of decisions that
> category/folder-based organizers force upon their users (e.g., "Is
> this note going to be work-specific or home-specific?"), and 2) Defeat
> the point of instantaneous searching by requiring, ultimately, the
> user to repeat each search for every database in use.

-   By providing a default directory, we offer (one) fix to the first
    issue.

-   By searching the whole set of directories simultaneously, we handle
    the second.

It also handles Notational Velocity's issue with multiple databases.
UNIX does not allow repeated filenames in the same folder, but often the
parent folder provides context, like in `workout/TODO.md` and
`coding/TODO.md`.

This plug-in attempts to abstract the operation of note-taking over
*all* the notes you take, with priority given to one main notes
directory.

## Caveat Emptor

-   This plugin is just a wrapper over FZF that can view directories and
    open/create files. That's all it's ever meant to be. Anything else
    would be put into a separate plugin.

## Feedback

Is ***always*** welcome. If you have any ideas or issues, let me know
and I'll try to address them. Not all will be implemented, but if they
fit into the philosophy of this plugin or seem really useful, I'll do my
best.

## License

Apache 2
