<?xml version="1.0" encoding="utf-8"?>

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
	xpath-default-namespace="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
	xmlns:html="http://www.w3.org/1999/xhtml"
	xmlns:math="http://www.w3.org/1998/Math/MathML"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	exclude-result-prefixes="html math xs">

<xsl:import href="page.xsl" />
<xsl:import href="judgment0.xsl" />

<xsl:param name="collection" as="xs:string" />
<xsl:param name="year" as="xs:string" />
<xsl:param name="number" as="xs:string" />

<xsl:template name="title">
	<xsl:value-of select="$title" />
</xsl:template>

<xsl:template name="breadcrumbs">
    <a href="/">/</a>
    <xsl:text> </xsl:text>
	<a href="/{ $collection }">
		<xsl:value-of select="$collection" />
	</a>
	<span> / </span>
	<a href="/{ $collection }/{ $year }">
		<xsl:value-of select="$year" />
	</a>
	<span> / </span>
	<span>
		<xsl:value-of select="$number" />
	</span>
</xsl:template>

<xsl:template name="middle-header">
	<div id="middle-header">
		<span class="title">
			<xsl:value-of select="$title" />
		</span>
	</div>
</xsl:template>

<xsl:template name="content">
	<div style="position:absolute;left:1em">
		<div style="width:6ch;text-align:center">
			<span style="display:inline-block;width:100%;padding:3pt;background-color:var(--color);color:gray">
				<a href="/{ $collection }/{ $year }/{ $number }/data.xml?pretty=true">view<br/>XML</a>
			</span>
		</div>
		<div style="margin-top:1em;width:6ch;text-align:center">
			<span style="display:inline-block;width:100%;padding:3pt;background-color:var(--color);color:gray">
				<a href="/{ $collection }/{ $year }/{ $number }?format=new">switch to new HTML format</a>
			</span>
		</div>
	</div>
	<xsl:variable name="attachments" as="element()*" select="/akomaNtoso/judgment/meta/references/hasAttachment" />
	<xsl:if test="exists($attachments)">
		<div class="attachments">
			<xsl:for-each select="$attachments">
				<p class="attachment" style="text-align:center">
					<a href="{ @href }" target="_blank" style="padding:3pt 6pt;background-color:var(--color);font-family:var(--font)">
						<xsl:value-of select="@showAs" />
					</a>
				</p>
			</xsl:for-each>
		</div>
	</xsl:if>
	<xsl:apply-templates select="/akomaNtoso/judgment" />
</xsl:template>

<xsl:template name="akomaNtoso">
	<xsl:apply-templates />
</xsl:template>


<!-- highlights -->

<xsl:template match="html:mark">
	<xsl:copy-of select="." />
</xsl:template>

</xsl:transform>
