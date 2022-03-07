xquery version '1.0-ml';
xdmp:document-insert("/judgments/xslts/judgment2.xsl",
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
	xpath-default-namespace="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
	xmlns:html="http://www.w3.org/1999/xhtml"
	xmlns:math="http://www.w3.org/1998/Math/MathML"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	exclude-result-prefixes="html math xs">

<xsl:output method="html" encoding="utf-8" indent="yes" include-content-type="no" /><!-- doctype-system="about:legacy-compat" -->

<xsl:strip-space elements="*" />
<xsl:preserve-space elements="p block span" />

<xsl:param name="image-base" as="xs:string" select="'https://judgment-images.s3.eu-west-2.amazonaws.com/'" />

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

<xsl:template match="meta" />

<xsl:template match="judgment">
	<article class="judgment">
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
	<header class="judgment-header">
		<xsl:apply-templates />
	</header>
</xsl:template>

<xsl:template match="judgmentBody">
	<section class="judgment-body">
		<xsl:apply-templates />
	</section>
</xsl:template>

<xsl:template match="doc[@name='annex']">
	<section id="annex">
		<xsl:apply-templates />
	</section>
</xsl:template>

<xsl:template match="doc[@name='attachment']">
	<article id="attachment">
		<xsl:apply-templates />
		<xsl:call-template name="footnotes" />
	</article>
</xsl:template>

<xsl:template match="doc[@name='attachment']/mainBody">
	<div class="body">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="level">
	<section>
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

<xsl:template match="paragraph[exists(content/p)]">
	<xsl:apply-templates select="* except num" />
</xsl:template>

<xsl:template match="paragraph">
	<xsl:apply-templates />
</xsl:template>

<xsl:template match="paragraph/num">
	<span class="judgment-body__number">
		<xsl:apply-templates />
	</span>
</xsl:template>

<xsl:template match="paragraph/content/p[1]">
	<p class="judgment-body__section">
		<xsl:apply-templates select="../../num | ../../heading" />
		<span class="judgment-body__text">
			<xsl:apply-templates />
		</span>
	</p>
</xsl:template>

<xsl:template match="paragraph/content/p[position() gt 1]">
	<p class="judgment-body__section">
		<span class="judgment-body__number"></span>
		<span class="judgment-body__text">
			<xsl:apply-templates />
		</span>
	</p>
</xsl:template>

<!-- <xsl:template match="hcontainer[@name='tableOfContents']" /> -->

<!-- <xsl:template match="blockContainer">
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
</xsl:template> -->

<xsl:template match="header/p">
	<xsl:choose>
		<xsl:when test="empty(preceding-sibling::*) and exists(child::img)">
			<div class="judgment-header__logo">
				<xsl:apply-templates />
			</div>
		</xsl:when>
		<xsl:when test="exists(child::neutralCitation)">
			<div class="judgment-header__neutral-citation">
				<xsl:apply-templates />
			</div>
		</xsl:when>
		<xsl:when test="exists(child::docketNumber)">
			<div class="judgment-header__case-number">
				<xsl:apply-templates />
			</div>
		</xsl:when>
		<xsl:when test="exists(child::courtType)">
			<div class="judgment-header__court">
				<xsl:apply-templates />
			</div>
		</xsl:when>
		<xsl:when test="exists(child::docDate)">
			<div class="judgment-header__date">
				<xsl:apply-templates />
			</div>
		</xsl:when>
		<xsl:when test="matches(normalize-space(.), '^- -( -)+$')">
			<div class="judgment-header__line-separator" aria-hidden="true">
				<xsl:apply-templates />
			</div>
		</xsl:when>
		<xsl:otherwise>
			<xsl:next-match />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="p">
	<xsl:element name="p">
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="span">
	<xsl:element name="span">
		<xsl:apply-templates select="@style" />
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="p[@class='Quote']">
	<div class="judgment-body__section">
		<span class="judgment-body__number"></span>
		<div class="judgment-body__text">
			<blockquote>
				<p>
					<xsl:apply-templates />
				</p>
			</blockquote>
		</div>
	</div>
</xsl:template>

<xsl:template match="a">
	<xsl:element name="a">
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
		<xsl:apply-templates select="@style" />
		<xsl:apply-templates />
	</span>
</xsl:template>

<xsl:template match="neutralCitation | courtType | docketNumber | docDate">
	<span>
		<xsl:apply-templates select="@style" />
		<xsl:apply-templates />
	</span>
</xsl:template>

<xsl:template match="party | role | judge | lawyer">
	<span>
		<xsl:apply-templates select="@style" />
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

<xsl:template match="img/@style">
	<xsl:next-match>
		<xsl:with-param name="properties" select="('width', 'height')" />
	</xsl:next-match>
</xsl:template>

<xsl:template match="br">
	<br />
</xsl:template>

<xsl:template match="date">
	<span>
		<xsl:apply-templates />
	</span>
</xsl:template>


<!-- tables -->

<xsl:template match="table">
	<table>
		<tbody>
			<xsl:apply-templates />
		</tbody>
	</table>
</xsl:template>

<xsl:template match="tr">
	<xsl:element name="tr">
		<xsl:copy-of select="@*" />
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="td">
	<xsl:element name="td">
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

<xsl:template match="@style">
	<xsl:param name="properties" as="xs:string*" select="('font-weight', 'font-style', 'text-transform', 'font-variant')" />
	<xsl:variable name="values" as="xs:string*">
		<xsl:for-each select="tokenize(., ';')">
			<xsl:if test="tokenize(., ':')[1] = $properties">
				<xsl:sequence select="." />
			</xsl:if>
		</xsl:for-each>
	</xsl:variable>
	<xsl:if test="exists($values)">
		<xsl:attribute name="style">
			<xsl:sequence select="string-join($values, ';')" />
		</xsl:attribute>
	</xsl:if>
</xsl:template>

<xsl:template match="@class | @src | @href | @title">
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

 , xdmp:permission('app-user', 'execute'))
