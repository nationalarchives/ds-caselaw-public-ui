xquery version "1.0-ml";
declare variable $uri as xs:string external;
let $judgment_xml := fn:doc($uri)/element()
let $xslt := <xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
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
	<xsl:choose>
		<xsl:when test="starts-with($work-uri, 't')">
			<xsl:sequence select="substring-after($work-uri, 't')" />
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
	<div>
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="judgmentBody">
	<div class="body">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="doc[@name='annex']">
	<section id="">
		<xsl:apply-templates />
	</section>
</xsl:template>

<xsl:template match="doc[@name='attachment']">
	<article id="">
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
	<xsl:element name="name">
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
	<xsl:element name="br">
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
					<col style="width:4" />
				</xsl:for-each>
			</colgroup>
		</xsl:if>
		<xsl:if test="exists(@uk:widths)">
			<colgroup>
				<xsl:for-each select="tokenize(@uk:widths, ' ')">
					<col style="width:4" />
				</xsl:for-each>
			</colgroup>
		</xsl:if>
		<tbody>
			<xsl:apply-templates />
		</tbody>
	</table>
</xsl:template>

<xsl:template match="tr | td">
	<xsl:element name="tr">
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
	<xsl:element name="p">
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

return xdmp:xslt-eval($xslt,
  $judgment_xml
)/element()
