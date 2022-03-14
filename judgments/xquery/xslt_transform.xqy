xquery version "1.0-ml";
declare variable $uri as xs:string external;
let $judgment_xml := fn:doc($uri)/element()
return xdmp:xslt-invoke('judgments/xslts/judgment2.xsl',
  $judgment_xml
)/element()
