#! /usr/bin/env python

import os, grp, tempfile

from myemsl.getconfig import getconfig
config = getconfig()

temp_prefix = 'MYEMSL_'



class Preallocate_Error( Exception ):
    """
    A special exception class especially for the Preallocate module
    """

    def __init__( self, msg ):
        """
        Initializes a Preallocate_Error
        
        @param msg: A custom message packaged with the exception
        """
        self.msg = msg

    def __str__( self ):
        """
        Produces a string representation of an Preallocate_Error
        """
        return "Error: %s" % self.msg

def require_condition( expr, msg ):
    """
    Requires a condition to be true, otherwise a Preallocate error is raised describing the error
    """
    if expr == False:
        raise Preallocate_Error( msg )

def mkstagedir(username):
    try:
        proc = SP.Popen( [ 'myemsl_mkstagedir', '--username', username ], stdout=SP.PIPE )
    except:
        raise Preallocate_Error( "Failed to create stage directory" )
    ( proc_out, proc_err ) = proc.communicate()
    require_condition( proc.returncode == 0, "Failed to exit normally. %i" % proc.returncode )


def preallocate(username, file_size = 0):
    # FIXME: where are these supposed to go?
    fsprefix="/var/www/myemsl/staging"
    webprefix="/myemsl/staging"

    group_name = None
    try:
        group_name = grp.getgrnam( config.get('unix', 'user') )
    except KeyError:
        raise Preallocate_Error( "Failed to get myemsl group" )
        
    require_condition( file_size > 0, "Invalid file size specified or no file size given" )
    
    location = os.path.join( fsprefix, remote_user )
    
    if not os.path.exists( location ):
        mkstagedir( username=remote_user )
    
    temp_handle = None
    temp_path = None
    temp_prefix = os.path.join( fsprefix, remote_user, temp_prefix )
    try:
        ( temp_handle, temp_path ) = tempfile.mkstemp( prefix=temp_prefix )
    except:
        raise Preallocate_Error( "Failed to make temporary file" )
        
    temp_file = os.path.basename( temp_path )
        
    # TODO: What do we do if size is not greater than 0?
    if size > 0:
        result = os.ftruncate( temp_handle, file_size )
        require_condition( result == 0, "Failed to truncate to size. %d" % result )

        print "Server: %s" % server_name
        print "Location: %s" % os.path.join( subdir_root, remote_user, temp_file )
        
        os.close( fd )

def preallocate_req( username, file_size = 0 ):
    try:
        (err, msg) = preallocate(username, file_size)
    except Preallocate_Error, err:
        (err, msg) = (False, str(err))
    return (err, msg)

def preallocate_from_options( parser ):
    """
    Preallocate for a transfer based upon command line options specified in an Option Parser
    """
    (options, args) = parser.parse_args()
    return preallocate(options.username, options.file_size)
    

def add_usage( parser ):
    """
    Adds a custom usage description string for this module to an Option Parser
    """
    pass
    
    

def add_options( parser ):
    """
    Adds custom command line options for this module to an OptionParser
    """
    parser.add_option("-u", "--username", dest="username", help="Username")
    parser.add_option("-s", "--filesize", dest="file_size", help="File Size")
    pass
                       
                       
                       
def check_options( parser ):
    """
    Performs custom option checks for this module given an Option Parser
    """
    pass
        
        

def main():
    try:
        parser = OptionParser()
        add_usage( parser )
        add_options( parser )
        parser.parse_args()
        check_options( parser )
        preallocate_from_options( parser )
    except Preallocate_Error, err:
        print err
    


if __name__ == '__main__':
    main()
