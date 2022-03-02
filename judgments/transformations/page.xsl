<?xml version="1.0" encoding="utf-8"?>

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xpath-default-namespace="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:uk1="https:/judgments.gov.uk/"
    xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn"
    exclude-result-prefixes="xs uk1 uk">

<xsl:output method="html" encoding="utf-8" indent="yes" include-content-type="no" /> <!-- doctype-system="about:legacy-compat" -->

<xsl:template name="page">
	<xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;
</xsl:text>
	<html>
        <head>
			<meta charset="utf-8" />
            <title>
                <xsl:call-template name="title" />
            </title>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans" />
            <xsl:call-template name="links" />
            <style>
:root { --color: lavender; --font: 'Open Sans', sans-serif }
body { margin: 0 }

body > header { position: fixed; top: 0; left: 0; width: 100%; z-index: 100; padding: 0 1in 12pt 1in; background-color: var(--color); font-family: var(--font) }
body > header > div { display:flex; width:calc(100% - 2in); justify-content: space-between; align-items: baseline }
body > header h1 { margin-bottom: 0.25em }
#search-form, #lookup-form { margin-bottom: 0 }
#search-form > input[name='q'] { width: 40ch }
#middle-header { width: 50%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis }
#lookup-form > input[name='cite'] { width: 30ch }

body > #content { margin-top: 128px; padding: 0 1in 12pt 1in }
#left-column { font-family: var(--font) }
#middle-column { padding-left: 2em; font-family: var(--font) }
#right-column { padding-left: 2em; flex: 1; font-family: var(--font) }
#left-column > h2, #middle-column > h2, #right-column > h2 { margin-top: 0 }
a { color: inherit; text-decoration: none }
a:hover { text-decoration: underline }
body > header > div > h1 > a:hover { text-decoration: none }

ul.collections, ul.years, ul.judgments { padding: 0; list-style-type: none }
.collections > li > a, .years > li > a { display: inline-block; padding: 2pt 6pt }
.years > li { text-align: center }
.judgments > li > a { display: inline-block; padding: 3pt 6pt }
.collections > li:hover, .years > li:hover, .judgments > li:hover { background-color: var(--color) }
.collections > li.highlight, .years > li.highlight, .judgments > li.highlight { background-color: var(--color) }
.collections > li > a:hover, .years > li > a:hover, .judgments > li > a:hover { text-decoration: none }
.total { margin-top: 2em; margin-left: 6pt; font-size: smaller }

.pills { margin-top: 6pt }
.pill { margin-left: 1ch; margin-right: 1ch; border-radius: 25px; padding: 3pt 9pt; background-color: var(--color); font-size: smaller }
.pill > span, .pill > a { display: inline-block; margin-left: 3pt }
.search-result > div > a { display: inline-block; padding: 3pt 6pt }
.search-result > div > a:hover { text-decoration: none; background-color: var(--color) }
ul.snippets { margin-top: 3pt; margin-bottom: 9pt }

mark { padding: 0 2pt; background-color: var(--color) }

article + article { margin-top: 1in }

<xsl:call-template name="style" />
            </style>
        </head>
        <body>
            <header>
                <div>
                    <h1>
                        <a href="/">
                            <xsl:text>UK Judgments</xsl:text>
                        </a>
                    </h1>
                    <xsl:call-template name="search-form" />
                </div>
                <div>
                    <div id="breadcrumbs">
                        <xsl:call-template name="breadcrumbs" />
                    </div>
                    <xsl:call-template name="middle-header" />
                    <xsl:call-template name="lookup-form" />
                </div>
            </header>
            <div id="content">
                <xsl:call-template name="content" />
            </div>
        </body>
	</html>
</xsl:template>

<xsl:template name="title">
    <xsl:text>Judgments</xsl:text>
</xsl:template>

<xsl:template name="links" />

<xsl:template name="style" />

<xsl:template name="search-form">
    <form id="search-form" action="/search">
        <input type="text" name="q" placeholder="search terms" />
        <input type="submit" value="Search" />
        <a href="/search" style="display:inline-block;margin-left:3pt;font-size:smaller">Advanced</a>
    </form>
</xsl:template>

<xsl:template name="breadcrumbs">
    <xsl:text>&#160;</xsl:text>
</xsl:template>

<xsl:template name="middle-header" />

<xsl:template name="lookup-form">
    <form id="lookup-form" action="/lookup">
        <input type="text" name="cite" placeholder="neutral citation" />
        <input type="submit" value="Lookup" />
    </form>
</xsl:template>


<xsl:template name="content">
    <xsl:call-template name="two-columns" />
</xsl:template>

<xsl:template name="two-columns">
    <div style="display:flex">
        <div id="left-column">
            <xsl:call-template name="left-column" />
        </div>
        <div id="right-column">
            <xsl:call-template name="right-column" />
        </div>
    </div>
</xsl:template>

<xsl:template name="left-column" />

<xsl:template name="right-column" />

<xsl:template match="/" mode="row">
    <xsl:variable name="uri" as="xs:string" select="akomaNtoso/judgment/meta/identification/FRBRWork/FRBRthis/@value" />
    <xsl:variable name="long-form-prefix" as="xs:string" select="'https://caselaw.nationalarchives.gov.uk/id/'" />
    <xsl:variable name="uri-component" as="xs:string">
        <xsl:choose>
            <xsl:when test="starts-with($uri, $long-form-prefix)">
                <xsl:sequence select="substring-after($uri, $long-form-prefix)" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:sequence select="$uri" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <xsl:variable name="name" as="xs:string" select="akomaNtoso/judgment/meta/identification/FRBRWork/FRBRname/@value" />
    <xsl:variable name="cite" as="xs:string" select="(akomaNtoso/judgment/meta/proprietary/uk1:cite, akomaNtoso/judgment/meta/proprietary/uk:cite, akomaNtoso/judgment/header//neutralCitation)[1]" />
    <li>
        <a href="/{ $uri-component }">
            <xsl:value-of select="$name" />
            <xsl:text>, </xsl:text>
            <xsl:value-of select="$cite" />
        </a>
    </li>
</xsl:template>

</xsl:transform>
