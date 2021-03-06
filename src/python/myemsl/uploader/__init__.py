#! /usr/bin/env python
"""
An Uploader module that uses PycURL to transfer data
"""

import os, sys, re, stat
from optparse import OptionParser
import pycurl
import tempfile
from myemsl import bundler
from getpass import getpass
from StringIO import StringIO


class Uploader_Error( Exception ):
    """
    A special exception class especially for the uploader module
    """

    def __init__( self, msg, outage=False ):
        """
        Initializes an Uploader_Error
        
        @param msg: A custom message packaged with the exception
        """
        self.msg = msg
	self.outage = outage

    def __str__( self ):
        """
        Produces a string representation of an Uploader_Error
        """
        if self.outage:
		return "Outage: %s" % self.msg
        return "Uploader failed: %s" % self.msg

def add_usage( parser ):
    """
    Adds a custom usage description string for this module to an OptionParser
    """
    parser.set_usage = "usage: %prog [options] [-b BUNDLE] [-c DIR1 -f FILE1 -f FILE2 -c DIR2 -f FILE3]..."

def add_options( parser, add_bundler_args=True ):
    """
    Adds custom command line options for this module to an OptionParser
    """

    # Upload the bundle to the specified server
    parser.add_option( '-s', '--server', type='string', action='store', dest='server',
                       default='ingest.my.emsl.pnl.gov',
                       help="Set the upload server to SERVER", metavar='SERVER' )

    # Upload the bundle using a specified protocol
    parser.add_option( '-P', '--protocol', type='string', action='store', dest='protocol', default='http',
                       help="Set the transfer protocol to PROTOCOL", metavar='PROTOCOL' )

    # Upload the bundle using a specified protocol
    parser.add_option( '-A', '--askpassword', dest='ask_password', default=False, action='store_true',
                       help="Ask the user for a password in a secure prompt" )

    # Upload the bundle as user
    parser.add_option( '-u', '--user', type='string', action='store', dest='user', default='',
                       help="Upload as the username USER", metavar='USER' )

    # Set the transfer to be unsecured
    parser.add_option( '-k', '--insecure', dest='insecure', default=False, action='store_true',
                       help="Use unsecured transfer" )

    # Just upload, no prompting
    parser.add_option( '-y', '--yes', dest='yes', default=False, action='store_true',
                       help="Answer yes to all questions" )

    # Set the transfer to be unsecured
    parser.add_option( '-n', '--negotiate', dest='negotiate', default=False, action='store_true',
                       help="Enable Kerberos5 negotiation for authentification" )
    if add_bundler_args:
       bundler.add_options( parser )
    else:
       parser.add_option( '-v', '--verbose', dest='verbose', default=False, action='store_true',
                       help="Be verbose" )

def check_options( parser ):
    """
    Performs custom option checks for this module given an OptionParser
    """

    if parser.values.bundle_name == '' and parser.values.file_list == []:
        parser.error( "You must specify either a bundle or a list of files to upload" )

    if parser.values.ask_password:
        parser.values.password = getpass( "Enter Password:" )
    else:
        parser.values.password = ':'



def upload( bundle_name='bundle.zip', protocol='http', server='myemsl-dev0.emsl.pnl.gov', user='',
            insecure=False, password=':', negotiate=False, verbose=False ):
    """
    Uploads a bundle of files via cURL to a specified server
    
    :Parameters:
        bundle_name
            The name of the bundle file to upload.
        protocol
            The communication protocol to use for the upload
        server
            The server to which the bundle should be uploaded
        user
            The user name on the destination server to use for the upload
        insecure
            Use insecure authentification ( don't verify the destination server )
        password
            The password to use for the selected user on the destination server
        negotiate
            Use Kerberos5 negotiation to authenticate the upload
        verbose
            Print lots and lots of status information for the upload
        
    @note This function assumes a bundle has been created already and is ready to upload
    """
    status = None

    bundle_path = os.path.abspath( bundle_name )
    if not os.path.exists( bundle_path ):
        raise Uploader_Error( "The target bundle does not exist:\n    %s" % bundle_path )

    # @todo: get cURL to use protocol as a guide for authentification type
    url = '%s://%s' % ( protocol, server )

    # If user isn't supplied, use the currently logged in user
    if user == '':
        user = os.getlogin()

    if verbose:
        print >> sys.stderr, 'Server URL: %s' % url
        print >> sys.stderr, 'File: %s' % bundle_path
        print >> sys.stderr, 'User: %s' % user

    server = ''
    location = ''



    # --- PycURL Options common to all 3 cURL actions ---

    # Set the user name and password for the queries.  Equivalent to --user cli option
    pycurl_userpwd = "%s:%s" % ( user, password )

    # Enable basic http authentification
    pycurl_httpauth = pycurl.HTTPAUTH_ANY

    # Enable Kerberos5 GssNegotiation for authentification.  Equivalent to --negotiate cli option
    if negotiate:
        pycurl_httpauth = pycurl.HTTPAUTH_GSSNEGOTIATE

    # Set SSL verification mode.  If insecure == true, this is equivalent to the --insecure cli option
    pycurl_ssl_verifypeer = not insecure

    # Set verbose mode in cURL
    pycurl_verbose = verbose

    cookie_file = tempfile.NamedTemporaryFile()
    cookie_jar = cookie_file.name

    # Pre-allocate with cURL
    if verbose:
        print >> sys.stderr, 'Peforming cURL preallocation'
    try:

        # Create the PycURL object
        curl = pycurl.Curl()

        pycurl_writeobject = StringIO()

        # Set the URL for the curl query.
        curl.setopt( pycurl.URL, url + "/myemsl/cgi-bin/preallocate" )

        # Set the output callback function to our StringIO object's write method
        curl.setopt( pycurl.WRITEFUNCTION, pycurl_writeobject.write )

        curl.setopt( pycurl.USERPWD, pycurl_userpwd )
        curl.setopt( pycurl.HTTPAUTH, pycurl_httpauth )
        curl.setopt( pycurl.SSL_VERIFYPEER, pycurl_ssl_verifypeer )
	curl.setopt( pycurl.SSL_VERIFYHOST, pycurl_ssl_verifypeer )
        curl.setopt( pycurl.VERBOSE, pycurl_verbose )
        curl.setopt( pycurl.COOKIEJAR, cookie_jar )
        curl.setopt( pycurl.FOLLOWLOCATION, 1 )
        curl.setopt( pycurl.UNRESTRICTED_AUTH, 1 )

        curl.perform()

        # Verify that authentification was successful
        curl_http_code = curl.getinfo( pycurl.HTTP_CODE )
        if curl_http_code / 100 == 4:
            raise Uploader_Error( "Authentification failed with code %i" % curl_http_code )

        if curl_http_code == 503:
            pycurl_writeobject.seek(0)
            raise Uploader_Error( pycurl_writeobject.read(), outage=True)

        # Make sure that cURL was able to get server and location data
        server = re.search( r'Server: ([\w\.-]*)', pycurl_writeobject.getvalue() ).group( 1 )
        location = re.search( r'Location: ([\w\./-@]*)', pycurl_writeobject.getvalue() ).group( 1 )

    except pycurl.error:
        raise Uploader_Error( "cURL operations failed for preallocation:\n    %s" % curl.errstr() )

    except AttributeError:
        raise Uploader_Error( "Failed to get proper server and/or location information from server" )

    if server == ''  or location == '':
        raise Uploader_Error( "Got invalid server and/or location information from server" )

    if verbose:
        print >> sys.stderr, 'Cookies:\n %s' %(open(cookie_jar).readlines())

    # Set the URL with the server data fetched via cURL
    url = '%s://%s' % ( protocol, server )

    if verbose:
        print >> sys.stderr, 'Fetched Server: %s' % server
        print >> sys.stderr, 'Fetched Location: %s' % location
        print >> sys.stderr, 'New Server URL: %s' % url

    # Upload bundle with cURL
    if verbose:
        print >> sys.stderr, 'Peforming cURL upload of bundle of %s' % bundle_path
    try:

        # Create the PycURL object
        curl = pycurl.Curl()

        # Set the URL for the curl query.
        curl.setopt( pycurl.PUT, 1 )
        curl.setopt( pycurl.UPLOAD, 1 )

        # Set the URL for the curl query.
        curl.setopt( pycurl.URL, url + location )

        # Set the input callback function to read from the bundle file
	bundlefd = open( bundle_path, 'rb' )
        curl.setopt( pycurl.READFUNCTION, bundlefd.read )
        # curl.setopt( pycurl.READDATA, bundlefd)
        size = os.lstat( bundle_path )[stat.ST_SIZE]
        curl.setopt( pycurl.INFILESIZE_LARGE, size )

        curl.setopt( pycurl.USERPWD, pycurl_userpwd )	
        curl.setopt( pycurl.HTTPAUTH, pycurl_httpauth )
        curl.setopt( pycurl.SSL_VERIFYPEER, pycurl_ssl_verifypeer )
	curl.setopt( pycurl.SSL_VERIFYHOST, pycurl_ssl_verifypeer )
        curl.setopt( pycurl.VERBOSE, pycurl_verbose )
        curl.setopt( pycurl.COOKIEJAR, cookie_jar )
        curl.setopt( pycurl.COOKIEFILE, cookie_jar )

        curl.perform()

        curl_http_code = curl.getinfo( pycurl.HTTP_CODE )
        if curl_http_code == 503:
            pycurl_writeobject.seek(0)
            raise Uploader_Error( pycurl_writeobject.read(), outage=True)

    except pycurl.error:
        raise Uploader_Error( "cURL operations failed during upload:\n    %s" % curl.errstr() )

    except IOError:
        raise Uploader_Error( "Couldn't read from bundle file" )



    # Finalize the upload
    if verbose:
        print >> sys.stderr, 'Peforming cURL finalization of upload'
    try:

        # Create the PycURL object
        curl = pycurl.Curl()

        pycurl_writeobject = StringIO()

        # Set the URL for the curl query.
        curl.setopt( pycurl.URL, url + "/myemsl/cgi-bin/finish" + location )

        # Set the output callback function to our StringIO object's write method
        curl.setopt( pycurl.WRITEFUNCTION, pycurl_writeobject.write )

        curl.setopt( pycurl.USERPWD, pycurl_userpwd )
        curl.setopt( pycurl.HTTPAUTH, pycurl_httpauth )
        curl.setopt( pycurl.SSL_VERIFYPEER, pycurl_ssl_verifypeer )
	curl.setopt( pycurl.SSL_VERIFYHOST, pycurl_ssl_verifypeer )
        curl.setopt( pycurl.VERBOSE, pycurl_verbose )
        curl.setopt( pycurl.COOKIEJAR, cookie_jar )
        curl.setopt( pycurl.COOKIEFILE, cookie_jar )

        curl.perform()

        curl_http_code = curl.getinfo( pycurl.HTTP_CODE )
        if curl_http_code == 503:
            pycurl_writeobject.seek(0)
            raise Uploader_Error( pycurl_writeobject.read(), outage=True)

        status = re.search( r'Status: (.*)', pycurl_writeobject.getvalue() ).group( 1 )
        # Make sure that the upload was accepted
        if re.search( r'Accepted', pycurl_writeobject.getvalue() ) == None:
            raise Uploader_Error( "Upload was not accepted" )

    except pycurl.error:
        raise Uploader_Error( "cURL operations failed for finalization:\n    %s" % curl.errstr() )

    try:

        # Create the PycURL object
        curl = pycurl.Curl()

        pycurl_writeobject = StringIO()

        # Set the URL for the curl query.
        curl.setopt( pycurl.URL, url + "/myemsl/logout" )

        # Set the output callback function to our StringIO object's write method
        curl.setopt( pycurl.WRITEFUNCTION, pycurl_writeobject.write )

        curl.setopt( pycurl.USERPWD, pycurl_userpwd )
        curl.setopt( pycurl.HTTPAUTH, pycurl_httpauth )
        curl.setopt( pycurl.SSL_VERIFYPEER, pycurl_ssl_verifypeer )
	curl.setopt( pycurl.SSL_VERIFYHOST, pycurl_ssl_verifypeer )
        curl.setopt( pycurl.VERBOSE, pycurl_verbose )
        curl.setopt( pycurl.COOKIEJAR, cookie_jar )
        curl.setopt( pycurl.COOKIEFILE, cookie_jar )

        curl.perform()

    except pycurl.error:
        raise Uploader_Error( "cURL operations failed for finalization:\n    %s" % curl.errstr() )

    cookie_file.close()

    return status

def confirm(prompt):
    prompt = "%s (%s|%s): " % (prompt, 'y', 'n')
        
    while True:
        res = raw_input(prompt)
        if res not in ['y', 'Y', 'n', 'N']:
            print 'Please enter y or n.'
            continue
        if res == 'Y' or res == 'y':
            return True
        if res == 'N' or res == 'n':
            return False

def upload_from_options( parser ):
    """
    Upload a bundle of files based upon command line options specified in an OptionParser
    """

    bundle_handle = None
    # If the file list is not empty, bundle the specified files in the specified bundle using the bundler module
    if len( parser.values.file_list ) > 0:
        bundle_handle = bundler.check_options( parser, bundle_name_optional=True )
        bundler.bundle_from_options( parser )

    if not parser.values.yes:
    	os.system("tar -tvf %s" %(parser.values.bundle_name))
    	res = confirm("Contents look ok?")
        if not res:
		sys.exit(0)
    res = upload( bundle_name=parser.values.bundle_name,
                   protocol=parser.values.protocol,
                   server=parser.values.server,
                   user=parser.values.user,
                   insecure=parser.values.insecure,
                   password=parser.values.password,
                   verbose=parser.values.verbose
                   )
    if bundle_handle:
        bundle_handle.close()
    return res

def main():
    try:
        parser = OptionParser()
        add_usage( parser )
        add_options( parser )
        parser.parse_args()
        if parser.values.verbose:
            print >> sys.stderr, "Begining Upload process"
        check_options( parser )
        status = upload_from_options( parser )
        if parser.values.verbose:
            print >> sys.stderr, "Uploaded %s successfully" % parser.values.bundle_name
        print "Status URL: %s" % ( status )
    except Uploader_Error, err:
        print >> sys.stderr, str(err)

if __name__ == '__main__':
    main()
