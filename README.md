freeotp-cli
===========

If you backup `org.fedorahosted.freeotp` and untar it via

    ( printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" ; tail -c +25 backup.ab ) |  tar xfvz -

or just download the `tokens.xml` file from your phone, this utility will
allow you to read that file and generate a TOPT from it.
