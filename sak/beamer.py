
def frame ( filename , title ) :

    with open( filename , 'w' ) as frame :
        frame.write( r"""\section{%s}
\begin{frame}\frametitle{\insertsection}\justifying

\end{frame}""" % title)

