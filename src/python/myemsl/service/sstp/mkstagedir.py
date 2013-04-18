#/usr/bin/env python

import os, pwd, grp, stat
from optparse import OptionParser



staging_root = '/var/www/myemsl/staging'
allowed_user = 'apache'
allowed_group = 'svc-myemsl'



class Mkstagedir_Error( Exception ):
    """
    A special exception class especially for the mkstagedir module
    """

    def __init__( self, msg ):
        """
        Initializes a Mkstagedir_Error
        
        @param msg: A custom message packaged with the exception
        """
        self.msg = msg

    def __str__( self ):
        """
        Produces a string representation of an Mkstagedir_Error
        """
        return "Failed to Make Staging Directory: %s" % self.msg



def require_condition( expr, msg ):
    """
    Requires a condition to be true, otherwise a Mkstagedir_Error is raised describing the error
    """
    if expr == False:
        raise Mkstagedir_Error( msg )



def mkstagedir( username=None ):
    """
    Makes a staging directory for a user
    
    :Parameters:
        username
            the MyEmsl username for which to create the staging directory
    """
    
    require_condition( username not in [ None, '' ], "Cannot create a staging directory for an empty username" )
    
    realuid = os.getuid()
    
    pwent = None
    try:
        pwent = pwd.getpwuid( realuid )
    except KeyError:
        raise Mkstagedir_Error( "Couldn't find a pwd entry for the current uid %i" % realuid )
        
    require_condtion( pwent.pw_name == allowed_user ), "Only the apache user can use this tool" )
        
    grpent = None
    try:
        grpent = grp.getgrnam( allowed_group )
    except KeyError:
        raise Mkstagedir_Error( "Failed to get gid for the myemsl user" )
        
    location = os.path.join( staging_root, username )
    
    location_flags = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
    try:
        os.mkdir( location, location_flags )
    except OSError:
        raise Mkstagedir_Error( "Failed to create staging directory %s" % location )
    
    # TODO: determine if the flag argument passing is redundant
    try:
        os.chmod( location, location_flags )
    except OSError:
        raise Mkstagedir_Error( "Failed to set permissions for staging diretory %s " % location )
        
    try:
        os.chown( location, pwent.pw_uid, grpent.gr_gid )
    except OSError:
        raise Mkstagedir_Error( "Failed to set ownership for staging directory %s" % locaton )
        
        
    
def mkstagedir_from_options( parser ):
    """
    Makes a staging directory based upon command line options specified in an Option Parser
    """
    mkstagedir( username=parser.values.username )
    
    

def add_usage( parser ):
    """
    Adds a custom usage description string for this module to an Option Parser
    """
    
    parser.set_usage( "usage: %prog --username=NAME" )
    
    

def add_options( parser ):
    """
    Adds custom command line options for this module to an OptionParser
    """
    
    # Set the username option
    parser.add_option( '-u', '--username', type='string', action='store', dest='username', default=None,
                       help="Set the MyEmsl User Name to NAME", metavar='MAIN' )
                       
                       
                       
def check_options( parser ):
    """
    Performs custom option checks for this module given an Option Parser
    """
    
    if parser.values.username == None:
        parser.error( "A username argument must be supplied.  See usage or help for details" )
        
        

def main():
    try:
        parser = OptionParser()
        add_usage( parser )
        add_options( parser )
        parser.parse_args()
        check_options( parser )
        mkstagedir_from_options( parser )
    except Mkstagedir_Error, err:
        print >> sys.stderr, err
    


if __name__ == '__main__':
    main()
