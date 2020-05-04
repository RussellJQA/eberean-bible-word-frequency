## bible_chapter.mako
<%inherit file="base.mako"/>
        <link rel="stylesheet" type="text/css" href="../style_freq_tables.css">
        <main id="main_content" role="main" tabindex="-1">
        <h2>${words_in_chapter} word occurrences in ${bible_book_name} ${chapter} in the KJV (${words_in_bible} word occurrences in the entire KJV):</h2>
        <p>For an explanation of what information is in the linked-to .csv file and in the table below, see the Home page .</p>
        <nav>
            <a href='../bible_word_frequency_index.html'>Home: KJV Bible Chapter Word Frequencies</a><br>
            <a href="${book_abbrev}_index.html">${bible_book_name}</a><br>
            <a href="${csv_file_name}" target="_blank" type="text/csv">Open ${csv_file_name} in new tab or window</a><br><br>
        </nav>
        <!-- Table sorting uses the following script, as explained at
        https://stackoverflow.com/questions/10683712/html-table-sort/51648529 -->
        <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>
        <table class="sortable">
            <thead>
                <tr>
                    <th title="Field #1">Word</th>
                    <th title="Field #2">In chapter</th>
                    <th title="Field #3">In KJV</th>
                    <th title="Field #4">Simple Freq</th>
                    <th title="Field #5">Weighted Freq</th>
                </tr>
            </thead>
            <tbody>
                % for row in rows:
                <tr>
                    <td>${row[0]}</td>
                    <td class="integer">${row[1]}</td>
                    <td class="integer">${row[2]}</td>
                    <td>${row[3]}</td>
                    <td>${row[4]}</td>
                </tr>
                % endfor
            </tbody>
        </table>
    </main>