from pysnmp.entity.rfc3413.oneliner import cmdgen
droped = open("droped.txt", "w+")

list=[IP_ADDRRESS]
for i in list:
    print("IP Address: "+str(i))
    droped.write("###################################################################" + "\n")
    droped.write("IP Address: " + str(i) + "\n")
    errorIndication, errorStatus, errorIndex, \
    varBindTable = cmdgen.CommandGenerator().bulkCmd(
                cmdgen.CommunityData('putnetcorero'),
                cmdgen.UdpTransportTarget((str(i), 161)),
                0,
                25,
                (1,3,6,1,4,1,1916,1,4,14,1,1), # drop packet OID . This works fine.
                #(1,3,6,1,2,1,4,21), # ipRouteTable
                #(1,3,6,1,2,1,4,22), # ipNetToMediaTable
            )

    if errorIndication:
       print( errorIndication)
    else:
        if errorStatus:
            print ('%s at %s\n' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                ))
            droped.write('%s at %s\n' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                ) + "\n")
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    print ('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                    droped.write('%s = %s' % (name.prettyPrint(), val.prettyPrint())+"\n")
droped.close()
