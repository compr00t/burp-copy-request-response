# Burp Extension: Copy Request & Response

## Description

Writing good reports is key in penetration tests / security assessments, since
this is the final result delivered to the customer. Vulnerabilities should be
described in a way so that the customer can understand and also reproduce the
issue. For web application pentests, the best way is often to show the HTTP
requests and responses to explain an issue. This Burp Suite extension "Copy
Request & Response" can assist you while the report.

When copying request/response from Burp, the workflow is often like this:

1. Select the request
2. Copy to clipboard
3. Switch to your reporting tool (Markdown, Web App, LaTeX Editor, `$YOUNAMEIT`)
4. Paste the request
5. Remove various entries in order to keep the focus
6. Switch back to Burp
7. Select the response
7. Copy to clipboard
8. Switch back to the report
9. Paste again
10. Remove various entries again
11. Add context to explain the request / response

The Copy Request & Response Burp Suite extension adds a new context menu
entry that can be used to simply copy the request and response from the
selected message to the clipboard. 

The workflow can then look like this:

1. Select "Copy Request & Response" from the context menu
2. Switch to the reporting tool (in markdown)
3. Paste
4. Add context to explain the request / response

Much easier, right? 😉

This extensions is based on a gread idea by mindfuckup (https://github.com/mindfuckup) 
and adapted to my own needs.

## Requirements

- Python environment / Jython for Burp Suite