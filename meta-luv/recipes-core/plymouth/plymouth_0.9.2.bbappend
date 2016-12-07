FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

RDEPENDS_${PN} = "ttf-dejavu-common ttf-dejavu-sans ttf-dejavu-sans-mono"

SRC_URI+= "file://0001-plymouth-Add-the-retain-splash-option.patch \
	   file://0001-plymouth-Change-the-plymouth-defaults.patch \
	   file://0001-plymouth-modify-the-script-theme.patch \
	   ${SPLASH_IMAGES}"

SRC_URI_append_x86 = " file://0001-plymouth-Specify-number-of-test-suites-in-x86.patch"
SRC_URI_append_x86-64 = " file://0001-plymouth-Specify-number-of-test-suites-in-x86-64.patch"
SRC_URI_append_aarch64 = " file://0001-plymouth-Specify-number-of-test-suites-in-ARM.patch"

SPLASH_IMAGES = "file://luv-splash.png;outsuffix=default"

do_install_append() {
	install -d ${datadir}/plymouth
	install -m 755 ${WORKDIR}/luv-splash.png ${D}/${datadir}/plymouth/
}

LOGO = "${datadir}/plymouth/luv-splash.png"
RDEPENDS_${PN}-initrd = "bash"
