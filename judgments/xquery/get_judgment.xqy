xquery version "1.0-ml";

declare variable $show_unpublished as xs:boolean? external;
declare variable $uri as xs:string external;

let $judgment := fn:document($uri)
let $judgment_published_property := xdmp:document-get-properties($uri, xs:QName("published"))[1]
let $is_published := $judgment_published_property/text()

let $return_value := if ($show_unpublished) then
        $judgment
    else if (xs:boolean($is_published)) then
        $judgment
    else
        ()

return $return_value
