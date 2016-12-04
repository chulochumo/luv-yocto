FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "file://interfaces-luv \
            file://ifup-lo \
	    file://networking.service \
           "

inherit systemd

SYSTEMD_PACKAGES =+ "${PN}"
SYSTEMD_SERVICE_${PN} = "networking.service"

do_install_append () {
	install -d ${D}/${systemd_unitdir}/system
	install -m 644 ${WORKDIR}/networking.service ${D}/${systemd_unitdir}/system
	sed -i -e 's,@libexecdir@,${libexecdir},g' ${D}/${systemd_unitdir}/system/networking.service
	install -d ${D}/${libexecdir}
	install -m 755 ${WORKDIR}/init ${D}/${libexecdir}/networking
	install -d ${D}/etc/systemd/system/multi-user.target.wants
	install -m 644 ${WORKDIR}/networking.service ${D}/etc/systemd/system/multi-user.target.wants/
	install -m 0644 ${WORKDIR}/interfaces-luv ${D}${sysconfdir}/network/interfaces
	install -m 0755 ${WORKDIR}/ifup-lo ${D}${sysconfdir}/network/if-up.d
}

RDEPENDS_${PN} +="ifupdown debianutils"

FILES_${PN} += "${systemd_unitdir}/system/networking.service \
		${libexecdir}/networking \
		"
