xquery version "1.0-ml";

declare variable $uri as xs:string external;
let $status := xdmp:document-get-properties($uri, xs:QName("published"))[1]
return $status/text()
