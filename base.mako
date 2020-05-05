## base.mako
<!doctype html>
<html lang='en'>

<head>
    <meta charset="UTF-8">
    <meta name="description" content="${description}">
    <meta name="keywords" content="${keywords}">
    <meta name="date" content="${datestamp}">
    <meta name="last-modified" content="${datestamp}">
    <meta name="language" content="english">
    <meta name="author" content="${author} (${site})">
    <meta name="copyright" content="${year} ${author}. All rights reserved.">
    <meta name="generator" content="HTML">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:site_name" content="${og_site_name}">
    <title>${title_h1}</title>

    <link rel="stylesheet" type="text/css" href="${style_sheet_path}">
    ##  I had originally just put the style sheet in the root.
    ##  That worked fine except if I just opened a downloaded copy of the Web site,
    ##  and opened 1 of its pages directly.
    ##  So, to allow even that to work, I'm passing the style sheet location as
    ##  parameter to the template.
</head>

<body>
    <a name="top"></a>
    <header role="banner"><%block name="header">
        <h1>${title_h1}</h1>
    </%block></header>
    ${self.body()}
    <footer role="contentinfo"><%block name="footer">
        <p><a href="#top">Back to Top</a></p>
        <p><a href="https://github.com/RussellJQA/bible-word-frequency">Website source code on GitHub</a></p>
        <p>Copyright &copy; ${year} by ${author}</p>
    </%block></footer>
</body>

</html>