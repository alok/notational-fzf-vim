function! s:escape(path)
  return escape(a:path, ' $%#''"\')
endfunction


"============================== User settings ==============================

if !exists('g:nv_directories')
    echomsg 'g:nv_directories is not defined'
    finish
endif

let s:ext = get(g:, 'nv_default_extension', '.md')
let s:wrap_text = get(g:, 'nv_wrap_preview_text', 0) ? 'wrap' : ''

" Show preview unless user set it to be hidden
let s:show_preview = get(g:, 'nv_show_preview', 1) ? '' : 'hidden'

" How wide to make preview window. 72 characters is default because pandoc
" does hard wraps at 72 characters.
let s:preview_width = exists('g:nv_preview_width') ? string(float2nr(str2float(g:nv_preview_width) / 100.0 * &columns)) : ''


" Valid options are ['up', 'down', 'right', 'left']. Default is 'right'. No colon for
" this command since it's first in the list.
let s:preview_direction = get(g:,'nv_preview_direction', 'right')


" Expand all directories and add trailing slash to avoid issues later.
let s:dirs = map(copy(g:nv_directories), 'expand(v:val)')

let s:main_dir = get(g:, 'nv_main_directory', s:dirs[0])

"=========================== Keymap ========================================

let s:create_note_key = get(g:, 'nv_create_note_key', 'ctrl-x')
let s:create_note_window = get(g:, 'nv_create_note_window', 'vertical split ')

let s:keymap = get(g:, 'nv_keymap',
            \ {'ctrl-s': 'split ',
            \ 'ctrl-v': 'vertical split ',
            \ 'ctrl-t': 'tabedit ',
            \ })

" Use `extend` in case user overrides default keys
let s:keymap = extend(s:keymap, {
            \ s:create_note_key : s:create_note_window,
            \ })

" FZF expect comma sep str
let s:expect_keys = join(keys(s:keymap) + get(g:, 'nv_expect_keys', []), ',')


"================================ Short Pathnames ==========================


" Can't be default since python3 is required for it to work
if get(g:, 'nv_use_short_pathnames', 0)
    let s:filepath_index = '3.. '
    let s:format_path_expr = ' | ' . fnameescape(expand('<sfile>:p:h:h') . '/shorten_path_for_notational_fzf.py') . ' '
else
    let s:filepath_index = '1.. '
    let s:format_path_expr = ''
endif


"============================ Ignore patterns ==============================

function! s:surround_in_single_quotes(str)
    return "'" . a:str . "'"
endfunction

function! s:ignore_list_to_str(pattern)
    return join(map(copy(a:pattern), ' " --ignore " . s:surround_in_single_quotes(v:val) . " " ' ))
endfunction


let s:nv_ignore_pattern = exists('g:nv_ignore_pattern') ? s:ignore_list_to_str(g:nv_ignore_pattern) : ''


"============================== Other settings ===========================
let s:highlight_format = has('termguicolors') ? 'truecolor' : 'xterm256'

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
   let cmd = get(s:keymap, keypress, 'edit ')
   " Preprocess candidates here. expect lines to have fmt
   " filename:linenum:content

   " Handle creating note.
   if keypress ==? s:create_note_key
     let candidates = [s:escape(s:main_dir  . '/' . query . s:ext)]
   else
       let filenames = a:lines[2:]
       let candidates = []
       for filename in filenames
           " don't forget traiiling space in replacement
           let linenum = substitute(filename, '\v.{-}:(\d+):.*$', '+\1 ', '')
           let name = substitute(filename, '\v(.{-}):\d+:.*$', '\1', '')
           call add(candidates, linenum . s:escape(name))
       endfor
   endif

   for candidate in candidates
       execute cmd . ' ' . candidate
   endfor

endfunction


" If the file you're looking for is empty, then why does it even exist? It's a
" note. Just type its name. Hence we ignore lines with only space characters,
" and use the "\S" regex.

" Use a big ugly option list. The '.. ' is because fzf wants a term of the
" form 'N.. ' where N is a number.

" Use backslash in front of 'ag' to ignore aliases.

command! -nargs=* -bang NV
      \ call fzf#run(
          \ fzf#wrap({
              \ 'sink*': function(exists('*NV_note_handler') ? 'NV_note_handler' : '<sid>handler'),
              \ 'source': '\ag --hidden ' .
                  \ s:nv_ignore_pattern  .
                  \ ' --nogroup ' . '"' .
                  \ (<q-args> ==? '' ? '\S' : <q-args>) .
                  \ '"' . ' 2>/dev/null ' .
                  \ join(map(copy(s:dirs), 's:escape(v:val)')) .
                  \ ' 2>/dev/null ' . s:format_path_expr  . ' 2>/dev/null ' ,
              \ 'options': '--print-query --ansi --multi --exact ' .
                  \ ' --delimiter=":" --with-nth=' . s:filepath_index .
                  \ ' --tiebreak=length,begin,index ' .
                  \ ' --expect=' . s:expect_keys .
                  \ ' --bind alt-a:select-all,alt-d:deselect-all,alt-p:toggle-preview,alt-u:page-up,alt-d:page-down,ctrl-w:backward-kill-word ' .
                  \ ' --color hl:68,hl+:110 ' .
                  \ ' --preview "(highlight --quiet --force --out-format=' . s:highlight_format . ' --style solarized-dark -l {1} || coderay {1} || cat {1}) 2> /dev/null | head -' . &lines . '" ' .
                  \ ' --preview-window=' . join([s:preview_direction ,  s:preview_width ,  s:wrap_text ,  s:show_preview]) . ' ',
              \ }
      \ ))
