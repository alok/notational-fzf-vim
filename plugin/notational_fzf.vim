function! s:escape(path)
  return escape(a:path, ' $%#''"\')
endfunction

if !exists('g:nv_directories')
    echomsg 'g:nv_directories is not defined'
    finish
endif

if !exists('g:nv_default_extension')
    let s:ext = '.md'
else
    let s:ext = g:nv_default_extension
endif


if !exists('g:nv_wrap_preview_text')
    " No wrap by default.
    let g:nv_wrap_preview_text = 0
endif

if g:nv_wrap_preview_text
    " Meant to be spliced into command line.
    let s:wrap_text = ':wrap'
else
    " Use empty string to splice into command line.
    let s:wrap_text = ''
endif

if !exists('g:nv_show_preview')
    " Hide or show preview window by default. Default is to show it.
    let g:nv_show_preview = 1
endif

if g:nv_show_preview
    " Meant to be spliced into command line.
    let s:show_preview = ''
else
    " Use empty string to splice into command line.
    let s:show_preview = ':hidden'
endif

if !exists('g:nv_preview_width')
    " How wide to make preview window. 72 characters is default because pandoc
    " does hard wraps at 72 characters.
    let g:nv_preview_width = 72
endif

if !exists('g:nv_preview_direction')
    " Valid options are up,down,right,left. Default is "right". No colon for
    " this command since it's first in the list.
    let g:nv_preview_direction = 'right'
endif

if !exists('g:nv_expect_keys')
    let g:nv_expect_keys = ''
endif

" Expand all directories and add trailing slash to avoid issues later.
let s:dirs = map(copy(g:nv_directories), 'expand(v:val) . "/" ')

if exists('g:nv_main_directory')
    let s:main_dir = g:nv_main_directory
else
    let s:main_dir = s:dirs[0]
endif

function! s:handler(lines) abort
    if a:lines == [] || a:lines == ['','','']
        return
    endif
   " Expect at least 2 elements, query and keypress, which may be empty
   " strings.
   let query = a:lines[0]
   let keypress = a:lines[1]
   " Don't forget to add spaces for the commands.
   " Handle key input.
   let cmd = get({
               \  'ctrl-s': 'split ',
                \ 'ctrl-v': 'vertical split ',
                \ 'ctrl-t': 'tabedit ',
                \ 'ctrl-x': 'vertical split ',
                \ },
                \ l:keypress, 'edit ')
   " Preprocess candidates here. expect lines to have fmt:
   " filename:linenum:content

   " Handle creating note.
   if l:keypress ==? 'ctrl-x'
     let candidates = [s:escape(s:main_dir  . '/' . l:query . s:ext)]
   else
       let l:filenames = a:lines[2:]
       let l:candidates = []
       for l:filename in l:filenames
           " don't forget traiiling space in replacement
           let l:linenum = substitute(filename, '\v.{-}:(\d+):.*$', '+\1 ', '')
           let l:name = substitute(filename, '\v(.{-}):\d+:.*$', '\1', '')
           call add(l:candidates, l:linenum . s:escape(l:name))
       endfor
   endif

   for candidate in candidates
       execute l:cmd . candidate
   endfor

endfunction


if !exists('g:nv_use_short_pathnames')
    let g:nv_use_short_pathnames = 0
endif

if g:nv_use_short_pathnames
    let s:filepath_index = '3.. '
    let s:format_path_expr = ' | shorten_path_for_notational_fzf.py '
else
    let s:filepath_index = '1.. '
    let s:format_path_expr = ''
endif

function! s:surround_in_single_quotes(str)
    return "'" . a:str . "'"
endfunction

function! s:ignore_list_to_str(pattern)
    return join(map(copy(a:pattern), ' " --ignore " . s:surround_in_single_quotes(v:val) . " " ' ))
endfunction

if !exists('g:nv_ignore_pattern')
    let s:nv_ignore_pattern = ' '
else
    let s:nv_ignore_pattern = s:ignore_list_to_str(g:nv_ignore_pattern)
endif



" If the file you're looking for is empty, then why does it even exist? It's a
" note. Just type its name. Hence we ignore lines with only space characters.

" Use a big ugly option list. The '.. ' is because fzf wants a term of the
" form 'N.. ' where N is a number.
" Use backslash in front of 'ag' to ignore aliases.

command! -bang NV
      \ call fzf#run(
          \ fzf#wrap({
              \ 'sink*': function(exists('*NV_note_handler') ? 'NV_note_handler' : '<sid>handler'),
              \ 'source': '\ag --hidden ' .  s:nv_ignore_pattern  . ' --nogroup "\S" 2>/dev/null ' . join(map(copy(s:dirs), 's:escape(v:val)')) . ' 2>/dev/null ' . s:format_path_expr  . ' 2>/dev/null ' . ' ',
              \ 'options': '--print-query --ansi --multi --exact' .
              \ ' --delimiter=":" --with-nth=' . s:filepath_index .
              \ ' --tiebreak=length,begin,index ' .
              \ ' --expect=ctrl-s,ctrl-v,ctrl-t,ctrl-x' . g:nv_expect_keys .
              \ ' --bind alt-a:select-all,alt-d:deselect-all,alt-p:toggle-preview,alt-u:page-up,alt-d:page-down,ctrl-w:backward-kill-word ' .
              \ ' --color hl:68,hl+:110 ' .
              \ ' --preview "(highlight -O ansi -l {1} || coderay {1} || cat {1}) 2> /dev/null | head -' . &lines . '" ' .
              \ ' --preview-window=' . g:nv_preview_direction . ':' . g:nv_preview_width .  s:wrap_text .  s:show_preview . ' ',
              \ }
      \ ))
