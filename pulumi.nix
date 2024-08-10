{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation {
  pname = "pulumi";
  version = "3.128.0";
  src = pkgs.fetchurl {
    url = "https://get.pulumi.com/releases/sdk/pulumi-v3.128.0-linux-x64.tar.gz";
    sha256 = "sha256-0CtD2FKGWsG2ui0ggyxCgk1qcfBbZlg5RYqcbBrDypU=";
  };
  installPhase = ''
    mkdir -p $out/bin
    tar -xzf $src -C $out/bin --strip-components=1
  '';
  meta = with pkgs.lib; {
    description = "Pulumi CLI";
    license = licenses.mit;
    platforms = platforms.linux;
  };
}
