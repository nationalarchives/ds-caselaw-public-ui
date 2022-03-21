xquery version "1.0-ml";
import module namespace dls="http://marklogic.com/xdmp/dls"
              at "/MarkLogic/dls.xqy";

dls:retention-rule-insert(
    dls:retention-rule(
        "All Versions Retention Rule",
        "Retain all versions of all documents",
        (),
        (),
        "Locate all of the documents",
        cts:and-query(())
    )
)
