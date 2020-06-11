GLI_TITLE='GLI - Configure network'
INTERFACES=()

for IFACE in $(ls /sys/class/net); do
    [[ ${IFACE} =~ (lo|lo0) ]] && continue
    INTERFACES+=( "${IFACE}" "${IFACE}" )
done

if [[ -z "${INTERFACES[@]}" ]]; then
    "${GLI_D}" \
        --title "${GLI_TITLE}" \
        --backtitle "${GLI_BTITLE}" \
        --msgbox 'No network interface found to configure.' 0 0
    exit 1
fi

exec 3>&1
MY_INTERFACE=$( echo "${INTERFACES[@]}" | xargs \
    "${GLI_D}" \
    --title "${gli_title}" \
    --backtitle "${GLI_BTITLE}" \
    --menu 'Please select a network interface to configure:' 0 0 0 \
2>&1 >&3 )
exec 3>&-

echo "MY_INTERFACE: ${MY_INTERFACE}"
