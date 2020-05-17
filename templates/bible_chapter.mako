## bible_chapter.mako
<%inherit file="base.mako"/>
    <link rel="stylesheet" type="text/css" href="../styles/style-freq-tables.css">
    <main id="main_content" role="main" tabindex="-1">
        <h2>${words_in_chapter} word occurrences in ${bible_book_name} ${chapter} in the KJV (${words_in_bible} word occurrences in the entire KJV):</h2>
        <p>For an explanation of what information is in the linked-to .csv file and in the sortable (by any column) table below, see the Home page.</p>
        
        <nav>
            <a href="../index.html">Home: KJV Bible Chapter Word Frequencies</a>
            <a href="${book_abbrev.lower()}-index.html">${bible_book_name}</a>
            <a href="${csv_file_name}" target="_blank" type="text/csv">Open ${csv_file_name} in new tab or window</a>
        </nav>

        <details>
            <summary>Read ${bible_book_name} ${chapter}</summary>
${bible_chapter_text}
        </details>
<%doc>Table sorting uses the following script, as explained at
    https://stackoverflow.com/questions/10683712/html-table-sort/51648529
</%doc>
        <script src="../scripts/sorttable.js"></script>
        <table class="sortable countedtable">
            <thead>
                <tr>
                    <th class="sorttable_nosort">#</th>
                    <th title="Field #1">Word</th>
                    <th title="Field #2">In chapter</th>
                    <th title="Field #3">In KJV</th>
                    <th title="Field #4">Simple Freq</th>
                    <th title="Field #5"  id="weighted-freq">Weighted Freq</th>
                    <th class="sorttable_nosort">#</th>
                </tr>
            </thead>
            <tbody>
                % for row in rows:
                <tr>
                    <td class="numerical"></td>
                    <td>${row[0]}</td>
                    <td class="numerical">${row[1]}</td>
                    <td class="numerical">${row[2]}</td>
                    <td class="numerical">${row[3]}</td>
                    <td class="numerical">${row[4]}</td>
                    <td class="numerical"></td>
                </tr>
                % endfor
            </tbody>
        </table>

    </main>
