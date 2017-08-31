# What characters do I need to encode in a CSS data URI?

Chrome seems to support direct insertion of SVG into a CSS URL to avoid having to base64 encode it and increase the size by ~1.33x which is kinda cool/handy. IE chokes on such things, however, desiring that the data URI is URL-encoded (e.g. `<` &rarr; `%3C`). Because *some* characters are increased in size by 3x, any savings are quickly obliterated, so might as well just use base64.

For a little SVG file:

* Raw, 289 B: `url('data:image/svg+xml,<svg xmlns="http://www.w3.org/" [...] </svg>')`
* Base64, 386 B: `url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaH5vcm [...] dmc+')`
* URL-encoded, 397 B: `url('data:image/svg+xml,%3Csvg%20xmlns%3D%22ht [...] svg%3E')`

However, with some monkeying around, I found that ol' `%20` isn't actually required for spaces in IE CSS data URIs, so for every space in the SVG, you could drop the size by 2 bytes. What characters do you actually have to encode?

Here, I used [`makepage.py`](makepage.py) to encode a little test SVG into a data URI several ways, encoding all but one special character that *should* be URL encoded (`! \"#$%&'(),:;<=>?[\]^``{|}~`) and used [Browserstack](https://www.browserstack.com/screenshots/5068c56b516fde070dad0e07ae4942c605c18a4b) to view the result in multiple browsers. It seems that the lowest common denominator (IE) only requires that `"'#%<>[]^``{|}` be escaped (when the data URI is wrapped in quotes).

Try your browser at https://nicktimko.github.io/svgenc

## Windows 7, IE 9

[![][1]][1]

Many minimized SVG files end up being smaller versus the base64 encoding, and the compatibility across browsers is identical


* No encoding (URI: **289 B**)
```
url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 21.9 31"><path fill="#000" d="M10.9 0C4.9 0 0 5.5 0 10.9 0 20.1 10.9 31 10.9 31s10.9-10.9 10.9-20.1C21.9 5.5 17 0 10.9 0zM6.1 10.9c0-2.7 2.2-4.8 4.8-4.8s4.8 2.2 4.8 4.8c0 2.7-2.2 4.8-4.8 4.8s-4.8-2.1-4.8-4.8z"/></svg>')
```   
      
* Base64 encoded (URI: **386 B**)
```
url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMS45IDMxIj48cGF0aCBmaWxsPSIjMDAwIiBkPSJNMTAuOSAwQzQuOSAwIDAgNS41IDAgMTAuOSAwIDIwLjEgMTAuOSAzMSAxMC45IDMxczEwLjktMTAuOSAxMC45LTIwLjFDMjEuOSA1LjUgMTcgMCAxMC45IDB6TTYuMSAxMC45YzAtMi43IDIuMi00LjggNC44LTQuOHM0LjggMi4yIDQuOCA0LjhjMCAyLjctMi4yIDQuOC00LjggNC44cy00LjgtMi4xLTQuOC00Ljh6Ii8+PC9zdmc+');
```

* URL encoded default (URI: **397 B**)
```
url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2021.9%2031%22%3E%3Cpath%20fill%3D%22%23000%22%20d%3D%22M10.9%200C4.9%200%200%205.5%200%2010.9%200%2020.1%2010.9%2031%2010.9%2031s10.9-10.9%2010.9-20.1C21.9%205.5%2017%200%2010.9%200zM6.1%2010.9c0-2.7%202.2-4.8%204.8-4.8s4.8%202.2%204.8%204.8c0%202.7-2.2%204.8-4.8%204.8s-4.8-2.1-4.8-4.8z%22/%3E%3C/svg%3E');
```

* URL encoded only `"#%<>[]^``{|}` (URI: **319 B**)
```
url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 21.9 31%22%3E%3Cpath fill=%22%23000%22 d=%22M10.9 0C4.9 0 0 5.5 0 10.9 0 20.1 10.9 31 10.9 31s10.9-10.9 10.9-20.1C21.9 5.5 17 0 10.9 0zM6.1 10.9c0-2.7 2.2-4.8 4.8-4.8s4.8 2.2 4.8 4.8c0 2.7-2.2 4.8-4.8 4.8s-4.8-2.1-4.8-4.8z%22/%3E%3C/svg%3E');
```

-- [From a question I originally asked/answered at StackOverflow](https://stackoverflow.com/q/34782535/194586)

  [1]: http://i.stack.imgur.com/qHsMy.png
