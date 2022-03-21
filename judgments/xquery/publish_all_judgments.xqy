xquery version "1.0-ml";
import module namespace dls="http://marklogic.com/xdmp/dls"
              at "/MarkLogic/dls.xqy";

let $props := ( <published>true</published> )
for $uri in cts:uris("", (), dls:documents-query())
  return dls:document-set-properties($uri, $props)
