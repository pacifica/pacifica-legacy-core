<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html"
  media-type="text/html"
  encoding="UTF-8"
  indent="yes"/>
<xsl:template match="/">
  <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;
</xsl:text>
  <html>
  <head>
    <xsl:text disable-output-escaping='yes'>&lt;/meta&gt;
</xsl:text>
    <xsl:if test="not(myemsl/status/step[@id = 6 and @status = 'SUCCESS'] or myemsl/status/step[@status = 'ERROR'])">
      <script type="text/javascript" src="/myemsl/status/refresh.js"></script>
    </xsl:if>
    <script type='text/javascript' src='/myemsl/status/prototype.js'></script>
    <xsl:text disable-output-escaping='yes'>&lt;link rel="stylesheet" type="text/css" href="/myemsl/status/status_style.css"&gt;&lt;/link&gt;
</xsl:text>
  </head>
  <body>
    <h2>MyEMSL Status</h2>
      <div class="bar_holder">
        <xsl:for-each select="myemsl/status/step">
            <span>
                <xsl:choose>
                  <xsl:when test="@status = 'SUCCESS'"><xsl:attribute name="class">green_bar_end</xsl:attribute></xsl:when>
                  <xsl:when test="@status = 'ERROR'"><xsl:attribute name="class">red_bar_end</xsl:attribute></xsl:when>
                  <xsl:otherwise><xsl:attribute name="class">orange_bar_end</xsl:attribute></xsl:otherwise>
                </xsl:choose>
                <xsl:attribute name="style">z-index:-<xsl:value-of select="@id"/></xsl:attribute>
                <xsl:attribute name="rel"><xsl:value-of select="translate(@message,'_',' ')" /></xsl:attribute>
                <xsl:choose>
                  <xsl:when test="@id = 0">Submitted</xsl:when>
                  <xsl:when test="@id = 1">Received</xsl:when>
                  <xsl:when test="@id = 2">Processing</xsl:when>
                  <xsl:when test="@id = 3">Verified</xsl:when>
                  <xsl:when test="@id = 4">Stored</xsl:when>
                  <xsl:when test="@id = 5">Available</xsl:when>
                  <xsl:when test="@id = 6">Archived</xsl:when>
                  <xsl:otherwise>Step <xsl:value-of select="@id"/></xsl:otherwise>
                </xsl:choose>
            </span>
        </xsl:for-each>
      </div>

    <xsl:if test="myemsl/status/step[@id = 5 and @status = 'SUCCESS']">
      <xsl:element name="a">
        <xsl:attribute name="target">_blank</xsl:attribute>
        <xsl:attribute name="href">/myemsl/files/transaction/<xsl:value-of select="/myemsl/status/transaction/@id" />/data</xsl:attribute>
        View the files in this upload.
      </xsl:element>
    </xsl:if>
    <xsl:if test="not(myemsl/status/step[@id = 5 and @status = 'SUCCESS'])">
      <div>View the files in this upload.<span style="vertical-align:top;font-size:60%">(Pending Make Available)</span></div>
    </xsl:if>
    <xsl:element name="a">
      <xsl:attribute name="target">_blank</xsl:attribute>
      <xsl:attribute name="href">/myemsl/files/data</xsl:attribute>
        View all files in MyEMSL.
    </xsl:element>
    <script type="text/javascript"><![CDATA[
document.observe('dom:loaded', function() {
  $$('a[rel]').each(function(element) {
    new Tip(element, element.rel);
  });
});

    ]]>
    </script>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
