<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:search="http://marklogic.com/appservices/search"
                exclude-result-prefixes="search"
                version="1.0">
    <xsl:output method="html" omit-xml-declaration="yes"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="search:result">
        <xsl:apply-templates select="search:snippet"/>
    </xsl:template>

    <xsl:template match="search:snippet">
        <xsl:if test="search:match/*">
            <xsl:apply-templates select="search:match"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="search:match">
        <p data-path="{@path}">
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <xsl:template match="search:highlight">
        <mark>
            <xsl:apply-templates/>
        </mark>
    </xsl:template>
</xsl:stylesheet>
