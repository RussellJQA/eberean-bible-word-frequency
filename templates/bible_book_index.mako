## bible_book_index.mako
<%inherit file="base.mako"/>
    <main id="main_content" role="main" tabindex="-1">
        <nav>
            <a href="../index.html">Home: KJV Bible Chapter Word Frequencies</a>
        </nav>
        <nav>
            % for chapter in range (1, chapters_in_book+1):
            <a href="${book_abbrev.lower()}${str(chapter).zfill(3)}-word-freq.html">${bible_book_name} ${str(chapter).zfill(3)}</a>
            % endfor
        <nav>
    </main>
