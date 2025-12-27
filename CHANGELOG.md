## 3.0.0

Major feature release addressing long-standing issues.

### New Features

- **`:NVFiles` command** - New search mode showing unique files sorted by
  modification time. Searches both filenames and content, no duplicates.
  Closer to original Notational Velocity behavior. (Issue #22, #70)

- **`g:nv_create_if_no_results`** - Auto-create note when no results match
  and you press Enter. (Issue #92)

- **`g:nv_create_dirs`** - Map custom keys to create notes in specific
  directories. Example: `{'ctrl-1': '~/notes', 'ctrl-2': '~/work'}` (Issue #67)

### Bug Fixes

- Fixed shell escaping for `--bind` option to prevent errors with special
  characters like `|` and `()`. (Issue #99)

### Improvements

- Added GitHub issue templates for bug reports and feature requests
- Updated documentation with new options and commands

## 2.1.0

Added more window size management with `g:nv_window_width` and
`g:nv_window_direction`. Can now run fullscreen with `:NV!`.

## 2.0.0

-   Rename `g:nv_directories` to `g:nv_search_paths`. This emphasizes
    that you can search directories *and* files.
-   Use `shellescape` instead of `fnameescape` to avoid path issues.
-   Fix bug in search that would cause it to ignore 1-line long files.

## 1.1.0

-   Color filenames and line numbers.

## 1.0.0

-   [rg](https://github.com/BurntSushi/ripgrep) is now required. `ag`
    will no longer work.
-   The preview feature has been reworked. Now, the preview window will
    show several lines of context around the currently selected line.

## 0.8.0

-   New default for preview window that sensibly sets width. Most users
    should not need to set this anymore.
-   Short pathname display no longer shows `./` before filename if it's
    in the current working directory.

## 0.7.0

-   You can now restrict your search with arguments passed to `:NV`
-   Fixed a bug that made preview window too narrow

## 0.6.0

-   Improve path shortening to display (in decreasing order of
    priority):
    -   `.`
    -   `..`
    -   `~`
-   Python 3 is now required for the path shortening script to work.
-   Key mappings to open files are now customizable.
-   set `highlight` to use `truecolor` if available and Solarized Dark
    background.

## 0.5.0

-   `g:nv_preview_width` is now a percentage. This makes it more useful
    on small screens, but slightly less useful on large ones without
    some config.

## 0.4.0

-   Add support for files in `g:nv_directories`

## 0.3.0

-   Add (working) short pathnames feature

## 0.2.0

-   Updated README to include use cases and to be easier to read.

## 0.1.0

-   Added
    [`highlight`](http://www.andre-simon.de/doku/highlight/en/highlight.html)
    as (superior) alternative to `coderay`
