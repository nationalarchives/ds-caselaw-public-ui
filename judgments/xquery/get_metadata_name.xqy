xquery version "1.0-ml";

declare namespace akn = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0";
declare variable $uri as xs:string external;

let $judgment := fn:document($uri)

return $judgment//akn:FRBRname/@value
