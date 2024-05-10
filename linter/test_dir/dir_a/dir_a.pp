File {
  owner => root,
  group => root,
}

# Default groups to put local admins in.
# Not sudo - separate sudoers policy for that, defining here gives a dependency loop
Localadmin {
  groups => $operatingsystem ? {
	  /Ubuntu/ => ['adm', 'cdrom', 'dip', 'plugdev', 'lpadmin', 'sambashare'],
    /CentOS/ => ['adm'],
    default   => [],
  }
}

node default {
    include role
}

file { "snmp.local.conf":
        content => template("snmp/snmpd.local.conf-coldfusion.erb"),
        path   => $operatingsystem ? { 
            Solaris => "/etc/sma/snmp/snmpd.local.conf",
            default => "/etc/snmp/snmpd.local.conf",
        },
        owner => 'root',
        group => 'root',
        mode  => '0440',
    }
