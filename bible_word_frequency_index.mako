## bible-word-frequency_index.mako
<%inherit file="base.mako"/>
    <main id='main_content' role='main' tabindex='-1'>
        <p>
            This site provides information about how often each word occurs in the <a href="https://ebible.org/Scriptures/eng-kjv_readaloud.zip">(KJV) Bible<a>.
        </p>
        <p>
            For each chapter in the Bible, it displays a sortable table with 5 columns of information for each word in that chapter:
            <ol>
                <li>Word: the word</li>
                <li>In chapter: The number of times that word occurs in that Bible chapter</li>
                <li>In KJV: The number of times that word occurs in the entire Bible</li>
                <li>Simple Freq: The simple, unweighted relative frequency of that word in this chapter:<br>
                    &nbsp;&nbsp;the total number of words in the Bible multiplied by the quotient of:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;In chapter (2nd column): The number of times that word occurs in that Bible chapter<br>
                    &nbsp;&nbsp;divided by:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;In KJV (3rd column): The number of times that word occurs in the entire Bible
                </li>
                <li>Weighted Freq: The weighted relative frequency of that word in this chapter:<br>
                    &nbsp;&nbsp;the sum of:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;the quotient of:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Simple Freq (4th column)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;divided by:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;the total number of words in the chapter<br>
                    &nbsp;&nbsp;and In chapter (2nd column) - 1<br>
                </li>
            </ol>
        </p>
        <p>
            The page also has a downloadable .csv file containing the same information.
        </p>
        % for bible_book in bible_books:
        <a href='${str(book_nums[bible_books[bible_book][0]]).zfill(2)}_${bible_books[bible_book][0]}/${bible_books[bible_book][0]}_index.html'>${bible_book}</a><br>
        % endfor
    </main>
