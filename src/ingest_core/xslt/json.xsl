<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
{"MyEMSLStatus":[
<xsl:for-each select="myemsl/status/step">
  {"State":<xsl:value-of select="@id"/>, "Status":"<xsl:value-of select="@status"/>", "Message":"<xsl:value-of select="@message"/>"}<xsl:if test="position()!=last()">,</xsl:if>
</xsl:for-each>
]
<xsl:for-each select="myemsl/status/transaction">
,  "Transaction": "<xsl:value-of select="@id" />"
</xsl:for-each>
}
</xsl:template>
</xsl:stylesheet>
