{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation {
  pname = "pulumi";
  version = "3.141.0";
  src = pkgs.fetchurl {
    url = "https://get.pulumi.com/releases/sdk/pulumi-v3.141.0-linux-x64.tar.gz";
    sha256 = "sha256-gbUeSuxw58jyKHou2It4AfTK3gdMrMnzzDyoUsrkdwA=";
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
