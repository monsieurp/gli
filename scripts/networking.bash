GLI_TITLE='GLI - Configure network'
INTERFACES=()

for IFACE in $(ls /sys/class/net); do
    [[ ${IFACE} =~ (lo|lo0) ]] && continue
    INTERFACES+=( "${IFACE}" "${IFACE}" )
done

if [[ ${GLI_DEBUG} -eq 1 ]]; then
    gli_debug "networking: INTERFACES = [${INTERFACES[@]}]"
fi

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
        --title "${GLI_TITLE}" \
        --backtitle "${GLI_BTITLE}" \
        --menu 'Please select a network interface to configure:' 0 0 0 \
2>&1 >&3 )
exec 3>&-

if [[ -z ${MY_INTERFACE} ]]; then
    exit 1
fi

exec 3>&1
MY_METHOD=$( "${GLI_D}" \
    --title "${GLI_TITLE}" \
    --backtitle "${GLI_BTITLE}" \
    --radiolist "How do you want to configure ${MY_INTERFACE}?" 0 0 0 \
    "1" "DHCP" ON \
    "2" "Static IPv4" OFF \
2>&1 >&3 )
exec 3>&-

ERROR=0
case "${MY_METHOD}" in
    1)
        "${GLI_D}" \
            --title "${GLI_TITLE}" \
            --backtitle "${GLI_BTITLE}" \
            --infobox "Launching dhcpcd on ${MY_INTERFACE} ..." 0 0
            SUB=$( dhcpcd -4 ${MY_INTERFACE} 2>&1 )
            RC=$?
            if [[ ${RC} -ne 0 ]]; then
                "${GLI_D}" \
                    --title "${GLI_TITLE}" \
                    --backtitle "${GLI_BTITLE}" \
                    --msgbox "Failed to get DHCP lease for ${MY_INTERFACE}!

${SUB}
" 0 0
            ERROR=1
            else
                "${GLI_D}" \
                    --title "${GLI_TITLE}" \
                    --backtitle "${GLI_BTITLE}" \
                    --msgbox "DHCP lease for ${MY_INTERFACE} acquired successfully!"
            fi
    ;;
    2)
        exec 3>&1
        MY_IPV4=$( "${GLI_D}" \
            --title "${GLI_TITLE}" \
            --backtitle "${GLI_BTITLE}" \
            --form 'IPv4 configuration' 0 0 0 \
                'IP Address' 1 0 '192.168.1.2' 1 20 16 0 \
                'Subnet Mask' 2 0 '255.255.255.0' 2 20 16 0 \
                'Default Router' 3 0 '192.168.1.1' 3 20 16 0 \
 2>&1 1>&3 )
        RC=$?
        if [[ ${RC} -eq 1 ]]; then
            exit 1;
        fi
        exec 3>&-

        MY_IPV4=( $(echo "${MY_IPV4}" | tr '\n' ' ' | awk '{
            split($0, a, " ");
            printf "%s %s %s", a[1], a[2], a[3];
        }') )

        MY_IPV4_COMMANDS=(
            "ifconfig ${MY_INTERFACE} down"
            "ifconfig ${MY_INTERFACE} ${MY_IPV4[0]} netmask ${MY_IPV4[1]} up"
            "ip route del default"
            "ip route add default via ${MY_IPV4[2]} dev ${MY_INTERFACE}"
        )
        LEN=${#MY_IPV4_COMMANDS[*]}

        for (( i = 0; i <= $(( $LEN -1 )); i++ )); do
            SUB=$( ${MY_IPV4_COMMANDS[$i]} 2>&1 )
            RC=$?
            if [[ $RC -eq 0 ]]; then
                "${GLI_D}" \
                    --title "${GLI_TITLE}" \
                    --backtitle "${GLI_BTITLE}" \
                    --msgbox "\"${MY_IPV4_COMMANDS[$i]}\" ran without error!" 0 0
            else
                "${GLI_D}" \
                    --title "${GLI_TITLE}" \
                    --backtitle "${GLI_BTITLE}" \
                    --msgbox "\"${MY_IPV4_COMMANDS[$i]}\" failed!

${SUB}" 0 0
                ERROR=1
            fi
        done
    ;;
esac

exit ${ERROR}
