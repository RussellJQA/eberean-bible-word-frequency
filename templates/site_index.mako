## bible-word-frequency_index.mako
<%inherit file="base.mako"/>
    <main id='main_content' role='main' tabindex='-1'>
        ${readme_html}
        % for bible_book in bible_books:
        <a href='${str(book_nums[book_abbrevs[bible_book]]).zfill(2)}-${book_abbrevs[bible_book].lower()}/${book_abbrevs[bible_book].lower()}-index.html'>${bible_book}</a><br>
        % endfor
    </main>
