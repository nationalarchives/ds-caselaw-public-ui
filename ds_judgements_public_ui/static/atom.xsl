<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom"
  exclude-result-prefixes="atom"
>
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
        <title><xsl:value-of select="atom:feed/atom:title"/> - Find Case Law - The National Archives</title>
        <style type="text/css">
          body{max-width:768px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";font-size:16px;line-height:1.5em}section{margin:30px 15px}h1{font-size:2em;margin:.67em 0;line-height:1.125em}h2{border-bottom:1px solid #eaecef;padding-bottom:.3em}.alert{background:#fff5b1;padding:4px 12px;margin:0 -12px}a{text-decoration:none}.entry h3{margin-bottom:0}.entry p{margin:4px 0}
        </style>
      </head>
      <body>
        <section>
          <div class="alert">
            <p>This is an <b>Atom feed</b> of documents in the Find Case Law service, sometimes also known as an RSS feed. <b>Subscribe</b> by copying the URL from the address bar into your newsreader app.</p>
          </div>
        </section>
        <section>
          <xsl:apply-templates select="atom:feed" />
        </section>
        <section>
          <h2>Recent Items</h2>
          <xsl:apply-templates select="atom:feed/atom:entry" />
        </section>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="atom:feed">
    <h1><xsl:value-of select="atom:title"/></h1>
    <p>This Atom feed provides the latest updates from the <a href="https://caselaw.nationalarchives.gov.uk">Find Case Law service</a>, operated by The National Archives.</p>

    <h2>What is an Atom feed?</h2>
    <p>An Atom feed is a data format that contains the latest content from a website, blog, or podcast. You can use feeds to <strong>subscribe</strong> to websites and get the <strong>latest content in one place</strong>.</p>
    <ul>
    	<li><strong>Feeds put you in control.</strong> Unlike social media apps, there is no algorithm deciding what you see or read. You always get the latest content.</li>
    	<li><strong>Feed are private by design.</strong> No one owns web feeds, so no one is harvesting your personal information and profiting by selling it to advertisers.</li>
    	<li><strong>Feeds are spam-proof.</strong> Had enough? Easy, just unsubscribe from the feed.</li>
    </ul>
    <p>All you need to do to get started is to add the URL (web address) for this feed to a special app called a newsreader. Visit <a href="https://aboutfeeds.com/">About Feeds</a> to get started with newsreaders and subscribing. It’s free. </p>
    <p>For more information on customising this feed, check our <a href="https://nationalarchives.github.io/ds-find-caselaw-docs/public#tag/Reading-documents/operation/atomFeed">API documentation</a>.</p>
  </xsl:template>

  <xsl:template match="atom:entry">
    <div class="entry">
      <h3>
        <a target="_blank">
          <xsl:attribute name="href">
            <xsl:value-of select="atom:id"/>
          </xsl:attribute>
          <xsl:value-of select="atom:title"/>
        </a>
      </h3>
      <p>
        <xsl:value-of select="atom:summary"  disable-output-escaping="yes" />
      </p>
      <small>
        <xsl:value-of select="atom:updated" />
      </small>
    </div>
  </xsl:template>

</xsl:stylesheet>
