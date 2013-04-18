#!/bin/env python
# Author: Joshua Short (joshua.short@pnnl.gov)
# Date: 06/17/2011
# Description:
#     a test script for myemsl's file bundling and uploading
#       ability to choose bundle type: (zip, tar)
#       ability to choose bundle count: [1,...]
#       ability to choose file count: [1,...]
#       ability to choose file size: [1,...]
import os
import tempfile
from optparse import OptionParser
from getpass import getpass

import myemsl.bundler
import myemsl.uploader 

def do_bundle(path, bundle_id, bundle_type):
        bundle_path = os.path.join(path, "bundle_%s.%s" % (bundle_id, bundle_type))
        bundler = Bundler(bundle_path)

        for file_id in range(0, parser.values.file_count):
            t = tempfile.NamedTemporaryFile()
            d = content.read(parser.values.file_size)
            t.write(d)
            t.file.flush()
            bundler.bundle_file(t.name, "file_%s" % file_id)

    	bundler.bundle_metadata()
        return bundle_path

if __name__ == "__main__":

    # initialize and use an option parser
    parser = OptionParser()
    parser.set_usage = "usage: %prog [options]"
    parser.add_option("-d", "--directory",
                       type="string", action="store", dest='directory',
                       default='.', metavar="DIRECTORY",
                       help="Set the directory in which to place generated bundle(s)")
    parser.add_option("-t", "--bundle-type",
                       type="string", action="store", dest='bundle_type',
                       default='tar', metavar="TYPE",
                       help="Set the type of bundle to create (e.g. zip, tar)")
    parser.add_option("-b", "--bundle-count",
                       type="int", action="store", dest='bundle_count',
                       default=1, metavar="N",
                       help="Set the number of bundles to create")
    parser.add_option("-f", "--file-count",
                       type="int", action="store", dest='file_count',
                       default=1, metavar="N",
                       help="Set the number of files to create per bundle")
    parser.add_option("-e", "--file-size",
                       type="int", action="store", dest='file_size',
                       default=4096, metavar="N",
                       help="Set the size of files to upload")
    parser.add_option("-z", "--zero",
                       dest="zero", default=False, action='store_true',
                       help="Generated zeroed files instead random ones" )
    parser.add_option("-S", "--bundle-same",
                       dest="bundle_same", default=False, action='store_true',
                       help="Upload the same bundle multiple times instead of unique ones" )

    myemsl.uploader.add_options(parser, add_bundler_args=False)

    args = parser.parse_args()

    if parser.values.zero:
        parser.values.bundle_same = True

    parser.values.bundle_name = "doesn't matter"
    myemsl.uploader.check_options(parser)
    
    # select and instantiate the correct bundler type
    if parser.values.bundle_type == "zip":
        Bundler = myemsl.bundler.Zip_Bundler
    elif parser.values.bundle_type == "tar":
        Bundler = myemsl.bundler.Tar_Bundler

    # get the real file system path to the specified directory
    path = os.path.realpath(parser.values.directory)
    if parser.values.zero:
        content = open('/dev/zero')
    else:
        content = open('/dev/urandom')

    # loop through the desired number of bundles and files to create test bundles
    bundles = []
    if parser.values.bundle_same:
        bundle_path = do_bundle(path, 0, parser.values.bundle_type)
        for bundle_id in range(0, parser.values.bundle_count):
            bundles += [bundle_path]

    else:
        for bundle_id in range(0, parser.values.bundle_count):
            bundle_path = do_bundle(path, bundle_id, parser.values.bundle_type)
            bundles += [bundle_path]

    # upload each of the created bundles with the given credentials
    for bundle in bundles:
        print "Uploading %s" % bundle
        status = myemsl.uploader.upload(bundle_name=bundle,
                   protocol=parser.values.protocol,
                   server=parser.values.server,
                   user=parser.values.user,
                   insecure=parser.values.insecure,
                   password=parser.values.password,
                   verbose=parser.values.verbose
                   )
        print "Status URL: %s" %(status)

    # remove the created bundles
    [os.remove(bundle) for bundle in bundles]
