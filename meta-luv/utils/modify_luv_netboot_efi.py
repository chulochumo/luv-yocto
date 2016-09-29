#!/usr/bin/python
#
# Copyright 2016 Intel Corporation; author Gayatri Kammela
#
# This script changes luv_netconsole and luv_storage parameters for network
# debugging(netconsole) and sending the results to the webserver respectively,
# when booting LUV via netboot(luv-netboot-image.efi). To know the usage of
# this file $ ./modify_luv_netboot_efi.py --help
#
#################################################################

import string
import argparse
import sys


def modify_luv_netboot_efi():
    parser = argparse.ArgumentParser()

    # .efi file is the FILENAME of the netboot image and retrieved
    # with args.filename
    parser.add_argument("-f", "--file", dest="filename",
                        help="read data from FILENAME")

    # luv_netconsole are the parameters required to enable netconsole
    # and retrieved with args.luv_netconsole
    parser.add_argument("-n", "--netconsole", dest="luv_netconsole",
                    action="store",
                    help="The format of the netconsole '10.11.12.13,64001'")

    # url_link is the url of the the server/website to store results and
    # retrieved with args.url_link
    parser.add_argument("-u", "--url", dest="url_link",
                        action="store",
                        help="The format of url:'http://ipaddress/path/to/folder'")

    # use -v to get the verbose
    parser.add_argument("-v", "--verbose",
                    action="store_true", dest="verbose")
    # use -q to silence the response
    parser.add_argument("-q", "--quiet",
                    action="store_false", dest="verbose")

    args = parser.parse_args()
    
    if not args.filename:
        parser.error(" Please provide filename as an argument")
    if args.verbose:
        print ("reading %s..." % args.filename)
    
    if args.filename:
        f = open(args.filename, "rb")
        s = str(f.read())
        # calculate the start and end indices of the file using the keywords
        # such as 'set LUV_NETCONSOLE' as beginning and '#END' as the ending
        # strings of the luv.cfg file
        end_index = s.index('#END')
        start_index = s.index('set LUV_NETCONSOLE')

    if args.luv_netconsole:
        # assign the netconsole line including the parameters given to a 
        # variable
        new_net_luv = "set LUV_NETCONSOLE=" + args.luv_netconsole + "\n"
        if args.verbose:
            print ("Setting LUV_NETCONSOLE=" + args.luv_netconsole)
    else:
        new_net_luv = "set LUV_NETCONSOLE=" + " " + "\n"
        print ("No netconsole params found!, provide valid parameters if you "
               "intend to use netconsole")

    if args.url_link:
        # assign the url line including the parameters given to a variable
        new_url_luv = "set LUV_STORAGE_URL=" + args.url_link + "\n"
        if args.verbose:
            print ("Setting LUV_STORAGE_URL=" + args.url_link)
    else:
        new_url_luv = "set LUV_STORAGE_URL=" + " " + "\n"
        print ("No url found! provide url if you intend to save results")
        
    # Add the netconsole and url lines and assign it to a variable
    new_rep_str = new_net_luv + new_url_luv

    # check if the length of the both lines is greater than the file size,
    # if not pad the file with x number of white spaces that are equal to
    # the difference of both lines and the length of the file itself.
    # Padding the file with white spaces is required as we are modifying a
    # .efi binary file. Failing to do so will result in unreadable binary.
    if len(new_rep_str) > end_index - start_index:
        parser.error("Sorry can't replace the variables, too large!!")
    else:
        spaces = end_index - len(new_rep_str) - start_index
        x = ' '
        white_spaces = x*spaces
        s = s[:start_index] + new_rep_str + white_spaces + s[end_index:]
        f.close()
        f = open(args.filename, "wb")
        f.write(s)
        f.close()


modify_luv_netboot_efi()
