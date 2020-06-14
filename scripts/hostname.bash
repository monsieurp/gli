. ${GLI_SCRIPTSDIR}/varfunc.bash
_0=$(basename $0); _0=${_0%%.bash};

GLI_TITLE='GLI - Set hostname'
ERROR=0

exec 3>&1
MY_HOSTNAME=$( "${GLI_D}" \
    --title "${GLI_TITLE}" \
    --backtitle "${GLI_BTITLE}" \
    --nocancel \
    --inputbox 'Please set a hostname for this machine.' 0 0 $(hostname) \
2>&1 1>&3 )

RC=$?
if [[ ${RC} -eq 0 ]]; then
    cat > ${GLI_MOUNT}/etc/conf.d/hostname << EOF
# Set the hostname of this machine
hostname="${MY_HOSTNAME}"
EOF
    ERROR=$?
else
    ERROR=1
fi

exit ${ERROR}
