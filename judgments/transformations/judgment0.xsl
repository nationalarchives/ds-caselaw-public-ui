<?xml version="1.0" encoding="utf-8"?>

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
	xpath-default-namespace="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
	xmlns:uk1="https:/judgments.gov.uk/"
	xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn"
	xmlns:html="http://www.w3.org/1999/xhtml"
	xmlns:math="http://www.w3.org/1998/Math/MathML"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	exclude-result-prefixes="uk1 uk html math xs">

<xsl:output method="html" encoding="utf-8" indent="no" include-content-type="no" /><!-- doctype-system="about:legacy-compat" -->

<!-- <xsl:strip-space elements="*" /> -->

<xsl:variable name="doc-id" as="xs:string">
	<xsl:variable name="work-uri" as="xs:string">
		<xsl:sequence select="/akomaNtoso/judgment/meta/identification/FRBRWork/FRBRthis/@value" />
	</xsl:variable>
	<xsl:variable name="long-form-prefix" as="xs:string" select="'https://caselaw.nationalarchives.gov.uk/id/'" />
	<xsl:choose>
		<xsl:when test="starts-with($work-uri, $long-form-prefix)">
			<xsl:sequence select="substring-after($work-uri, $long-form-prefix)" />
		</xsl:when>
		<xsl:otherwise>
			<xsl:sequence select="$work-uri" />
		</xsl:otherwise>
	</xsl:choose>
</xsl:variable>
<xsl:variable name="title" as="xs:string">
	<xsl:sequence select="/akomaNtoso/judgment/meta/identification/FRBRWork/FRBRname/@value" />
</xsl:variable>
<xsl:variable name="image-base" as="xs:string" select="'https://judgment-images.s3.eu-west-2.amazonaws.com/'" />

<xsl:template match="akomaNtoso">
	<xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;
</xsl:text>
	<html>
        <head>
			<meta charset="utf-8" />
            <title>
                <xsl:value-of select="$title" />
            </title>
            <style>

body { padding: 1cm 1in }
				<xsl:call-template name="style" />
            </style>
        </head>
        <body>
			<xsl:apply-templates />
        </body>
	</html>
</xsl:template>

<xsl:template match="meta" />

<xsl:template name="style">
	<xsl:apply-templates select="/akomaNtoso/judgment/meta/presentation/html:style" />
	<xsl:apply-templates select="/akomaNtoso/judgment/attachments/attachment/doc/meta/presentation/html:style" />
</xsl:template>

<xsl:template match="html:style">
	<xsl:variable name="selector1" as="xs:string">
		<xsl:variable name="raw" as="xs:string" select="normalize-space(substring-before(., '{'))" />
		<xsl:choose>
			<xsl:when test="starts-with($raw, '#')">
				<xsl:sequence select="$raw" />
			</xsl:when>
			<xsl:otherwise>
				<xsl:sequence select="'#judgment'" />
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<xsl:for-each select="tokenize(., '\n')">
		<xsl:choose>
			<xsl:when test="matches(., '^\s*$')" />
			<xsl:when test="matches(., '^\s*#')">
				<xsl:value-of select="." />
			</xsl:when>
			<xsl:when test="matches(., '^\s*\.')">
				<xsl:value-of select="$selector1" />
				<xsl:text> </xsl:text>
				<xsl:value-of select="." />
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="selector" as="xs:string" select="substring-before(., '{')" />
				<xsl:variable name="value" as="xs:string" select="concat('{', substring-after(., '{'))" />
				<xsl:value-of select="$selector1" />
				<xsl:text> </xsl:text>
				<xsl:value-of select="$value" />
			</xsl:otherwise>
		</xsl:choose>
		<xsl:text>
</xsl:text>
	</xsl:for-each>
<xsl:value-of select="$selector1" /> .tab { display: inline-block; width: 0.25in }
<xsl:value-of select="$selector1" /> section { position: relative }
<xsl:value-of select="$selector1" /> h2 { font-size: inherit; font-weight: normal }
<xsl:value-of select="$selector1" /> h2.floating { position: absolute; margin-top: 0 }
<xsl:value-of select="$selector1" /> .num { display: inline-block; padding-right: 1em }
<xsl:value-of select="$selector1" /> td { position: relative; min-width: 2em; padding-left: 1em; padding-right: 1em }
<xsl:value-of select="$selector1" /> td > .num { left: -2em }
<xsl:value-of select="$selector1" /> table { margin: 0 auto; width: 100%; border-collapse: collapse }
<xsl:value-of select="$selector1" /> .header table { table-layout: fixed }
<xsl:value-of select="$selector1" /> .fn { vertical-align: super; font-size: small }
<xsl:value-of select="$selector1" /> .footnote > p > .marker { vertical-align: super; font-size: small }
<xsl:value-of select="$selector1" /> .restriction { color: red }

</xsl:template>

<xsl:template match="judgment">
	<article id="judgment">
		<xsl:apply-templates />
		<xsl:apply-templates select="attachments/attachment/doc[@name='annex']" />
		<xsl:call-template name="footnotes" />
		<xsl:for-each select="attachments/attachment/doc[@name='annex']">
			<xsl:call-template name="footnotes" />
		</xsl:for-each>
	</article>
	<xsl:apply-templates select="attachments/attachment/doc[@name='attachment']" />
</xsl:template>

<xsl:template match="attachments" />

<xsl:template match="coverPage | header">
	<div class="{ local-name() }">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="judgmentBody">
	<div class="body">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="doc[@name='annex']">
	<section id="{ @name }{ count(../preceding-sibling::*) + 1 }">
		<xsl:apply-templates />
	</section>
</xsl:template>

<xsl:template match="doc[@name='attachment']">
	<article id="{ @name }{ count(../preceding-sibling::*) + 1 }">
		<xsl:apply-templates />
		<xsl:call-template name="footnotes" />
	</article>
</xsl:template>

<xsl:template match="doc[@name='attachment']/mainBody">
	<div class="body">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template name="class">
	<xsl:attribute name="class">
		<xsl:value-of select="local-name()" />
		<xsl:if test="@class">
			<xsl:text> </xsl:text>
			<xsl:value-of select="@class" />
		</xsl:if>
	</xsl:attribute>
</xsl:template>

<xsl:template match="level | paragraph">
	<section>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:if test="num | heading">
			<h2>
				<xsl:choose>
					<xsl:when test="exists(heading/@class)">
						<xsl:attribute name="class">
							<xsl:value-of select="heading/@class" />
						</xsl:attribute>
					</xsl:when>
					<xsl:when test="empty(heading)">
						<xsl:attribute name="class">floating</xsl:attribute>
					</xsl:when>
				</xsl:choose>
				<xsl:apply-templates select="num | heading" />
			</h2>
		</xsl:if>
		<xsl:apply-templates select="* except (num, heading)" />
	</section>
</xsl:template>

<!-- <xsl:template match="hcontainer[@name='tableOfContents']" /> -->

<xsl:template match="blockContainer">
	<section>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates select="* except num" />
	</section>
</xsl:template>

<xsl:template match="blockContainer/p[1]">
	<p>
		<xsl:apply-templates select="@*" />
		<xsl:apply-templates select="preceding-sibling::num" />
		<xsl:apply-templates />
	</p>
</xsl:template>

<xsl:template match="p | span | a">
	<xsl:element name="{ local-name() }">
		<xsl:apply-templates select="@*" />
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="block">
	<p>
		<xsl:attribute name="class">
			<xsl:value-of select="@name" />
			<xsl:if test="@class">
				<xsl:text> </xsl:text>
				<xsl:value-of select="@class" />
			</xsl:if>
		</xsl:attribute>
		<xsl:apply-templates select="@* except @name, @class" />
		<xsl:apply-templates />
	</p>
</xsl:template>

<xsl:template match="num | heading">
	<span>
		<xsl:attribute name="class">
			<xsl:value-of select="local-name()" />
		</xsl:attribute>
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</span>
</xsl:template>

<xsl:template match="neutralCitation | courtType | docketNumber | docDate">
	<span>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</span>
</xsl:template>

<xsl:template match="party | role | judge | lawyer">
	<span>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</span>
</xsl:template>

<xsl:template match="img">
	<img>
		<xsl:apply-templates select="@*" />
		<xsl:apply-templates />
	</img>
</xsl:template>
<xsl:template match="img/@src">
	<xsl:attribute name="src">
		<xsl:sequence select="concat($image-base, $doc-id, '/', .)" />
	</xsl:attribute>
</xsl:template>

<xsl:template match="br">
	<xsl:element name="{ local-name() }">
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="date">
	<span>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</span>
</xsl:template>


<!-- tables -->

<xsl:template match="table">
	<table>
		<xsl:copy-of select="@class | @style" />
		<xsl:if test="exists(@uk1:widths)">
			<colgroup>
				<xsl:for-each select="tokenize(@uk1:widths, ' ')">
					<col style="width:{.}" />
				</xsl:for-each>
			</colgroup>
		</xsl:if>
		<xsl:if test="exists(@uk:widths)">
			<colgroup>
				<xsl:for-each select="tokenize(@uk:widths, ' ')">
					<col style="width:{.}" />
				</xsl:for-each>
			</colgroup>
		</xsl:if>
		<tbody>
			<xsl:apply-templates />
		</tbody>
	</table>
</xsl:template>

<xsl:template match="tr | td">
	<xsl:element name="{ local-name() }">
		<xsl:copy-of select="@*" />
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>


<!-- tables of contents -->

<xsl:template match="toc">
	<div>
		<xsl:attribute name="class">
			<xsl:value-of select="local-name()" />
			<xsl:if test="@class">
				<xsl:text> </xsl:text>
				<xsl:value-of select="@class" />
			</xsl:if>
		</xsl:attribute>
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="tocItem">
	<p class="toc">
		<xsl:attribute name="class">
			<xsl:value-of select="local-name()" />
			<xsl:if test="@class">
				<xsl:text> </xsl:text>
				<xsl:value-of select="@class" />
			</xsl:if>
		</xsl:attribute>
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</p>
</xsl:template>


<!-- markers and attributes -->

<xsl:template match="marker[@name='tab']">
	<span class="tab"> </span>
</xsl:template>

<xsl:template match="@class | @style | @src | @href | @title">
	<xsl:copy />
</xsl:template>

<xsl:template match="@refersTo | @date | @as" />

<xsl:template match="@*" />


<!-- footnotes -->

<xsl:template match="authorialNote">
	<span class="fn">
		<xsl:value-of select="@marker" />
	</span>
</xsl:template>

<xsl:template name="footnotes">
	<xsl:variable name="footnotes" select="descendant::authorialNote" />
	<xsl:if test="$footnotes">
		<footer>
			<hr style="margin-top:2em" />
			<xsl:apply-templates select="$footnotes" mode="footnote" />
		</footer>
	</xsl:if>
</xsl:template>

<xsl:template match="authorialNote" mode="footnote">
	<div class="footnote">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="authorialNote/p[1]">
	<xsl:element name="{ local-name() }">
		<xsl:apply-templates select="@*" />
		<span class="marker">
			<xsl:value-of select="../@marker" />
		</span>
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>


<!-- math -->

<xsl:template match="math:*">
	<xsl:copy>
		<xsl:copy-of select="@*"/>
		<xsl:apply-templates />
	</xsl:copy>
</xsl:template>

</xsl:transform>
