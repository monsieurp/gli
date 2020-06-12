GLI_TITLE='GLI - Start sshd'
ERROR=0

"${GLI_D}" \
    --title 'GLI - Start sshd' \
    --backtitle "${GLI_BTITLE}" \
    --yesno 'Would you like to start sshd for this installation?

sshd can be started to allow other users
to access the system during the installation.' 0 0
RC=$?

if [[ ${RC} -eq 0 ]]; then
    OUTPUT=$( rc-service sshd start 2>&1 > /dev/null )
    RC=$?

    if [[ ${GLI_DEBUG} -eq 1 ]]; then
        gli_debug "sshd: OUTPUT = [${OUTPUT}]"
        gli_debug "sshd: RC = [${RC}]"
    fi
    
    if [[ ${RC} -eq 0 ]]; then
        "${GLI_D}" \
            --title "${GLI_TITLE}" \
            --backtitle "${GLI_BTITLE}" \
            --msgbox "sshd started successfully!" 0 0
    else
        "${GLI_D}" \
            --title "${GLI_TITLE}" \
            --backtitle "${GLI_BTITLE}" \
            --yes-label "Continue" \
            --no-label "Restart Installation" \
            --yesno "Could not start sshd:
    
    ${OUTPUT}" 0 0
        ERROR=$?
    fi
fi

exit ${ERROR}
