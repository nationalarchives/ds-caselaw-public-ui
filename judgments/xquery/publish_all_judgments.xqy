xquery version "1.0-ml";
let $props := ( <published>true</published> )
for $uri in cts:uris()
  return xdmp:document-set-properties($uri, $props)
