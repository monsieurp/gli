GLI_TITLE='GLI - Start sshd'

"${GLI_D}" \
    --title 'GLI - Start sshd' \
    --backtitle "${GLI_BTITLE}" \
    --yesno 'Would you like to start sshd for this installation?

sshd can be started to allow other users
to access the system during the installation.' 0 0
RC=$?

if [[ ${RC} -eq 0 ]]; then
    OUTPUT=$(rc-service sshd start 2>&1 > /dev/null)
    RC=$?
    
    if [[ ${RC} -eq 0 ]]; then
        "${GLI_D}" \
            --title "${GLI_TITLE}" \
            --backtitle "${GLI_BTITLE}" \
            --msgbox "sshd started successfully!" 0 0
    else
        "${GLI_D}" \
            --title "${GLI_TITLE}" \
            --backtitle "${GLI_BTITLE}" \
            --yes-label "Restart Installation" \
            --no-label "Continue" \
            --yesno "Could not start sshd:
    
    ${OUTPUT}" 0 0
        RC=$?
        if [[ ${RC} -eq 0 ]]; then
            gli main
        fi
    fi
    
fi
