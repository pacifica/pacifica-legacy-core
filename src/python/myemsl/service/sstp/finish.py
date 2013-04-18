#/usr/bin/env python

import os
import Subprocess as SP
from optparse import OptionParser



class Finish_Error( Exception ):
    """
    A special exception class especially for the Finish module
    """

    def __init__( self, msg ):
        """
        Initializes a Finish_Error
        
        @param msg: A custom message packaged with the exception
        """
        self.msg = msg

    def __str__( self ):
        """
        Produces a string representation of an Finish_Error
        """
        return "Error: %s" % self.msg



def require_condition( expr, msg ):
    """
    Requires a condition to be true, otherwise a Finish error is raised describing the error
    """
    if expr == False:
        raise Finish_Error( msg )



def finish( username, bundle_path ):
    """
    Finish the transfer
    
    @username: username to finish the upload as
    @bundle_path: where the bundle of files is at

    Return:
    return success or throws error
    ( True, "Status URL" )
    """
    
    # Kerberos includes the domain in the remote_user variable
    remote_user = remote_user.split( '@' )[0]
    
    try:
        proc = SP.Popen( [ 'myemsl_ingest', '--username', remote_user, '--bundle', bundle, '--statefd', 0 ],
                         stdout=SP.PIPE )
    except:
        raise Finish_Error( "Failed to run" )
    
    ( proc_out, proc_err ) = proc.communicate()
    
    jobid = 0
    try:
        jobid = int( proc_out.split()[0] )
    except:
        raise Finish_Error( "can't get the child status" )
    
    require_condition( proc.returncode == 0, "Failed to exit normally. %i" % proc.returncode )
    
    return (True, "Status: http://%s%s/status/%d" % ( server_name, os.path.dirname( script_name ), jobid ))
    
def finish_req( user, bundle ):
    try:
        (err, msg) = finish(user, bundle)
    except Finish_Error, err:
        (err, msg) = (False, str(err))
    return
 
def finish_from_options( parser ):
    """
    Finish a transfer based upon command line options specified in an Option Parser
    """
    (options, args) = parser.parse_args()
    return finish_req(options.username, options.bundle)
    

def add_usage( parser ):
    """
    Adds a custom usage description string for this module to an Option Parser
    """
    
    parser.set_usage( "usage: %prog [options]" )
    
    

def add_options( parser ):
    """
    Adds custom command line options for this module to an OptionParser
    """
    parser.add_option("-u", "--username", dest="username", help="Username")
    parser.add_option("-b", "--bundle", dest="bundle", help="Bundle to process")
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
        finish_from_options( parser )
    except Finish_Error, err:
        print err
    


if __name__ == '__main__':
    main()
