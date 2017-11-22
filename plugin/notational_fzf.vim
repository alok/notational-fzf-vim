"============================== Utility functions =============================
function! s:escape(path)
  return escape(a:path, ' $%#''"\')
endfunction

function! s:double_quote(str)
    return '"' . a:str . '"'
endfunction

function! s:single_quote(str)
    return "'" . a:str . "'"
endfunction

"============================== User settings ==============================

if !exists('g:nv_directories')
    echoerr 'g:nv_directories is not defined'
    finish
endif

let s:ext = get(g:, 'nv_default_extension', '.md')

" Valid options are ['up', 'down', 'right', 'left']. Default is 'right'. No colon for
" this command since it's first in the list.
let s:preview_direction = get(g:, 'nv_preview_direction', 'right')

let s:wrap_text = get(g:, 'nv_wrap_preview_text', 0) ? 'wrap' : ''

" Show preview unless user set it to be hidden
let s:show_preview = get(g:, 'nv_show_preview', 1) ? '' : 'hidden'

" How wide to make preview window. 72 characters is default because pandoc
" does hard wraps at 72 characters.
let s:preview_width = exists('g:nv_preview_width') ? string(float2nr(str2float(g:nv_preview_width) / 100.0 * &columns)) : ''

" Expand all directories and add trailing slash to avoid issues later.
let s:dirs = map(copy(g:nv_directories), 'expand(v:val)')

let s:main_dir = get(g:, 'nv_main_directory', s:dirs[0])

"=========================== Keymap ========================================

let s:create_note_key = get(g:, 'nv_create_note_key', 'ctrl-x')
let s:create_note_window = get(g:, 'nv_create_note_window', 'vertical split ')

let s:keymap = get(g:, 'nv_keymap',
            \ {'ctrl-s': 'split',
            \ 'ctrl-v': 'vertical split',
            \ 'ctrl-t': 'tabedit',
            \ })

" Use `extend` in case user overrides default keys
let s:keymap = extend(s:keymap, {
            \ s:create_note_key : s:create_note_window,
            \ })

" FZF expect comma sep str
let s:expect_keys = join(keys(s:keymap) + get(g:, 'nv_expect_keys', []), ',')

"================================ Short Pathnames ==========================

let s:use_short_pathnames = get(g:, 'nv_use_short_pathnames', 0)

" Can't be default since python3 is required for it to work
if s:use_short_pathnames
    let s:python_executable = executable('pypy3') ? 'pypy3' : 'python3'
    let s:format_path_expr = join(['|', s:python_executable, '-S', fnameescape(expand('<sfile>:p:h:h') . '/shorten_path_for_notational_fzf.py'),])
    let s:highlight_path_expr = join([s:python_executable  , '-S', fnameescape(expand('<sfile>:p:h:h') . '/print_lines.py') . ' {2} {1} ',])
    " After piping through the Python script, our format is
    " filename:linum:shortname:linenum:contents, so we start at index 3 to
    " avoid displaying the long pathname
    let s:display_start_index = '3..'
else
    let s:format_path_expr = ''
    " Since we don't pipe through the python script, our data format is
    " filename:linenum:contents, so we start at 1.
    let s:display_start_index = '1..'
endif

"============================ Ignore patterns ==============================

function! s:ignore_list_to_str(pattern)
    let l:glob_fmt = ' --glob !' " format to ignore a pattern. leading space matters
    return l:glob_fmt . join(map(copy(a:pattern), 's:single_quote(v:val)'), l:glob_fmt)
endfunction

let s:nv_ignore_pattern = exists('g:nv_ignore_pattern') ? s:ignore_list_to_str(g:nv_ignore_pattern) : ''

"============================== Handler Function ===========================

function! s:handler(lines) abort
    " exit if empty
    if a:lines == [] || a:lines == ['','','']
        return
    endif
   " Expect at least 2 elements, `query` and `keypress`, which may be empty
   " strings.
   let query    = a:lines[0]
   let keypress = a:lines[1]
   " `edit` is fallback in case something goes wrong
   let cmd = get(s:keymap, keypress, 'edit')
   " Preprocess candidates here. expect lines to have fmt
   " filename:linenum:content

   " Handle creating note.
   if keypress ==? s:create_note_key
     let candidates = [s:escape(s:main_dir  . '/' . query . s:ext)]
   else
       let filenames = a:lines[2:]
       let candidates = []
       for filename in filenames
           " Don't forget trailing space in replacement.
           let linenum = substitute(filename, '\v.{-}:(\d+):.*$', '+\1 ', '')
           let name = substitute(filename, '\v(.{-}):\d+:.*$', '\1', '')
           call add(candidates, linenum . s:escape(name))
       endfor
   endif

   for candidate in candidates
       execute join([cmd, candidate])
   endfor

endfunction

" If the file you're looking for is empty, then why does it even exist? It's a
" note. Just type its name. Hence we ignore lines with only space characters,
" and use the "\S" regex.

" Use a big ugly option list. The '.. ' is because fzf wants a term of the
" form 'N.. ' where N is a number.

" Use backslash in front of 'rg' to ignore aliases.
command! -nargs=* -bang NV
      \ call fzf#run(
          \ fzf#wrap({
              \ 'sink*': function(exists('*NV_note_handler') ? 'NV_note_handler' : '<sid>handler'),
              \ 'source': join([
                   \ 'command',
                   \ 'rg',
                   \ '--follow',
                   \ '--hidden',
                   \ '--line-number',
                   \ '--color never',
                   \ '--no-messages',
                   \ s:nv_ignore_pattern,
                   \ '--no-heading',
                   \ '--with-filename',
                   \ ((<q-args> is '') ?
                     \ '-F " " ' :
                     \ s:double_quote(<q-args>)),
                   \ '2>/dev/null',
                   \ join(map(copy(s:dirs), 's:escape(v:val)')) ,
                   \ '2>/dev/null',
                   \ s:format_path_expr,
                   \ '2>/dev/null',
                   \ ]),
                   \
              \ 'options': join([
                               \ '--print-query',
                               \ '--ansi',
                               \ '--multi',
                               \ '--exact',
                               \ '--inline-info',
                               \ '--delimiter=":"',
                               \ '--with-nth=' . s:display_start_index ,
                               \ '--tiebreak=' . 'length,begin' ,
                               \ '--expect=' . s:expect_keys ,
                               \ '--bind=' .  join([
                                              \ 'alt-a:select-all',
                                              \ 'alt-d:deselect-all',
                                              \ 'alt-p:toggle-preview',
                                              \ 'alt-u:page-up',
                                              \ 'alt-d:page-down',
                                              \ 'ctrl-w:backward-kill-word',
                                              \ ], ','),
                               \ '--color=' . join([
                                              \ 'hl:68',
                                              \ 'hl+:110',
                                              \ ], ',') ,
                               \ '--preview=' . s:double_quote(s:highlight_path_expr) ,
                               \ '--preview-window=' . join(filter(copy([
                                                                   \ s:preview_direction,
                                                                   \ s:preview_width,
                                                                   \ s:wrap_text,
                                                                   \ s:show_preview,
                                                                   \ ]),
                                                            \ 'v:val != "" ')
                                                       \ ,':')
                               \ ])}))
