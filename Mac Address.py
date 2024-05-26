import re, uuid

print("")
print ("The MAC address of this PC is ", end="")
print (':'.join(re.findall('..', '%012x' % uuid.getnode())))

