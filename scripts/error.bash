ERROR=$1
if [[ -n ${ERROR} ]]; then
    ERROR="${ERROR}\n\n"
fi

"${GLI_D}" \
    --title 'GLI - Error!' \
    --backtitle "${GLI_BTITLE}" \
    --yes-label 'Restart' \
    --no-label 'Exit' \
    --yesno "${ERROR}GLI encountered an error.

Would you like to restart
GLI or exit now?" 0 0
RC=$?

if [[ $RC -eq 0 ]]; then
    exec gli main
else
    kill $PPID
fi
