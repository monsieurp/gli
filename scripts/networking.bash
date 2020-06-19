. "${GLI_SCRIPTSDIR}"/varfunc.bash
_0=$(basename "$0"); _0=${_0%%.bash};

GLI_TITLE='GLI - Network configuration'
INTERFACES=()
METHODS=$(cat << 'EOF'
DHCPv4|Get IPv4 using dhcpcd
DHCPv6|Get IPv6 using dhcpcd
Static IPv4|Set up IPv4 manually
Skip|Skip interface configuration
EOF
)

for IFACE in /sys/class/net/*; do
    IFACE=$(basename "${IFACE}")
    [[ ${IFACE} =~ (lo|lo0) ]] && continue
    INTERFACES+=( "${IFACE}" "${IFACE}" )
done

if [[ ${GLI_DEBUG} -eq 1 ]]; then
    gli_debug "${_0}: INTERFACES = ${INTERFACES[*]}"
fi

if [[ -z "${INTERFACES[*]}" ]]; then
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

if [[ ${GLI_DEBUG} -eq 1 ]]; then
    gli_debug "${_0}: MY_INTERFACE = ${MY_INTERFACE}"
fi

if [[ -z ${MY_INTERFACE} ]]; then
    exit 1
fi

GLI_D_METHODS=$(cat << EOF
${GLI_D} \
    --title "${GLI_TITLE}" \
    --backtitle "${GLI_BTITLE}" \
    --menu "How do you want to configure ${MY_INTERFACE}?" 0 0 0 \
    $(gli_fmt_d_menu "${METHODS}")
EOF
)

exec 3>&1
MY_METHOD=$( eval "${GLI_D_METHODS}" 2>&1 >&3 )
exec 3>&-

if [[ ${GLI_DEBUG} -eq 1 ]]; then
    gli_debug "${_0}: MY_METHOD = ${MY_METHOD}"
fi

if [[ -z ${MY_METHOD} ]]; then
    exit 1
fi

ERROR=0
case "${MY_METHOD}" in
    "DHCPv4")
        pkill -9 dhcpcd
        "${GLI_D}" \
            --title "${GLI_TITLE}" \
            --backtitle "${GLI_BTITLE}" \
            --infobox "Launching \"dhcpcd -4\" on ${MY_INTERFACE} ..." 0 0
        sleep 1
        SUB=$( dhcpcd -4 "${MY_INTERFACE}" 2>&1 )
        RC=$?
        if [[ ${RC} -ne 0 ]]; then
            "${GLI_D}" \
                --title "${GLI_TITLE}" \
                --backtitle "${GLI_BTITLE}" \
                --msgbox "Failed to get DHCPv4 lease for ${MY_INTERFACE}!

${SUB}
" 0 0
            ERROR=1
        else
            "${GLI_D}" \
                --title "${GLI_TITLE}" \
                --backtitle "${GLI_BTITLE}" \
                --msgbox "DHCPv4 lease for ${MY_INTERFACE} acquired successfully!" \
                0 0
        fi

        if [[ ${GLI_DEBUG} -eq 1 ]]; then
            gli_debug "${_0}: dhcpcd -4 ${MY_INTERFACE} = ${RC}"
            gli_debug "${_0}: dhcpcd -4 ${MY_INTERFACE} = ${SUB}"
        fi
    ;;

    "DHCPv6")
        pkill -9 dhcpcd
        "${GLI_D}" \
            --title "${GLI_TITLE}" \
            --backtitle "${GLI_BTITLE}" \
            --infobox "Launching \"dhcpcd -6\" on ${MY_INTERFACE} ..." 0 0
        sleep 1
        SUB=$( dhcpcd -6 "${MY_INTERFACE}" 2>&1 )
        RC=$?
        if [[ ${RC} -ne 0 ]]; then
            "${GLI_D}" \
                --title "${GLI_TITLE}" \
                --backtitle "${GLI_BTITLE}" \
                --msgbox "Failed to get DHCPv6 lease for ${MY_INTERFACE}!

${SUB}
" 0 0
            ERROR=1
        else
            "${GLI_D}" \
                --title "${GLI_TITLE}" \
                --backtitle "${GLI_BTITLE}" \
                --msgbox "DHCPv6 lease for ${MY_INTERFACE} acquired successfully!" \
                0 0
        fi

        if [[ ${GLI_DEBUG} -eq 1 ]]; then
            gli_debug "${_0}: dhcpcd -6 ${MY_INTERFACE} = ${RC}"
            gli_debug "${_0}: dhcpcd -6 ${MY_INTERFACE} = ${SUB}"
        fi
    ;;

    "Static IPv4")
        exec 3>&1
        MY_IPV4_CFG=$( "${GLI_D}" \
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

        mapfile -t <<< "${MY_IPV4_CFG}"

        MY_IPV4_CFG=( "${MAPFILE[@]}" )

        unset MAPFILE

        if [[ ${GLI_DEBUG} -eq 1 ]]; then
            gli_debug "${_0}: MY_IPV4_CFG = ${MY_IPV4_CFG[*]}"
        fi

        MY_IPV4_COMMANDS=(
            "ip route del default"
            "ifconfig ${MY_INTERFACE} down"
            "ifconfig ${MY_INTERFACE} ${MY_IPV4_CFG[0]} netmask ${MY_IPV4_CFG[1]} up"
            "ip route add default via ${MY_IPV4_CFG[2]} dev ${MY_INTERFACE}"
        )
        LEN=${#MY_IPV4_COMMANDS[*]}

        for (( i = 0; i <= $(( LEN -1 )); i++ )); do
            sleep 1
            SUB=$( ${MY_IPV4_COMMANDS[$i]} 2>&1 )
            RC=$?
            if [[ $RC -eq 0 ]]; then
                "${GLI_D}" \
                    --title "${GLI_TITLE}" \
                    --backtitle "${GLI_BTITLE}" \
                    --msgbox "\"${MY_IPV4_COMMANDS[$i]}\" OK!" 0 0
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

    "Skip")
        :
    ;;
esac

if [[ ${ERROR} -ne 1 ]]; then
    "${GLI_D}" \
        --title "${GLI_TITLE}" \
        --backtitle "${GLI_BTITLE}" \
        --msgbox "Network has been configured successfully!" 0 0
fi

exit ${ERROR}
