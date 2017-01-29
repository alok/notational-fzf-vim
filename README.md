# Notational FZF

***Loosen the mental blockages to recording information. Scrape away the
tartar of convention that handicaps its retrieval.***

— [Notational Velocity home page](http://notational.net/)

![Usage](/screenshots/Screenshot%202017-01-24%2023.03.27.png?raw=true "Usage")

I want to write everything in Vim. But Vim isn't optimized for
note-taking. Instead, I used
[nvALT](http://brettterpstra.com/projects/nvalt/) for years, and
whenever I had to do serious editing, I would open the file in Vim.

But some things about nvALT bugged me. It's not meant for large text
files, and opening them will cause it to lag *a lot*. I can't use
splits, and having to have a separate window open for it when I'm
working in Vim is annoying.

Plugins like [vim-pad](https://github.com/fmoralesc/vim-pad) didn't do
it for me either, because I don't want to archive my notes or use the
first line as the title since I have notes with duplicated titles. I
just want to be able to search a set of directories and create notes in
one of them, ***quickly***.

When [Junegunn](https://github.com/junegunn/) made
[`fzf`](https://github.com/junegunn/fzf), I realized that I could
recreate Notational Velocity in Vim.

This plugin allows you to define a list of directories that you want to
search. It also handles Notational Velocity's issue with multiple
databases. UNIX does not allow repeated filenames in the same folder,
but often the parent folder provides context, like in `workout/TODO.md`
and `coding/TODO.md`.

The first directory in the list is used as the main directory, unless
you set `g:nv_main_directory`. If you press `control-x` after typing
some words, it will use those words as the filename to create a file in
the main directory. It will then open that file in a vertical split. If
that file already exists, don't worry, it won't overwrite it. This
plugin never modifies your files at any point. It can only read, open,
and create them.

You can define relative links, so adding `./docs` and `./notes` will
work. Keep in mind that it's relative to your current working directory
(as Vim interprets it).

This plugin may not work on Windows. I only have a Mac to test it on. It
works for sure on Mac with Neovim, and *should* work in terminal Vim,
since it's just a wrapper over `fzf`.

## Installation

``` {.vim}
" with vim-plug
Plug 'https://github.com/Alok/notational-fzf-vim'
```

## Dependencies

`ag` is required for its fast search. I'm not planning on changing this
anytime soon.

-   [`fzf`](https://github.com/junegunn/fzf)
-   [`ag`](https://github.com/ggreer/the_silver_searcher)

## Optional Dependencies

-   [`coderay`](https://github.com/rubychan/coderay), for the ability to
    preview files, with syntax highlighting.
-   [`highlight`](http://www.andre-simon.de/doku/highlight/en/highlight.html).
    Will be used instead of `coderay` if available.

## Required settings

You have to define a list of directories (which must be strings) to
search.

``` {.vim}
" example
let g:nv_directories = ['~/wiki', '~/writing', '~/code']
```

## Usage

This plugin unites searching and file creation. Just type in keywords
and it will search for them. It does not search in a fully fuzzy fashion
because that's less useful for prose. You can use the arrow keys or
`c-p` and `c-n` to scroll up and down the search results, and then hit
one of these keys to open up a file:

-   `c-x`: Use search string as filename and open in vertical split
-   `c-v`: Open in vertical split
-   `c-s`: Open in horizontal split
-   `c-t`: Open in new tab
-   `<Enter>`: Open highlighted search result in current buffer

The first few lines of the selected file will be visible in a preview
window.

## Mappings

This plugin defines a command `:NV`, and if you want a mapping for it,
then you can define it yourself. This is intentionally not done by
default. You should use whatever mapping or mappings work best for you.

For example,

``` {.vim}
nnoremap <c-s> :NV<CR>
```

## Optional settings and their defaults

``` {.vim}
" String. Set to '' (the empty string) if you don't want an extension appended by default.
" Don't forget the dot, unless you don't want one.
let g:nv_default_extension = '.md'

" String. Default is first in directory list.
let g:nv_main_directory = g:nv_directories[0]

" Boolean. Display filename in matches. Set to 0 if you want to hide the filename.
let g:nv_show_filepath = 1

" Boolean. Show preview. Set by default. Pressing Alt-p in FZF will toggle this for the current search.
let g:nv_show_preview = 1

" Boolean. Wrap text in preview window.
let g:nv_wrap_preview_text = 1

" Integer. Width of preview window. 72 characters by default.
let g:nv_preview_width = 72

" String. Determines where the preview window is. Valid options are: 'right', 'left', 'up', 'down'.
let g:nv_preview_direction = 'right'

"  Boolean. If set, will truncate each path element to a single character. If
you have colons in your pathname, this will fail. Not set by default.
let g:nv_use_short_pathnames = 0
```

You can also define your own handler function, in case you don't like
how this plugin handles input but like how it wraps everything else. It
*must* be called `NV_note_handler`.

## FAQ

Q: I get an error updating with `vim-plug`.

A: Remove the plugin with `:PlugClean` and re-run `:PlugInstall`.

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

This plug-in attempts to abstract the operation of note-taking over
*all* the notes you take, with priority given to one main notes
directory.

## Caveat Emptor

-   There is no Simplenote syncing, and there never will be. I use plain
    text files synced over services like Dropbox for my notes, and I
    don't plan on changing that anytime soon.

-   This plugin is just a wrapper over FZF that can view directories and
    open/create files. That's all it's ever meant to be. Anything else
    would be put into a separate plugin.
