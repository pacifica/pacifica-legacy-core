<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
>

<xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

<xsl:output method="text"/>
<xsl:template match="/">
<xsl:for-each select="/myemsl/files//file">
<xsl:value-of select="name"/>
<xsl:if test="not (position() = last())"><xsl:value-of select="$newline"/></xsl:if>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>
