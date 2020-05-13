## bible-word-frequency_index.mako
<%inherit file="base.mako"/>
    <main id="main_content" role="main" tabindex="-1">
        ${readme_html}
        <nav>
            % for bible_book_key in bible_book_index_hrefs:
            <a href="${bible_book_index_hrefs[bible_book_key]}">${bible_book_key}</a>
            % endfor
        <nav>
    </main>
