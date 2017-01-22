" TODO doc if you have coderay this will work
" TODO doc ctr-x opens in vertical split.
" TODO doc: mapping: nnoremap <silent> ... :NV<CR>

if (exists("g:loaded_nv") && g:loaded_nv) || &compatible
    finish
endif

let g:loaded_nv = 1

" Copied from fzf.vim
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

" expand all directories and add trailing slash to avoid issues later
let s:dirs = map(copy(g:nv_directories), 'expand(v:val) . "/" ')

if exists('g:nv_main_directory')
    let s:main_dir = g:nv_main_directory
else
    let s:main_dir = s:dirs[0]
endif


function! s:handler(lines) abort
   " expect at least 2 elements, query and keypress, which may be empty strings
   let query = a:lines[0]
   let keypress = a:lines[1]
   " Don't forget to add spaces for the commands
   " Handle key input
   let cmd = get({
               \  'ctrl-s': 'split ',
                \ 'ctrl-v': 'vertical split ',
                \ 'ctrl-t': 'tabedit ',
                \ 'ctrl-x': 'vertical split ',
                \ },
                \ l:keypress, 'edit ')
   " preprocess candidates here. expect lines to have fmt:
   " filename:linenum:content

   if len(a:lines) >= 3 | let filenames = a:lines[2:] | endif

   " handle creating note
   if l:keypress ==? 'ctrl-x'
       " TODO doc don't type .md
     let candidates = [s:escape(s:main_dir  . '/' . l:query . s:ext)]
   else
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

" If the file you're looking for is empty, then why does it even exist? It's a
" note. Just type it's name. Hence we ignore lines with only space characters

" Use a big ugly option list
command! -bang NV
      \ call fzf#run(
          \ fzf#wrap({
              \ 'sink*': function('<sid>handler'),
              \ 'source': 'ag --nogroup "\S" ' . join(map(copy(s:dirs), 's:escape(v:val)')),
              \ 'options': '--print-query --ansi -m -e --delimiter=":" --with-nth=1.. --tiebreak=length,begin,index --expect=ctrl-s,ctrl-v,ctrl-t,ctrl-x --bind alt-a:select-all,alt-d:deselect-all --color hl:68,hl+:110 --preview "(coderay {1} || cat {}) 2> /dev/null | head -'.&lines.'"',
              \ }
      \ ))
