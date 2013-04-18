<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
MyEMSL Status
<xsl:for-each select="myemsl/status/step">
  <xsl:choose>
    <xsl:when test="@id = 0">
  Submitted For Processing
    </xsl:when>
    <xsl:when test="@id = 1">
  Transaction Assigned
    </xsl:when>
    <xsl:when test="@id = 2">
  Unbundle Job Submission
    </xsl:when>
    <xsl:when test="@id = 3">
  Verify Bundle Type
    </xsl:when>
    <xsl:when test="@id = 4">
  Unbundle
    </xsl:when>
    <xsl:when test="@id = 5">
  Make Available
    </xsl:when>
    <xsl:when test="@id = 6">
  Data Safe
    </xsl:when>
    <xsl:otherwise>
  Step <xsl:value-of select="@id"/>
    </xsl:otherwise>
  </xsl:choose>
  <xsl:if test="@status = 'SUCCESS'">Status:  Success</xsl:if>
  <xsl:if test="@status = 'ERROR'">Status:  Error</xsl:if>
    Message: <xsl:value-of select="@message"/>
</xsl:for-each>
</xsl:template>

</xsl:stylesheet>
