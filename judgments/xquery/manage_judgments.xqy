xquery version "1.0-ml";
import module namespace dls = "http://marklogic.com/xdmp/dls"
      at "/MarkLogic/dls.xqy";


for $uri in cts:uris("", xs:string("limit=100"),xs:string("descending"))
  where fn:not(dls:document-is-managed($uri))
    return dls:document-manage($uri, fn:true())
