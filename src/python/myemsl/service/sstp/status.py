#!/usr/bin/python

import subprocess
import libxml2
import libxslt

class Status_Error( Exception ):
    """
    A special exception class especially for the Status module
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

def status_output(jobid, remote_user, oformat="html"):
	p1 = subprocess.Popen(['myemsl_status', '--username', remote_user, '--jobid', jobid, '--format', oformat], stdout=subprocess.PIPE)
	return p1.communicate()

def require_condition( expr, msg ):
    """
    Requires a condition to be true, otherwise a Finish error is raised describing the error
    """
    if expr == False:
        raise Status_Error( msg )



def status():
    """
    Print status information about a job
    """

    print "Content-Type: text/plain; charset=us-ascii"
    print

    
