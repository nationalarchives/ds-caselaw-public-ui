xquery version "1.0-ml";

declare variable $uri as xs:string external;

let $judgment_xml := fn:doc($uri)/element()
let $judgment_published_property := xdmp:document-get-properties($uri, xs:QName("published"))[1]
let $is_published := $judgment_published_property/text()

let $return_value := if (xs:boolean($is_published)) then
        xdmp:xslt-invoke('judgments/xslts/judgment2.xsl',
          $judgment_xml
        )/element()
    else
        ()

return $return_value
