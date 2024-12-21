{ pkgs }: {
  deps = [
    pkgs.geckodriver
    pkgs.lsof
    pkgs.python39Full
    pkgs.nodejs
    pkgs.glibc
    pkgs.gobject-introspection
    pkgs.gtk3
    pkgs.nss
    pkgs.libdrm
    pkgs.python3
    pkgs.chromedriver
    pkgs.chromium
  ];
}
